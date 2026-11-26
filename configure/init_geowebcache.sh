#!/usr/bin/env bash
set -euo pipefail
# Run inside Django container, beside manage.py.
python /usr/src/s4m_catalogue/manage.py shell <<'PY'
from django.conf import settings
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote
import os

WORKSPACE = 'geonode'
STORE = 'backoffice'
DRY_RUN = os.environ.get('GWC_DRY_RUN', '0') == '1'
config = settings.OGC_SERVER['default']
base = config['LOCATION'].rstrip('/')
s = requests.Session()
s.auth = (config['USER'], config['PASSWORD'])

def request(method, path, **kwargs):
    r = s.request(method, base + path, timeout=60, **kwargs)
    r.raise_for_status()
    return r

def esc(value):
    return quote(value, safe=':')

# Discover published vector layers belonging to this PostGIS store.
path = f'/rest/workspaces/{esc(WORKSPACE)}/datastores/{esc(STORE)}/featuretypes.json'
items = request('GET', path).json().get('featureTypes', {}).get('featureType', []) or []
if not items:
    raise SystemExit('No feature types found; check workspace/store.')
root = ET.fromstring(request('GET', '/gwc/rest/layers.xml').content)
existing = {e.text for e in root.findall('./layer/name')}
created = skipped = failed = 0
for item in items:
    name = item['name']
    qualified = f'{WORKSPACE}:{name}'
    if qualified in existing:
        print(f'SKIP {qualified}: already configured', flush=True)
        skipped += 1
        continue
    try:
        layer = ET.fromstring(request('GET', f'/rest/layers/{esc(qualified)}.xml').content)
        layer_id = layer.findtext('id')
        payload = ET.Element('GeoServerLayer')
        if layer_id:
            ET.SubElement(payload, 'id').text = layer_id
        ET.SubElement(payload, 'enabled').text = 'true'
        ET.SubElement(payload, 'name').text = qualified
        formats = ET.SubElement(payload, 'mimeFormats')
        ET.SubElement(formats, 'string').text = 'image/png'
        grids = ET.SubElement(payload, 'gridSubsets')
        for grid in ('EPSG:4326', 'EPSG:900913'):
            ET.SubElement(ET.SubElement(grids, 'gridSubset'), 'gridSetName').text = grid
        meta = ET.SubElement(payload, 'metaWidthHeight')
        for _ in range(2):
            ET.SubElement(meta, 'int').text = '4'
        ET.SubElement(payload, 'gutter').text = '0'
        ET.SubElement(payload, 'autoCacheStyles').text = 'true'
        endpoint = f'/gwc/rest/layers/{esc(qualified)}.xml'
        if DRY_RUN:
            print(f'WOULD CREATE {qualified}', flush=True)
            continue
        request('PUT', endpoint, data=ET.tostring(payload, encoding='utf-8'), headers={'Content-Type': 'text/xml'})
        request('GET', endpoint)
        created += 1
        print(f'OK {qualified}', flush=True)
    except (requests.RequestException, ET.ParseError) as exc:
        failed += 1
        print(f'ERROR {qualified}: {exc}', flush=True)
        if isinstance(exc, requests.HTTPError) and exc.response is not None:
            print(exc.response.text[:1000], flush=True)
print(f'Total: {len(items)} | Created: {created} | Existing: {skipped} | Errors: {failed} | Dry run: {DRY_RUN}')
if failed:
    raise SystemExit(1)
PY
