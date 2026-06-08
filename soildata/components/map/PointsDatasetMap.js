"use client"

import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, LayersControl, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import { bbox } from '@turf/turf';
import "leaflet-providers";
import "leaflet/dist/leaflet.css";
import MapLegend from './legend';
import ProfileService from '../../service/profiles';
import Loading from '../Loading';

// Map for AOI selection
export default function Page ({
  fPoints, /* Soil points data */
  area, /* Area of interest */
  kPoints, /* aggregated points */}) 
{
  let bounds = [[10, -10],[ 50, 50]];
  const legend = useRef(null); 
  const legend2 = useRef(null); 
  const pointsRef = useRef(null);  
  const areaRef = useRef(null); 
  const [ points, setPoints ] = useState(fPoints)
  const [ aoi, setAoi ] = useState(area) 
  const bboxArray = area? bbox(area) : bbox(fPoints);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  
  // Filtered Points Soil Data Map configuration
  const createPopupContent = (feature) => {
    try {
      if ( feature && feature.properties ){
        let panel = '<div class="flex flex-wrap w-full">';
        const max = 6;
        Object.keys(feature.properties).forEach(
          (field) => {
            if ( max > 0 ){
              panel += '<span class="text-cyan-500 align-items-center font-bold" >' + field + '</span>';
              panel += '<span>' + (feature.properties[field]) + '</span>';
            }
            max -= 1;
          }
        );
        panel += '</div>'; 
      }
      return panel;
    } catch (e) {
      console(e)
    }
    return '<div><span class="font-bold">No data</span></div>';  
  } 

  // It defines the style of the Area Of Interest 
  const setAreaStyle = ({ properties }) => {
    return {
      "color": "#00aa00",
      "weight": 2,
      "fillOpacity": 0.6,
      "fillColor": "#00ff00",
    };
  };

  // It defines the style of the measure points 
  function pointToLayer (feature, latlng) {
    return L.circleMarker(latlng, { radius: 8, fillColor: '#3767ab', color: '#1205a2', weight: 2, opacity: 1, fillOpacity: 0.3, });
  };

  function onEachFeature (feature, layer) {
    const popupOptions = {
      minWidth: 100,
      maxWidth: 250,
      className: 'popup-classname'
    };
    if ( feature.properties ) {
      layer.bindPopup(() => {
        return createPopupContent(feature);
      }, popupOptions);
    }
  }
  
  // default zoom
  let zoom = 7;

  return (
      <MapContainer
        doubleClickZoom={false}
        id='pointsfilterMap'
        zoom={zoom}
        bounds={bounds}
        style={{ height: '500px', width: '100%' }}
      > 
        <TileLayer
          url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
          attribution='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
        />
      { aoi && (
        <GeoJSON
          key="area"
          ref={areaRef} 
          data={aoi}
          style={setAreaStyle}
        />
      )}
      { points && (
        <GeoJSON
          key="points"
          ref={pointsRef}
          data={points}
          pointToLayer={pointToLayer}
          onEachFeature={onEachFeature}
        />
      )}
        <MapLegend legendRef={legend2} data={{pointsFilter: true}} position="bottomleft" />  
      </MapContainer> 
  );
};
  