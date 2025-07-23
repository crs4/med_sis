import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, useMapEvents, WMSTileLayer } from 'react-leaflet';
import "leaflet/dist/leaflet.css"
import './leaflet-extensions/htmllegend/L.Control.HtmlLegend';
import { GeoJSON } from 'react-leaflet/GeoJSON';
import { points, bbox, pointsWithinPolygon  } from '@turf/turf';
import { Dropdown } from 'primereact/dropdown';
import { Message } from 'primereact/message';
import { Button } from 'primereact/button';

function SelectArea({setArea, data}) {
    const map = useMapEvents({
        click: async (e) => {
          const { lat, lng } = e.latlng;
          let url = 'http://localhost/geoserver/geonode/ows?service=WFS&version=1.0.0&request=GetFeature&maxFeatures=4&outputFormat=application%2Fjson';
          url += '&typeName=' + data.gsLayer +'&bbox='+lng+','+lat+','+lng+','+lat+'&access_token=' + data.token;
          const response = await fetch (url);
          const aoi = await response.json();
          let p = points([ [lng, lat], ])
          console.log(aoi);
          if ( aoi && aoi.features )
            for ( let x = 0; x < aoi.features.length; x++ ){
              let ok = pointsWithinPolygon(p, aoi.features[x]);
              if ( ok && ok.features.length === 1 )
                setArea(aoi.features[x])
            }
          
        }
    });
    return null;
}

const MapLegend = ({ legendRef }) => {
  const map = useMap();

  useEffect(() => {
    if (!map || legendRef.current ) 
      return;
    console.log (map);
    let layer = null;
    if (layer) {
      legendRef.current = L.control.htmllegend({
        position: 'bottomleft',
        legends: [
          {
            name: 'Availability of data',
            layer,
            opacity: 1,
            elements: [{
              label: 'Data point',
              html: '',
              style: {
                'text-align': 'left',
                'background-color': '#2f2',
                'width': '20px',
                'height': '20px',
                'position': 'relative',
                'margin': '3.75px 0',
              },
            },],
          },
        ],
        collapseSimple: true,
        detectStretched: false,
        collapsedOnInit: false,
        defaultOpacity: 1.0,
      }).addTo(map);
    }
  }, [map, legendRef]);
  return null  
};
/*
const reqMap = {
          layers : {
            gsLayers: gsLayers, 
            aoi: aoi,
            points: avail,
          },
          label: 'AOI selection',
        };
*/
export default function S4Mmap ({toast, setAoi, data}) {
  
  const [ gsLayer, setGsLayer ] = useState(null);
  const [ area, setArea ] = useState(null);
  const [ bounds, setBounds ] = useState(null);
  const fileRef = useRef(null);
  const [fileName, setFileName] = useState(null); 
  const avail = data.layers.points 
  const gsLayers = data.layers.gsLayers
  const zoom = 7;
  const polyStyle = { fillColor: '#aaf', color: '#99d', weight: 2, opacity: 1, fillOpacity: 0.5}
  const controlLegend = useRef(null); // eslint-disable-line
  const url =  'http://localhost/geoserver/geonode/ows?'
  const token = data.token

  function pointToLayer (feature, latlng) {
    let style = { radius: 8, fillColor: '#7f7', color: '#2b2', weight: 2, opacity: 1, fillOpacity: 0.6};
    return L.circleMarker(latlng, style);
  }
  
  function onEachFeature (feature, layer) {
    const popupOptions = {
      minWidth: 100,
      maxWidth: 250,
      className: 'popup-classname'
    };
    if (feature.properties) {
      let panel = '<div class="flex flex-wrap  justify-content-center">';
      panel += '<span class="text-cyan-500 align-items-center font-bold" >' + feature.properties.id + '</span></div>';
      if ( feature.properties.profile ) 
        panel += '<div><span class="font-bold" >Profile: </span><span>' + feature.properties.profile + '</span></div>';
      if ( feature.properties.number ) 
        panel += '<div><span class="font-bold" >Layer: </span><span>' + feature.properties.number + '</span></div>';
      if ( feature.properties.upper ) 
        panel += '<div><span class="font-bold" >Upper: </span><span>' + feature.properties.upper + '</span></div>';
      if ( feature.properties.lower ) 
        panel += '<div><span class="font-bold" >Lower: </span><span>' + feature.properties.lower + '</span></div>';
      layer.bindPopup(() => {
        return panel;
      }, popupOptions);
    }
  }
  
  const readAOIFile = async (file) => {
    
    try {
      // validate geometry first feature
      // Add bbox, area to new geojson
      if ( file ) {
        let _aoi = null
        setFileName(file.name);
        const readFilePromise = (path) => new Promise((resolve, reject) => {
          const readFile = new FileReader();
          readFile.onload = (event) =>  { 
            const contents = event.target.result;
            const geojson = JSON.parse(contents.replaceAll('/n',''));
            /// only first feature
            const feature = geojson.features[0];
            geojson.features = [feature];
            geojson.bbox = bbox(geojson);
            console.log(geojson)
            resolve(geojson);
          };
          readFile.onerror = (error) => {
            reject(error);
          };
          readFile.readAsText(file);
        });     
        await readFilePromise(file)
          .then((result) => _aoi = result );
        if ( !_aoi ){
          //fileRef.current?.clear();
          toast.current.show({severity:'error', summary: 'Error!', detail:'Wrong file!', life: 3000});
        }
        else {
          toast.current.show({severity:'info', summary: 'Success', detail:'AOI set!', life: 3000});
          setAoi(_aoi)
          setArea(_aoi)
          console.log(_aoi)
        }
      }
      
    } catch (error) {
      //fileRef.current?.clear();
      toast.current.show({severity:'error', summary: 'Error!', detail:'Errors reading file!', life: 3000});
    }
  };

  useEffect(() => {
    const bboxArray = bbox(avail);
    if ( bboxArray )
      setBounds( [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]]);  
  }, [avail]);
  
  useEffect(() => {
    if ( area )
      setAoi(area);
  }, [area,setAoi]);

  if ( !avail || !gsLayers || !bounds )
    return <></>;
  else
    return (
    <>
      <div className="card m-4 ">
        <Dropdown value={gsLayer} onChange={(e) => setGsLayer(e.value)} options={gsLayers} optionLabel="name" placeholder="Select a dataset" className="w-full md:w-14rem" />
        <input
          className="hidden"
          type="file"
          accept=".geojson"
          multiple={false}
          ref={fileRef}
          onChange={(e) => readAOIFile(e.target.files[0])}
        />
        <Button
          label='UPLOAD_POLYGON'
          icon="pi pi-image"
          type="button"
          className="p-mr-2 p-mt-2"
          onClick={() => {
            fileRef.current.click();
          }}
        />
        {(fileName) && ( 
        <Message severity="success" content={'File: ' + fileName} /> )}
      </div>
      <MapContainer
        doubleClickZoom={false}
        id='s4mMap'
        zoom={zoom}
        bounds={bounds}
        style={{ height: '400px' }}
      >
        <TileLayer
          url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
          attribution='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
        />
        {gsLayer && (
        <WMSTileLayer 
          url={url}
          params={{ layers: gsLayer, FORMAT: 'image/png', TRANSPARENT: true, access_token: token,  attribution: "<a href='http://localhost/'>Soils4Med SIS</a>" }}
        />)} 
        <GeoJSON
          key={Math.random()}
          pointToLayer={pointToLayer}
          onEachFeature={onEachFeature}
          data={avail}
        /> 
        { area && (
          <GeoJSON
            key={Math.random()}
            style={polyStyle}
            data={area}
          /> 
        )}
        <MapLegend legendRef={controlLegend} />
        { token && gsLayer && (
        <SelectArea setArea={setArea} data={{ token:token, gsLayer: gsLayer}} />
        )}
      </MapContainer>
    </>  
  );
};

      