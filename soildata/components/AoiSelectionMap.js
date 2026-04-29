"use client"

import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, LayersControl, WMSTileLayer } from 'react-leaflet';
import L from 'leaflet';
import { bbox } from '@turf/turf';
import 'leaflet-providers';
import { GeoJSON } from 'react-leaflet/GeoJSON';
import '@geoman-io/leaflet-geoman-free';
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css';
import ProfileService from '../service/profiles';
import Loading from './Loading';

export default function AoiSelectionMap ({base_url, areasTN, area, points, setarea}) {
  let bounds = [[10, -10],[ 50, 50]];
  const pointsRef = useRef(null);  
  const areaRef = useRef(null);  
  const bboxArray = area? bbox(area) : bbox(points);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  const url = base_url + '/geoserver/geonode/wms';
  
  const setAreaStyle = ({ properties }) => {
    return {
      "color": "#ffff66'",
      "weight": 2,
      "fillOpacity": 0.1,
      "fillColor": "#ffff66"
    };
  };

  function AreaByLocation( typename, setArea ) {
    const [isWorking, setIsWorking] = useState(false)
    
    const getArea = async (pt) => {
      setIsWorking(true)
      try {
        const response = await ProfileService.getAreaByPoint(areasTN,pt);
        if ( response && response.ok && response.data ){
          setarea(response.data)
        }
      } catch (error) {
        console.log(error)
      }
      setIsWorking(false)   
    }

    const map = useMapEvents({
      click(e) {
        e.stopPropagation()
        if ( isWorking )
          return
        getArea(e.latlng)
      }
    })

    return !isWorking ? null : (
      <Loading title="Loading..."></Loading>
    )

  };

  function pointToLayer (feature, latlng) {
    if ( feature.properties && feature.properties.selected )
      return L.circleMarker(latlng, { radius: 8, fillColor: '#666666', color: '#ffff66', weight: 2, opacity: 1, fillOpacity: 0.3, } );
    return L.circleMarker(latlng, { radius: 8, fillColor: '#666666', color: '#6666ff', weight: 2, opacity: 1, fillOpacity: 0.3, });
  };

  let zoom = 7;
  
  return (
    <div className="Card flex flex-column gap-2">
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
      { url && areasTN && (
        <WMSTileLayer url={url} params={{format:"image/png", layers:{areasTN}, transparent: true}} />
      )}
      { area && (
        <GeoJSON
          ref={areaRef} 
          data={area}
          style={setAreaStyle}
        />
      )}
      { points && (
        <GeoJSON
          ref={pointsRef}
          data={points}
          pointToLayer={pointToLayer}
        />
      )}     
      </MapContainer>
    </div>  
  );
};
  