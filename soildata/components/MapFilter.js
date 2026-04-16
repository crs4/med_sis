import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import { bbox, point, polygon, multiPolygon, booleanPointInPolygon, booleanIntersects } from '@turf/turf';
import 'leaflet-providers';
import { GeoJSON } from 'react-leaflet/GeoJSON';
import '@geoman-io/leaflet-geoman-free';
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css';
import ProfileService from '../service/profiles';
import { Fieldset } from 'primereact/fieldset';
import { Dropdown } from 'primereact/dropdown';
import { FileUpload } from 'primereact/fileupload';
import { Button } from 'primereact/button';


const GeomanControl = ({ toolbarRef, setPolygon }) => {
  const map = useMap();
  const toolOptions = {
      position: 'topleft', 
      oneBlock: true,
      drawMarker: false,
      drawCircleMarker: true,
      drawPolyline: false,
      drawPolygon: false,
      drawCircle: false,
      drawText: false,
      editMode: false,
      dragMode: false,
      cutPolygon: false,
      removalMode: false,
      rotateMode: false,    
  }
  const geomanControl = L.Control.extend({
    options: {},
    initialize(options) {
      L.setOptions(this, options);
    },
    addTo(map) {
      map.pm.addControls({
        ...this.options,
      });
      map.pm.setGlobalOptions({ snappable: false });
      map.on('pm:drawstart', (e) => {
        map.pm.getGeomanDrawLayers(false).forEach(
          (geomanLayer) => {
            map.removeLayer(geomanLayer);
          }
        )
      })
      map.on('pm:create', async (e) => {
        map.pm.disableDraw();
        if ( map.output) 
        {
          const geojson = e.layer.toGeoJSON();
          if (( geojson.geometry.type === 'Polygon' &&
                map.isValidBox(geojson) === true ) ||
              ( geojson.geometry.type === 'Point' &&
                map.isValidPoint(geojson) === true ))
          {
            setPolygon(geojson);
          }
        }  
        map.pm.getGeomanDrawLayers(false).forEach(
          (geomanLayer) => {map.removeLayer(geomanLayer);})
      });
    }, 
  })
  
  const toolbar = function(opts) {
    return new geomanControl(opts);
  }

  useEffect(() => {
    if (!map || !map.pm || toolbarRef.current )
      return;
    toolbarRef.current = (toolbar(toolOptions)).addTo(map);
  }, [map, toolbarRef]); // eslint-disable-line 


  return null  
};

export default function S4Mmap ({areasDsList, points, output}) {
  let bounds = [[20, -2],[ 50, 40]];
  const [polygons, setPolygons] = useState(null)
  const [polygon, setPolygon] = useState(null)
  const [areasDs, setAreasDs] = useState(null)
  const geojson = useRef(null);  
  const toolbar = useRef(null);
  const bboxArray = bbox(points);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];

  const setAreaStyle = ({ properties }) => {
    return {
      "color": "#2266ff'",
      "weight": 2,
      "fillOpacity": 0.1,
      "fillColor": "#6699ff"
    };
  };

  const setSelectStyle = ({ properties }) => {
    return {
      "color": "#ffff66'",
      "weight": 2,
      "fillOpacity": 0.1,
      "fillColor": "#ffff66"
    };
  };

  function pointToLayer (feature, latlng) {
    let style = {
      radius: 8, fillColor: '#66ff66', color: '#ff6666', weight: 2, opacity: 1, fillOpacity: 0.3,
    };
    return L.circleMarker(latlng, style);
  }

  let zoom = 7;
  
  const isValidPoint = (pin) => {
    const pt = point(pin.geometry.coordinates);
    const p = null;
    let isValid = false;
    for (let geoIndex = 0; geoIndex < mapData.features.length; geoIndex += 1) {
      const feature = mapData.features[geoIndex];
      if (feature.geometry.type === 'MultiPolygon') {
        const turfShape = multiPolygon(feature.geometry.coordinates);
        if (booleanPointInPolygon(pt, turfShape) === true) {
          isValid = true;
          break;
        };
      } else if (feature.geometry.type === 'Polygon') {
        const turfShape = polygon(feature.geometry.coordinates);
        if (booleanPointInPolygon(pt, turfShape) === true) {
          isValid = true;
          break;
        };
      }
      if ( !p && isValid )
        p = feature;
    }
    if ( p && isValid )
      setPolygon(p);
    return isValid;
  }
      
  const isValidBox = (box) => {
    const plg = polygon(box.geometry.coordinates);
    let isValid = false;
    const p = null;
    if ( mapData )
      for (let geoIndex = 0; geoIndex < mapData.features.length; geoIndex += 1) {
        const feature = mapData.features[geoIndex];
        if (feature.geometry.type === 'MultiPolygon') {
          const turfShape = multiPolygon(feature.geometry.coordinates);
          if (booleanIntersects(plg, turfShape) === true) {
            isValid = true;
            break;
          };
        } else if (feature.geometry.type === 'Polygon') {
          const turfShape = polygon(feature.geometry.coordinates);
          if (booleanIntersects(plg, turfShape) === true) {
            isValid = true;
            break;
          };
        }
        if ( !p && isValid )
          p = feature;
      }
    if ( p && isValid )
      setPolygon(p);
    return isValid;
  }

  useEffect(() => {
    setLoading(true)
    const response = ProfileService.getDataset(areasDs, document.cookie) 
    if ( response && response.data ) {
      toast.current.show({severity:'success', summary: 'Done!', detail:'Ok Dataset polygons loaded', life: 3000});      
      setPolygons(response.data) 
    }
    else toast.current.show({severity:'error', summary: 'Error', detail:'Errors loading polygons', life: 3000});
    setLoading(false)
  }, [areasDs]); // eslint-disable-line 
  
  return (
  <div className="Card flex flex-column gap-2">
    <Fieldset classname="flex flex-column" legend="Area Of Interest Selection">
      <h5>Select a Med-SIS dataset then click on a polygon in the map</h5>
      <Dropdown id="areasDs" classname="md:w-30rem" optionLabel="name" value={areasDs} options={areasDsList} 
          onChange={(e) => setAreasDs(e.value)} placeholder="Select a Dataset"/>
      <h5>or upload a custom polygon</h5>
      <FileUpload 
        disabled={fileId !== null || validating}
        id="file"
        ref={roiFileRef}
        accept='.json, .geojson'
        chooseLabel={t('CUSTOM_POLYGON')}
        mode="basic"
        multiple={false}
        customUpload
        auto
        className='mb-4 mr-2 mt-4'
        uploadHandler={(e) => validateRoiFile(e.files)}
      /> 
      <MapContainer
        doubleClickZoom={false}
        id='RoiSelector'
        zoom={zoom}
        bounds={bounds}
        style={{ height: '500px' }}
      > 
        <TileLayer
          url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <GeomanControl toolbarRef={toolbar} isValidPoint={isValidPoint} setMapData={setMapData} isValidBox={isValidBox} output={output} /> 
            
        { polygons && (
          <GeoJSON
            key="areas"
            ref={geojson} 
            data={polygons}
            style={setAreaStyle}
          />
        )}
        { polygon && (
          <GeoJSON
            key="area"
            data={polygon}
            style={setSelectStyle}
          />
        )}
        { points && (
          <GeoJSON
            key="points"
            data={points}
            pointToLayer={pointToLayer}
          />
        )}     
      </MapContainer>
      <Button
        label={t('setAoi')}
        icon='pi pi-save'
        type='button'
        disabled={ !polygon }
        className='mt-4 flex mr-4'
        onClick={() => { output(polygon); }}
      />
    </Fieldset>
  </div>  
  );
};




        