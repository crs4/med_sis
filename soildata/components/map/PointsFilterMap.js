"use client"

import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, LayersControl, GeoJSON } from 'react-leaflet';
import L from 'leaflet';
import { bbox, feature, featureCollection } from '@turf/turf';
import "leaflet-providers";
import "leaflet/dist/leaflet.css";
import MapLegend from './legend';
import ProfileService from '../../service/profiles';
import Loading from '../Loading';

const LayersGeoJSON = ({ layersRef, points, area }) => {
  const map = useMap()
  
  const areaStyle = ({ properties }) => {
    return {
      "color": "#00aa00",
      "weight": 2,
      "fillOpacity": 0.6,
      "fillColor": "#00ff00",
    };
  };

  // It defines the style of the points of the measure 
  function pointToLayer (feature, latlng) {
    if ( feature && feature.properties && feature.properties.outlier )
      return L.circleMarker(latlng, { radius: 8, fillColor: '#f76218', color: '#a21505', weight: 2, opacity: 1, fillOpacity: 1 }); 
    return L.circleMarker(latlng, { radius: 8, fillColor: '#188ff7', color: '#0805a2', weight: 2, opacity: 1, fillOpacity: 1 });
  };

  function onEachFeature (feature, layer) {
    const popupOptions = {
      minWidth: 100,
      maxWidth: 250,
      className: 'popup-classname'
    };
    if (feature && feature.properties) {
      layer.bindPopup(() => {
        return feature.properties.popup;
      }, popupOptions);
    }
  }

  useEffect(() => {
    try {
      if (!map)
        return;
      if ( layersRef.current ){
        map.removeLayer(layersRef.current)
      }
      const layers = [] 
      if ( area ){
        layers.push( L.geoJSON( area, {
          style: areaStyle
        }))
      }
      if ( points ){
        layers.push( L.geoJSON( points, {
          pointToLayer: pointToLayer,
          onEachFeature: onEachFeature
        }) )
      }
      if ( layers.length > 0 )
        layersRef.current = L.layerGroup(layers).addTo(map);
      else layersRef.current = null;
    } catch (error) {
      console.log(error)
    }
  
  }, [points, area, layersRef]);   // eslint-disable-line
  return null
};

// Map for AOI selection
export default function PointsFilterMap ({
  points, /* Soil points data */
  area, /* Area of interest */}) 
{
  let bounds = [[10, -10],[ 50, 50]];
  const legend = useRef(null); 
  const layersRef = useRef(null);  
  const bboxArray = area? bbox(area) : bbox(points);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];

  // default zoom
  let zoom = 7;

  return (
      <MapContainer
        doubleClickZoom={false}
        id='pointsfilterMap'
        zoom={zoom}
        bounds={bounds}
        style={{ width: '100%', height: '500px' }}
      > 
        <TileLayer
          url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
          attribution='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
        />
        <LayersGeoJSON area={area} points={points} layersRef={layersRef} /> 
        <MapLegend legend={legend} data={{pointsFilter: true}} position="bottomleft" />  
      </MapContainer> 
  );
};
  