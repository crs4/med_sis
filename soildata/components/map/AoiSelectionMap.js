"use client"

import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, LayersControl, GeoJSON, WMSTileLayer, Pane } from 'react-leaflet';
import L from 'leaflet';
import { bbox, polygon } from '@turf/turf';
import 'leaflet-providers';
import "leaflet/dist/leaflet.css";
import '@geoman-io/leaflet-geoman-free';
import '@geoman-io/leaflet-geoman-free/dist/leaflet-geoman.css';
import './leaflet-extensions/mask/leaflet.mask';
import MapLegend from './legend';
import ProfileService from '../../service/profiles';
import Loading from '../Loading';

const GeomanControl = ({ toolbarRef, setByBox, setByPoint }) => {
  const map = useMap();
  const toolOptions = {
      position: 'topleft', 
      oneBlock: false,
      drawMarker: false,
      drawCircleMarker: true,
      drawPolyline: false,
      drawPolygon: false,
      drawCircle: false,
      drawText: false,
      editMode: false,
      dragMode: false,
      cutPolygon: false,
      removalMode: false,
      rotateMode: false,    
  }
  const geomanControl = L.Control.extend({
    options: {},
    initialize(options) {
      L.setOptions(this, options);
    },
    addTo(map) {
      map.setByBox = setByBox;
      map.setByPoint = setByPoint;
      map.pm.addControls({
        ...this.options,
      });
      map.pm.setGlobalOptions({ snappable: false });
      map.on('pm:drawstart', (e) => {
        map.pm.getGeomanDrawLayers(false).forEach(
          (geomanLayer) => {
            map.removeLayer(geomanLayer);
          }
        )
      })
      map.on('pm:create', async (e) => {
        map.pm.disableDraw();
        const geojson = e.layer.toGeoJSON();
        if ( geojson.geometry.type === 'Polygon' )
          await map.setByBox(geojson)  
        if ( geojson.geometry.type === 'Point' )
          await map.setByPoint(geojson) 
        map.pm.getGeomanDrawLayers(false).forEach(
          (geomanLayer) => {map.removeLayer(geomanLayer);})
      });
    }, 
  })
  
  const toolbar = function(opts) {
    return new geomanControl(opts);
  }

  useEffect(() => {
    if (!map || !map.pm || toolbarRef.current )
      return;
    toolbarRef.current = (toolbar(toolOptions)).addTo(map);
  }, [map, toolbarRef]); // eslint-disable-line 

  return null  
};

const AreaGeoJSON = ({ areaRef, data }) => {
  const map = useMap()
  
  // It defines the style of the Area Of Interest 
  const areaStyle = ({ properties }) => {
    return {
      "color": "#00aa00",
      "weight": 2,
      "fillOpacity": 0.6,
      "fillColor": "#00ff00",
    };
  };

  useEffect(() => {
    if (!map)
      return;
    if ( areaRef?.current ){
      map.removeLayer(areaRef.current)
    }
    if ( data ){
      areaRef.current = L.geoJSON(data, {
        style: areaStyle
      }).addTo(map);
    }
    else areaRef.current = null;
  }, [map, data, areaRef]);   // eslint-disable-line
  return null
};

const Mask = ({ maskRef, data }) => {
  const map = useMap();
  useEffect(() => {
    if (!map) 
      return;
    if ( maskRef.current )
      map.removeLayer(maskRef.current)
    if ( data )
      maskRef.current = L.mask(data, {
        map: map, fitBounds: true,
      }).addTo(map);
  }, [map, data, maskRef]); // eslint-disable-line
  return null  
};

// Map for AOI selection
export default function AoiSelectionMap ({
  points, /* Soil points data */
  area, /* Area of interest */
  token,
  areasTypeName, /*Areas dataset geoserver typename*/
  setByBox, /*function in ./ConfigureDataset.js*/ 
  setByPoint /*function in ./ConfigureDataset.js*/ }) 
{
  let bounds = [[10, -10],[ 50, 50]];
  const legend = useRef(null); 
  const mask = useRef(null); 
  const areasRef = useRef(null);  
  const pointsRef = useRef(null);  
  const aoiRef = useRef(null); 
  const [ fPoints, setFPoints ] = useState(points) 
  const [ aoi, setAoi ] = useState(area) 
  const [ typeName, setTypeName ] = useState(areasTypeName) 
  const bboxArray = area? bbox(area) : bbox(points);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  const url = process.env.NEXT_PUBLIC_GEOSERVER_BASE_URL + '/geonode/wms';
  
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

  // It defines the style of the points of the measure 
  function pointToLayer (feature, latlng) {
    return L.circleMarker(latlng, { radius: 8, fillColor: '#2a96f5', color: '#0805a2', weight: 2, opacity: 1, fillOpacity: 1 });
  };

  // default zoom
  let zoom = 7;

  useEffect(() => {
    setFPoints(points)
    setTypeName(areasTypeName)
    setAoi(area)
  }, [points,area,areasTypeName]); // eslint-disable-line
  
  return (
      <>
      <MapContainer
        doubleClickZoom={false}
        id='RoiSelector'
        zoom={zoom}
        bounds={bounds}
        style={{ height: '500px' }}
      > 
        <TileLayer
          url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
          attribution='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
        />
      { url && typeName && (
        <GeomanControl toolbarRef={toolbar} setByPoint={setByPoint} setByBox={setByBox} /> 
      )}
      { typeName && (
        <WMSTileLayer
          url={process.env.NEXT_PUBLIC_GEOSERVER_BASE_URL+"/geonode/wms"}
          params={{
            format:"image/png",
            layers:typeName,
            transparent: true,
            access_token: token,
          }}
        />
      )}
      <AreaGeoJSON
        areaRef={aoiRef}
        data={aoi}
      />
      <Mask maskRef={mask} data={aoi}/>
      { fPoints && (
        <GeoJSON
          key="points"
          ref={pointsRef}
          data={fPoints}
          pointToLayer={pointToLayer}
        />
      )}
        <MapLegend legend={legend} data={{aoiSelection: true}} position="bottomleft" />  
      </MapContainer>
      </> 
  );
};
  