import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css"
import { bbox } from '@turf/turf';
import './leaflet-extensions/htmllegend/L.Control.HtmlLegend';
import { GeoJSON } from 'react-leaflet/GeoJSON';



export default function S4Mmap ({data}) {
  if ( !data || !data.layer || !data.layer.points )
    return;
  const points = data.layer.points;
  const bboxArray = bbox(points);
  const bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  
  let zoom = 7;

  function pointToLayer (feature, latlng) {
    let style = {
      radius: 8, fillColor: '#aaa', color: '#ddd', weight: 2, opacity: 1, fillOpacity: 0.8,
    };
    return L.circleMarker(latlng, style);
  }
  
  function onEachFeature (feature, layer) {
    const popupOptions = {
      minWidth: 100,
      maxWidth: 250,
      className: 'popup-classname'
    };
    if (feature.properties && feature.properties.popupContent) {
      layer.bindPopup(() => {
        return feature.properties.popupContent;
      }, popupOptions);
    }
  }
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
        {points && (
          <GeoJSON
            key={Math.random()}
            pointToLayer={pointToLayer}
            onEachFeature={onEachFeature}
            data={points} 
          /> )}
      </MapContainer>
    </>  
  );
};


        