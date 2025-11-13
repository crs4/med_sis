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
    if (!map || legendRef.current ) 
      return;
    let JSONlayer = null;
    map.eachLayer(function (layer) {
      if (layer.key = 'pointsGeoJSON' ){
        JSONlayer = layer;
      }
    });
    if (JSONlayer) {
      legendRef.current = L.control.htmllegend({
        position: 'bottomleft',
        legends: [
          {
            name: 'Profiles Status',
            JSONlayer,
            opacity: 1,
            elements: [{
              label: 'OK - profiles without errors',
              html: '',
              style: {
                'text-align': 'left',
                'background-color': '#42c05c',
                'width': '20px',
                'height': '20px',
                'position': 'relative',
                'margin': '3.75px 0',
              },
            },
            {
              label: 'KO - profiles with errors',
              html: '',
              style: {
                'text-align': 'left',
                'background-color': '#d0526c',
                'width': '20px',
                'height': '20px',
                'position': 'relative',
                'margin': '3.75px 0',
              },
            },
            {
              label: 'Warn - profiles with warnings',
              html: '',
              style: {
                'text-align': 'left',
                'background-color': '#777777',
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
  if ( !data || !data.layer || !data.layer.points )
    return;
  const layerJSON = useRef(null); // eslint-disable-line
  const points = data.layer.points;
  const controlLegend = useRef(null); // eslint-disable-line
  const bboxArray = bbox(points);
  const bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  
  
  const defaultstyles = {
    'ok'  : { radius: 8, fillColor: '#2f2', color: '#0d0', weight: 2, opacity: 1, fillOpacity: 0.8},
    'ko'  : { radius: 8, fillColor: '#f22', color: '#d22', weight: 2, opacity: 1, fillOpacity: 0.8},
    'warn': { radius: 8, fillColor: '#f80', color: '#d60', weight: 2, opacity: 1, fillOpacity: 0.8},
  }
  let zoom = 7;

  function pointToLayer (feature, latlng) {
    let style = {
      radius: 8, fillColor: '#aaa', color: '#ddd', weight: 2, opacity: 1, fillOpacity: 0.8,
    };
    if (feature.properties && feature.properties.status )
      style = defaultstyles[feature.properties.status]
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
  //https://services.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile
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
          <>
          <GeoJSON
            jsonRef={layerJSON} 
            key='pointsGeoJSON'
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


        