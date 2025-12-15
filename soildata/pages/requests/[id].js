<<<<<<< HEAD
import React, { useEffect, useState, useRef } from 'react';
import Loading from '../../components/Loading';
=======
import React, { useEffect } from 'react';
import Footer from '../../components/Footer';
import ToDo from '../../components/ToDo';
>>>>>>> 58dcde557d1da9070628851a32775b2507519611
import { useTranslations } from 'next-intl';
import { useUser } from '../../context/user';
import { useRouter } from 'next/router';
import { Panel } from 'primereact/panel';
import { Toast } from 'primereact/toast';
import dynamic from "next/dynamic"
import { RequestService } from '../../service/requests';
 
const MyMap = dynamic(() => import("../../components/RequestMap"), { ssr:false })

export default function Page() {
  const router = useRouter();
  const t = useTranslations('default');
  const user = useUser();
  const [prequest, setPrequest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [pointsGeoJSON, setPointsGeoJSON] = useState(null);
  const [aoiGeoJSON, setAoiGeoJSON] = useState(null);
  const [map, setMap] = useState(null);
  const toast = useRef(null);
  const statuses = [ "Created", "Elaborating", "Rejected", "Elaborated" ];

  useEffect(() => {
      if ( user.userData && user.userData.forbidden2 !== null && user.userData.forbidden2 )
          router.push(`/401`);
  },[user]);  // eslint-disable-line

  
  useEffect(() => {
/* 
  const _request = { 
    'id': router.query.id,  ///auto-increment
    'name': 'Request3',
    'user': 'enduser', 
    'date': new Date('2025/05/25'),
    'manager': 'datamanager',
    'data_type' : 'indicator', 
    'data_keys': 'pluto',
    'purpose' : 'purpose'
    'aoi': '{ "type": "Feature", "properties": { "id": null }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -6.024438810208561, 37.021985476287526 ], [ -6.021881710476406, 37.016871276823217 ], [ -5.975853915297635, 37.01516654366845 ], [ -5.939202152470095, 37.017723643400608 ], [ -5.876979392321015, 36.979367147418294 ], [ -5.867603359969785, 36.945272484322906 ], [ -5.85396549473163, 36.916292020691834 ], [ -5.844589462380399, 36.860888193161827 ], [ -5.863341527082861, 36.804631999054443 ], [ -5.923007187499786, 36.770537335959055 ], [ -5.999720179464406, 36.780765734887673 ], [ -6.087513936935025, 36.80377963247706 ], [ -6.18383136017949, 36.826793530066439 ], [ -6.217073656697492, 36.887311557060755 ], [ -6.191502659375953, 36.954648516674141 ], [ -6.168488761786567, 37.004085778162448 ], [ -6.142917764465027, 37.03136150863876 ], [ -6.104561268482718, 37.044999373876912 ], [ -6.082399737470717, 37.061194338847223 ], [ -6.077285538006409, 37.076536937240142 ], [ -6.038929042024099, 37.042442274144761 ], [ -6.028700643095483, 37.026247309174451 ], [ -6.024438810208561, 37.021985476287526 ] ] ] ] } }',
    'from': null,
    'to': new Date('2025/05/10'),
    'depth': 20,
    'status': one of [ "Created", "Assigned", "Rejected", "Elaborated", "Cancelled" ];
    'user_abort'

  - only data manager can delete Request
  - request can be created by Registered User ( only: id,name,user,date,data_type,data_key,aoi,depth,from,to,depth,purpose)
  - the registered user can update only user_abort 
*/
      const _request = { 
          id: router.query.id,
          name: 'Request3',
          user: 1004, 
          date: new Date('2025/05/25'),
          manager: 1001,
          data_type : 'pippo',
          data_keys: 'pluto',
          aoi: '{ "type": "Feature", "properties": { "id": null }, "geometry": { "type": "MultiPolygon", "coordinates": [ [ [ [ -6.024438810208561, 37.021985476287526 ], [ -6.021881710476406, 37.016871276823217 ], [ -5.975853915297635, 37.01516654366845 ], [ -5.939202152470095, 37.017723643400608 ], [ -5.876979392321015, 36.979367147418294 ], [ -5.867603359969785, 36.945272484322906 ], [ -5.85396549473163, 36.916292020691834 ], [ -5.844589462380399, 36.860888193161827 ], [ -5.863341527082861, 36.804631999054443 ], [ -5.923007187499786, 36.770537335959055 ], [ -5.999720179464406, 36.780765734887673 ], [ -6.087513936935025, 36.80377963247706 ], [ -6.18383136017949, 36.826793530066439 ], [ -6.217073656697492, 36.887311557060755 ], [ -6.191502659375953, 36.954648516674141 ], [ -6.168488761786567, 37.004085778162448 ], [ -6.142917764465027, 37.03136150863876 ], [ -6.104561268482718, 37.044999373876912 ], [ -6.082399737470717, 37.061194338847223 ], [ -6.077285538006409, 37.076536937240142 ], [ -6.038929042024099, 37.042442274144761 ], [ -6.028700643095483, 37.026247309174451 ], [ -6.024438810208561, 37.021985476287526 ] ] ] ] } }',
          data_from: null,
          data_to: new Date('2025/05/10'),
          depth: 20,
          status: RequestService.STATUSES.CREATED,
          user_abort : false
      }
      setPrequest ( _request )
      // fetch data!!!!!!
      if (Availability)
        setPointsGeoJSON(Availability);
      if (_request.aoi){ 
        const aoi = JSON.parse(_request.aoi);
        setAoiGeoJSON(aoi);
      }
      setLoading (false);

  },[]);  // eslint-disable-line

  useEffect(() => {
      const fetchMap = async () => {
        if ( pointsGeoJSON && aoiGeoJSON ) {
          const requestMap = {
            layers : [{
              points: pointsGeoJSON,
              style: { radius: 6, fillColor: '#6f6', color: '#2f2', weight: 2, opacity: 1, fillOpacity: 0.4, },
            },
            {
              polygon: aoiGeoJSON,
              style: { fillColor: '#66f', color: '#22f', weight: 2, opacity: 1, fillOpacity: 0.4, },
            }],
            label: 'RequestMap',
          }
          setMap(requestMap);
        }  
      }
      fetchMap();
  }, [pointsGeoJSON,aoiGeoJSON]); 

  if ( loading )
    return (   <div className="layout-dashboard"> <Loading /> </div> )
 
  if ( !prequest)
    return (   <div className="layout-dashboard"><h1> Not Found </h1></div> )

  return (
      <div className="layout-dashboard">
      <Toast ref={toast} />
      <div className="card">
        <h5>Data Request {router.query.id} </h5>
        <Panel header="Info" toggleable>
          <div>Blah,Blah,Blah</div>
          <div className="flex flex-column sm:flex-row my-2 w-full gap-3">
            <a href="doc/scheda_indicatorxxx.pdf" target="_blank" rel="noopener noreferrer" className="p-button font-bold">
              Indicator info
            </a>
          </div>
        </Panel>
        <h6>{ 'Name: ' + prequest.name + ' Date:' + prequest.date } blah blah</h6>
        {(map) && (    
          <div className="card">
            <h5>{ map ? map.label : 'Pre-Validation Map' }</h5>
            <MyMap data={map} />
          </div>

        )} 
      </div>
    </div>
  )
};

export async function getStaticPaths() {
  return {
    paths: [], //indicates that no page needs be created at build time
    fallback: 'blocking' //indicates the type of fallback
  }
}

export async function getStaticProps(context) {
  return {
    props: {
      messages: (await import(`../../translations/${context.locale}.json`)).default
     },
  }
}


