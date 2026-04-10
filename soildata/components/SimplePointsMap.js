import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css"
import { bbox } from '@turf/turf';
import './leaflet-extensions/htmllegend/L.Control.HtmlLegend';
import { GeoJSON } from 'react-leaflet/GeoJSON';

const Selection =  ({ selRef, element }) => {
  const map = useMap();
  console.log(element)
  if (!map)
    return
  if ( selRef.current )
    map.removeLayer( selRef.current )
  selRef.current = L.polygon ( 
    element.latlngs, 
    { fillColor: '#d18c1dff', color: '#f0f008ff', weight: 3, opacity: 1, fillOpacity: 0 }
  ).addTo(map);
}

export default function S4Mmap ({data, setSelected}) {
  if ( !data || !data.layers || !data.layers.points || !data.layers.selected )
    return;
  const points = data.layer.points;
  const areas = data.layer.areas;
  const controllSelection = useRef(null); // eslint-disable-line
  const bboxArray = bbox(points);
  let bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  let zoom = 7;  

  function pointToLayer (feature, latlng) {
    let style = data.layer.style;
    if ( !style )
      style = { radius: 8, fillColor: 'rgb(213, 223, 9)', color: 'rgb(229, 59, 7)', weight: 2, opacity: 1, fillOpacity: 0.6 };
    return L.circleMarker(latlng, style);
  }

  const setStyle = ({ properties }) => {
    return { fillColor: 'rgb(74, 213, 232)', color: 'rgb(44, 17, 220)', weight: 2, opacity: 1, fillOpacity: 0.2 }; 
  };

  function onEachFeature(feature, layer) {
    //bind click
    layer.on({
        click: setSelected(feature)
    });
  };

  return (
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
      {areas && (
      <GeoJSON
          key='pointsGeoJSON'
          style={setStyle}
          onEachFeature={onEachFeature}
          data={areas}
      />
      )} 
      {selected && (
        <Selection selRef={controllSelection} element={selected}/>
      )}
      <GeoJSON
          key='pointsGeoJSON'
          pointToLayer={pointToLayer}
          data={points}
      /> 
    </MapContainer>
  );
};


        