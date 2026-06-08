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

const FilteredPointsGeoJSON = ({ pointsRef, points }) => {
  const map = useMap()

  // Filtered Points Soil Data Map configuration
  const createPopupContent = (feature) => {
    try {
      if ( feature && feature.properties ){
        let panel = '<div class="flex flex-wrap  justify-content-center">';
        Object.keys(feature.properties).forEach(
          (field) => {
            panel += '<span class="text-cyan-500 align-items-center font-bold" >' + field + '</span>';
            panel += '<span>' + (feature.properties[field]) + '</span>';
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
    if ( feature.properties ){
      layer.bindPopup(() => {
        return createPopupContent(feature);
      }, popupOptions);
    }
  }

  useEffect(() => {
    if (!map)
      return;
    if ( pointsRef?.current ){
      map.removeLayer(pointsRef.current)
    }
    if ( data ){
      pointsRef.current = L.geoJSON(data, {
        pointToLayer: pointToLayer,
        onEachFeature: onEachFeature
      }).addTo(map);
    }
    else pointsRef.current = null;
  }, [map, points, pointsRef]);   // eslint-disable-line
  
  return null
};

// Map for AOI selection
export default function PointsFilterMap ({
  points, /* Soil points data */
  area, /* Area of interest */}) 
{
  let bounds = [[10, -10],[ 50, 50]];
  const legend = useRef(null); 
  const pointsRef = useRef(null);  
  const areaRef = useRef(null); 
  const [ fPoints, setFPoints ] = useState(points)
  const [ aoi, setAoi ] = useState(area) 
  const bboxArray = area? bbox(area) : bbox(points);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];

  // It defines the style of the Area Of Interest 
  const setAreaStyle = ({ properties }) => {
    return {
      "color": "#00aa00",
      "weight": 2,
      "fillOpacity": 0.6,
      "fillColor": "#00ff00",
    };
  };

  useEffect(() => {
    setFPoints(points)
    setAoi(area)
    console.log(points)
  }, [points,area]); // eslint-disable-line


  // default zoom
  let zoom = 7;

  return (
      <MapContainer
        doubleClickZoom={false}
        id='pointsfilterMap'
        zoom={zoom}
        bounds={bounds}
        style={{ height: '500px' }}
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
      { fPoints && (
        <FilteredPointsGeoJSON
          key="points"
          ref={pointsRef}
          data={fPoints}
        />
      )}
        <MapLegend legendRef={legend} data={{pointsFilter: true}} position="bottomleft" />  
      </MapContainer> 
  );
};
  