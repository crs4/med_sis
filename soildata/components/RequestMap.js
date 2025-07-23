import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css"
import { bbox } from '@turf/turf';
import './leaflet-extensions/htmllegend/L.Control.HtmlLegend';
import { GeoJSON } from 'react-leaflet/GeoJSON';

const MapLegend = ({ legendRef }) => {
  const map = useMap();

  useEffect(() => {
    if (!map || !map.pointJSON || !map.pointJSON.current || legendRef.current ) 
      return;
    let layer = map.layerJSON.current;
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

export default function S4Mmap ({data}) {
  if ( !data || !data.layers || !data.layers[0] || !data.layers[1] )
    return;
  const pointJSON = useRef(null); // eslint-disable-line
  const areaJSON = useRef(null); // eslint-disable-line
  const points = data.layers[0].points;
  const pointStyle = data.layers[0].style;
  const aoi = data.layers[1].polygon;
  let polyStyle = data.layers[1].style;
  const controlLegend = useRef(null); // eslint-disable-line
  const bboxArray = bbox(aoi);
  const bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  
  const defaultstyles = {
    'point'  : { radius: 8, fillColor: '#7f7', color: '#2b2', weight: 2, opacity: 1, fillOpacity: 0.6},
    'area'  : { fillColor: '#77f', color: '#00d', weight: 2, opacity: 1, fillOpacity: 0.5},
  }
  let zoom = 7;

  function pointToLayer (feature, latlng) {
    let style = pointStyle;
    if ( !style )
      style = defaultstyles['point'];
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
  
  if ( !polyStyle )
    polyStyle = defaultstyles['area'];

  
  return (
    <>
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
        {points && aoi && (
          <>
          <GeoJSON
            jsonRef2={areaJSON} 
            key={Math.random()}
            data={aoi}
            style={polyStyle}
          /> 
          <GeoJSON
            jsonRef1={pointJSON} 
            key={Math.random()}
            pointToLayer={pointToLayer}
            onEachFeature={onEachFeature}
            data={points}
          /> 
          
          <MapLegend legendRef={controlLegend} />
          </>
        )}
        
      </MapContainer>
    </>  
  );
};


        