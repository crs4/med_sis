"use client"

import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, useMap, LayersControl, GeoJSON, WMSTileLayer, Pane } from 'react-leaflet';
import L from 'leaflet';
import { bbox, polygon, featureCollection, feature, booleanPointInPolygon, booleanIntersects } from '@turf/turf';
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
        layers.push( L.geoJSON(area, {
          style: areaStyle
        }) )
      }
      if ( points ){
        layers.push( L.geoJSON(points, {
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
export default function AoiSelectionMap ({
  points, /* Soil points data */
  area, /* Area of interest */
  token,
  areasTypeName, /*Areas dataset geoserver typename*/
  setAoi /*set the Area of Interest*/
}) 
{
  let bounds = [[10, -10],[ 50, 50]];
  const legend = useRef(null); 
  const layersRef = useRef(null);  
  const [ fPoints, setFPoints ] = useState(null);
  
  const bboxArray = area? bbox(area) : bbox(points);
  bounds = [[bboxArray[1], bboxArray[0]], [bboxArray[3], bboxArray[2]]];
  const url = process.env.NEXT_PUBLIC_GEOSERVER_BASE_URL + '/geonode/wms';

  // It aggregates points to manage points with same position
  const aggregatePoints = async () => {
      const aggregateIndex = {}
      if ( !points || !points.features )
        return
      points.features.forEach( ft => {
        if ( ft.geometry.coordinates ){
          const key = ft.geometry.coordinates[0] + '_' + ft.geometry.coordinates[1] ;
          if ( ft.properties ) {
            if ( !aggregateIndex[key] )
              aggregateIndex[key] = { geometry: ft.geometry, points: [], values: [], lat : ft.geometry.coordinates[1], lon : ft.geometry.coordinates[0] }
            aggregateIndex[key].points.push(ft.properties.id)
            if ( ft.properties.value )
              aggregateIndex[key].values.push(""+ft.properties.value)
            else aggregateIndex[key].values.push("No data")
          }   
        }  
      });
      const aFeatures = [];
      Object.keys(aggregateIndex).forEach ((d) => {
        let panel = '<div class="flex flex-column justify-content-center text-cyan-500 font-bold">';
        const pdata = aggregateIndex[d];
        if ( pdata && pdata.geometry ) {
          const ft = feature (pdata.geometry)
          panel += '<div class="justify-content-center text-blue-500 font-bold">' + pdata.points.length + ' aggregated Points '
          panel += '<div>Latitude ' + pdata.lat + '</div>';
          panel += '<div>Longitude ' + pdata.lon + '</div>';
          panel += '<div>Values: '
          for ( let i = 0; i < pdata.points.length; i+=1 ) {
            panel += '<div>' + pdata.points[i]  ;
            if ( pdata.values.length > i )
              panel += '; Value ' + pdata.values[i]
            panel += '</div>'
          }  
          panel += '</div>'  
          ft.properties = { popup: panel } 
          aFeatures.push(ft)
        }
      });
      setFPoints( featureCollection(aFeatures) ) 
  };

  // This selects the AOI (polygonal or multipolygonal geometry) by providing a click location
  const setByPoint = async (pin) => {
    if ( !areasTypeName )
      return
    if ( !pin || !pin.geometry || !pin.geometry.coordinates || !pin.geometry.coordinates.length === 2 )
      return;
    const pt = pin.geometry.coordinates;
    const bboxFilter = 'bbox=' + pt[1] + ',' + pt[0] + ',' + pt[1] + ',' + pt[0];
    const p = null;
    const response = await ProfileService.getDataset( areasTypeName, bboxFilter, token )
    let features = [];
    if ( response && response.ok && response.data && response.data.features ){
      // verify data: wfs use bounding box
      const geojson = response.data
      console.log(geojson)
      if ( geojson.features ) {
        for ( let i = 0; i <  geojson.features.length; i+=1 )
          if ( booleanPointInPolygon(pin,geojson.features[i],))
            features.push(geojson.features[i])  
        if ( features.length > 0 ){
          console.log('ok')
          setAoi(featureCollection(features))
          return;
        }
      }
    }
    setAoi(null);
  }

  // This selects the AOI (polygonal or multipolygonal geometry) by quering catalogue using a box filter
  const setByBox = async (box) => {
    if ( !areasTypeName )
      return
    const bboxArray = bbox(box)
    const bboxFilter = 'bbox=' + bboxArray[1] + ',' + bboxArray[0] + ',' + bboxArray[3] + ',' + bboxArray[2];
    const response = await ProfileService.getDataset( areasTypeName, bboxFilter, token )
    let features = [];
    if ( response && response.ok && response.data && response.data.features ){
      // verify data
      const geojson = response.data
      if ( geojson.features ) {
        console.log(geojson)
        for ( let i = 0; i <  geojson.features.length; i+=1 )
          if ( booleanIntersects(box,geojson.features[i]))
            features.push(geojson.features[i])  
        if ( features.length > 0 ){
          console.log('ok')
          setAoi(featureCollection(features))
          return;
        }
      }
    }
    setAoi(null);
  }

  // default zoom
  let zoom = 7;

  useEffect(() => {
    aggregatePoints(points)
  }, [points]); // eslint-disable-line
  
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
      { url && areasTypeName && (
        <GeomanControl toolbarRef={toolbar} setByPoint={setByPoint} setByBox={setByBox} /> 
      )}
      { areasTypeName && (
        <WMSTileLayer
          url={process.env.NEXT_PUBLIC_GEOSERVER_BASE_URL+"/geonode/wms"}
          params={{
            format:"image/png",
            layers:areasTypeName,
            transparent: true,
            access_token: token,
          }}
        />
      )}
        <LayersGeoJSON
          layersRef={layersRef}
          area={area}
          points={fPoints}
        />
        <MapLegend legend={legend} data={{aoiSelection: true}} position="bottomleft" /> 
      </MapContainer>
      </> 
  );
};

// 