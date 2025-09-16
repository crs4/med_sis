import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css"
import { bbox } from '@turf/turf';
import './leaflet-extensions/htmllegend/L.Control.HtmlLegend';
import { GeoJSON } from 'react-leaflet/GeoJSON';

const Selection =  ({ selRef, element }) => {
  const map = useMap();
  if (!map)
    return
  if ( selRef.current )
    map.removeLayer(selRef.current)
  let alt = "No Data" 
  if (element.elev_m_asl)
    alt = element.elev_m_asln.toFixed(0)

  selRef.current = L.circleMarker([element.lat_wgs84, element.lon_wgs84], 
        { radius: 10, fillColor: '#f0f008ff', color: '#d18c1dff', weight: 3, opacity: 1, fillOpacity: 1}
  ).bindPopup(
    "<div class='flex flex-wrap  font-bold justify-content-center'>" + 
    "<span class='text-cyan-500 align-items-center' >Identifier:</span><span>" + element.id + "</span></div>" +
    "<div><span class='text-green-500'> Location: </span><span>" + element.location + "</span></div>" +
    "<div><span class='text-green-500'> Latitude: </span><span>" + element.lat_wgs84 + "</span></div>" +
    "<div><span class='text-green-500'> Longitude: </span><span>" + element.lon_wgs84 + "</span></div>" +
    "<div><span class='text-green-500'> Altitude (ASL):</span><span>"+ alt + "</span></div>" ).addTo(map)
  map.flyTo([element.lat_wgs84, element.lon_wgs84]);
}

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
              label: 'Selected profile',
              html: '',
              style: {
                'text-align': 'left',
                'background-color': '#f0f008ff',
                'width': '20px',
                'height': '20px',
                'position': 'relative',
                'margin': '3.75px 0',
              },
            },
            {
              label: 'Profile',
              html: '',
              style: {
                'text-align': 'left',
                'background-color': '#8b6b9fff',
                'width': '20px',
                'height': '20px',
                'position': 'relative',
                'margin': '3.75px 0',
              },
            },
            ],
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

export default function S4Mmap ({data, selected}) {
  const layerJSON = useRef(null); // eslint-disable-line
  const controlLegend = useRef(null); // eslint-disable-line
  const controllSelection = useRef(null); // eslint-disable-line
  const points = data.layer.points;
  const bboxArray = bbox(points);
  let bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  let zoom = 7;  

  function pointToLayer (feature, latlng) {
    let style = { radius: 8, fillColor: '#8b6b9fff', color: '#533aabff', weight: 2, opacity: 1, fillOpacity: 0.8}
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
        {selected && (
          <Selection selRef={controllSelection} element={selected}/>
        )}
      </MapContainer>
    </>  
  );
};


        