"use client"

import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic";
import { TreeTable } from 'primereact/treetable';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { TabView, TabPanel } from 'primereact/tabview';
import { Calendar } from 'primereact/calendar';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { Toast } from 'primereact/toast';
import { useUser } from '../../context/user';
import { Dialog } from 'primereact/dialog';
import { InputTextarea } from 'primereact/inputtextarea';
import { Galleria } from 'primereact/galleria';
import { Dropdown } from 'primereact/dropdown';
import { InputText } from 'primereact/inputtext';
import { TaxonomyService } from '../../service/taxonomies';
import { ProfileService } from '../../service/profiles';
import Mapping from '../../data/mapping';
import { Chart } from 'primereact/chart';
import * as munsell from 'munsell';

const MyMap = dynamic(() => import("../../components/PointMap"), { ssr:false })

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const id = router.query.id
  const user = useUser();
  const [loading, setLoading] = useState(false);
  const [pointData, setPointData] = useState(null);
  const [layersData, setLayersData] = useState(null);
  const [labData, setLabData] = useState(null);
  const [labExtData, setLabExtData] = useState(null);
  const [point, setPoint] = useState(null);
  const [layerColumns, setLayerColumns] = useState([]);
  const [layerNumber,setLayerNumber] = useState(0);
  const [horizonSequence,setHorizonSequence] = useState("");
  const [labDataColumns, setLabDataColumns] = useState([]); 
  const [topTabIndex, setTopTabIndex] = useState(0);
  const [expandedKeys1, setExpandedKeys1] = useState(null);
  const [expandedKeys2, setExpandedKeys2] = useState(null);
  const [visibleEdit, setVisibleEdit] = useState(false);
  const [visibleInfo, setVisibleInfo] = useState(false); 
  const toast = useRef(null);
  const [selected, setSelected] = useState(false);
  const [taxList, setTaxList] = useState(null);
  const [formValues, setFormValues] = useState(null);
  const [images, setImages] = useState(null);
  const [chartData, setChartData] = useState({});
  const [chartOptions, setChartOptions] = useState({});
  const [filled, setFilled] = useState(0);
  const [total, setTotal] = useState(0);
  
  

  useEffect(() => {
    if ( !user.userData || ( user.userData.forbidden !== null && user.userData.forbidden ))
        router.push(`/401`);
    const fetchData = ( async(id) => {
      try {
        setLoading(true);
        let mapping = Mapping['XLS_P:General and Surface'];
        let result = await generatePointTree ( mapping, id, false)
        let _total = result.total  
        let _filled = result.filled  
        setPointData(result.nodes);
        mapping = Mapping['XLS_P:Layer descriptions'];
        result = await generateLayerTree ( mapping, id, true)
        _total += result.total
        _filled += result.filled
        const _depths = result.depths
        const _colours = result.colours
        setLayersData(result.nodes);
        mapping = Mapping['XLS_P:Lab data'];
        result = await generateLabDataTree ( mapping, id, true)
        _total += result.total
        _filled += result.filled
        setLabData(result.data); 
        setFilled(_filled)
        setTotal(_total)     
        //const labextradataTree = generateLabExtraDataTree ( mapping, id, true)
        //setLabExtData(labextradataTree);
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
        const surfaceBorder = documentStyle.getPropertyValue('--surface-border');
        const datasets = []

        for ( let d = 1; d < _depths.length; d += 1 ) {
          let _v = _depths[d]
          if ( d > 1 ) 
            if (_v ) _v -= _depths[d-1]
            else _v = _depths[d-1]
          let colour = documentStyle.getPropertyValue('--secondaryy-' + (d*100) );
          if ( _colours[d-1] && _colours[d-1] !== '?' ) 
          {
            const c = munsell.munsellToRgb255(_colours[d-1]);
            if ( c && c[0] && c[1] && c[2] ) 
              colour = ['rgba('+c[0]+','+c[1]+','+c[2]+', 1)']
          }
          datasets.push( 
            {
              type: 'bar',
              label: 'layer ' + d,
              backgroundColor: colour,
              data: [_v]
            }
          )
        }
        const data = {
            labels: ['Layer\'s depth'],
            datasets: datasets
        };
        const options = {
            maintainAspectRatio: false,
            aspectRatio: 0.8,
            plugins: {
                tooltips: { mode: 'index', intersect: false },
                legend: { labels: { color: textColor  } }
            },
            scales: {
                x: { stacked: true, ticks: { color: textColorSecondary }, grid: { color: surfaceBorder } },
                y: { reverse: true, stacked: true, ticks: { color: textColorSecondary }, grid: { color: surfaceBorder  } }
            }
        };
        setChartData(data);
        setChartOptions(options);
        const _photos = await ProfileService.getPhotos(document.cookie, id);
        let _images = [];
        for ( let m = 1; m < _photos.length; m += 1) {
          if ( _photos[m].id ) {
            let alt = _photos[m].caption
            if ( !alt )
              alt = 'No description'
            let title = id + ': '
            if ( _photos[m].type )
              title += _photos[m].type
            _images.push ( {
                    image: '/documents/' + id +'/link',
                    alt: alt,
                    title: title
            })
          }
        }
      }  
      catch( error ) { 
        console.log(error)
      }
      setLoading(false); 
    })
    if (!pointData || !labData || !layersData ) 
      fetchData(id);
  },[user]);  // eslint-disable-line

  const resetSelectInfo = ( async(newData) => {
    setSelected(newData)
    setTaxList(null) 
    setVisibleInfo(true)
    if (newData && newData.taxonomy)  {
      try {
        const taxonomies = await TaxonomyService.listValues ( document.cookie, newData.taxonomy )
        if ( taxonomies && taxonomies.data )  {
          setTaxList(taxonomies.data);
        }
      }  
      catch( error ) { 
        console.log(error)
      }
    }
    else setTaxList([]);
  })

  const resetSelectEdit = ( async(newData) => {
    setSelected(newData)
    setFormValues(null);
    setVisibleEdit(true) 
    setTaxList([]) 
    if (newData && newData.taxonomy)  {
      try {
        const taxonomies = await TaxonomyService.listValues ( document.cookie, newData.taxonomy )
        if ( taxonomies && taxonomies.data ) 
          setTaxList(taxonomies.data);
        console.log(taxonomies.data)
      }  
      catch( error ) { 
         console.log(error)
      }
      
    } 
    let _values = {}
    const others = ["id", "name", "type", "taxonomy", "model", "descr", "ep"] 
    Object.keys(newData).forEach( function(key, index) {
      if ( !others.includes(key) ) {
        if ( key === 'value')  
          _values[newData['id']] = { id : newData['id'], value: newData[key] } 
        else _values[key] = { id : key , value: newData[key] } 
      }
    })
    setFormValues(_values);
  })

  async function generatePointTree ( mapping, id) {
    try {
      let _nodes = [];
      const models = {}
      const models_ep = {}
      let col_nr = 1;
      let col = null;
      while ( col = mapping[''+col_nr]) {
        if ( !models[col.m] ) {
          models[col.m] = {}
          models_ep[col.m] = col.ep  
        } 
        models[col.m][col.f] =  {
          name : col.f,
          value : null,
          type : col.check,
          taxonomy : col.t,
          model : col.m,
          descr : col.n,
          ep : col.ep,
          id : id
        }
        col_nr += 1;
      } 
      let _filled = 0
      let _total = 0
      let mod_keys = Object.keys(models);
      const main_resp = await ProfileService.get(document.cookie, id, 'point-generals');
      let main = main_resp.data;
      if ( main_resp && main_resp.data ) {
        Object.keys(main_resp.data).forEach(function(key, index) {
          if ( models[mod_keys[0]][key] && main_resp.data[key] ) { 
            let _v = main_resp.data[key];
            let _t = models[mod_keys[0]][key].type;
            if ( _t ) 
              if ( _t.startsWith('num') ) 
                _v = Number.parseFloat(_v).toFixed(6);
              else if ( _t.startsWith('tax') )
                _v = _v.substring( _v.indexOf(':') + 1 )
            models[mod_keys[0]][key].value = _v
            _filled += 1
          }
          _total += 1
        });
        let node = { key: 0, data: { name: mod_keys[0] }, icon: 'pi pi-fw pi-book', children : [] }
        Object.keys(models[mod_keys[0]]).forEach(function(key, index) {
            node.children.push(
              { key: '' + 0 + '-' + index,  data: models[mod_keys[0]][key], children : [] }
            )
        })
        _nodes.push(node)
        for ( let m = 1; m < mod_keys.length; m += 1) {
          let node = { key: m, data: { name: mod_keys[m] }, icon: 'pi pi-fw pi-book', children : [] }
          if ( main[mod_keys[m].toLowerCase()] ){
            const response = await ProfileService.get(document.cookie, id, models_ep[mod_keys[m]]);
            if ( response && response.data ) {
              Object.keys(response.data).forEach(function(key, index) {
                if ( models[mod_keys[m]][key] ) {
                  if (response.data[key] && models[mod_keys[m]][key] ) {
                    let _v = response.data[key]
                    let _t = models[mod_keys[m]][key].type 
                    if ( _t.startsWith('num') ) 
                      _v = Number.parseFloat(_v).toFixed(6);
                    else if ( _t.startsWith('tax') )
                      _v = _v.substring( _v.indexOf(':') + 1 )
                    models[mod_keys[m]][key].value = _v
                    _filled += 1;
                  }
                  _total += 1; 
                }
              });
            }
          }
          Object.keys(models[mod_keys[m]]).forEach(function(key, index) {
            if ( models[mod_keys[m]][key] && models[mod_keys[m]][key].value )
              node.children.push(
              { key: '' + m + '-' + index,  data: models[mod_keys[m]][key], children : [] }
              )
          })
          _nodes.push(node)  
        };
        if ( models['PointGeneral'].lat_wgs84 &&  models['PointGeneral'].lon_wgs84 ) {
          setPoint ( [models['PointGeneral']['lat_wgs84'].value, models['PointGeneral']['lon_wgs84'].value] )
        }
        if ( _nodes && _nodes.length > 0 )
          return { nodes : _nodes, filled: _filled, total: _total}     
      }     
    }  
    catch( error ) { 
      console.log(error)
    }
    return { nodes : [], filled: 0, total: 0} 
  }
  
  async function generateLayerTree ( mapping, id) {
    try {
      let resp = await ProfileService.getLayers(document.cookie, id);
      const ids = [];
      const colours = [];
      let layers = null;
      let _filled = 0;
      let _total = 0;
      const _columns = [];
      const depths = [];
      let h_s = "";
      if ( resp && resp.data && Array.isArray(resp.data) ) {
        layers = resp.data
        setLayerNumber(layers.length);
        for ( let ln = 0; ln < layers.length; ln+=1 ) {
          const name = layers[ln].id.substring(id.length+1);
          if ( ln > 0 ) 
            h_s += '_'
          if ( layers[ln].horizon )
            h_s += layers[ln].horizon;
          else h_s += '?'
          if ( layers[ln] && layers[ln].id ){
            ids.push(layers[ln].id)
            depths[layers[ln].number] = layers[ln].lower
            _columns.push({ f : layers[ln].id, h : 'Layer ' + name  })
          }
        }
      }
      setLayerColumns (_columns)
      setHorizonSequence (h_s)
      const models = {}
      const models_ep = {}
      let col_nr = 1;
      let col = null;
      const _nodes = []
      while ( col = mapping[''+col_nr]) {
        let mod = col.m
        if ( mod === 'LayerStructure' && col.lv ){
          mod += col.lv.substring(16)
        } 
        if ( !models[mod] ) {
          models[mod] = {}
          models_ep[mod] = col.ep  
        } 
        models[mod][col.f] =  {
          name : col.f,
          type : col.check,
          taxonomy : col.t,
          model : col.m,
          descr : col.n,
          ep : col.ep  
        }
        for ( let l = 0; l < ids.length; l+=1 ) {
          if ( layers[l] && layers[l].id )
            if ( mod === 'LayerMatrixColours' && col.f === 'munsell_m1' )
            {
              if ( layers[l][col.f] )
                colours[l] = layers[l][col.f]
            }
            if ( mod === 'PointLayer' && layers[l][col.f] )
            {
              let _v = layers[l][col.f]
              let _t = col.check
              if ( _t )
                if ( _t.startsWith('num') ) 
                  _v = Number.parseFloat(_v).toFixed(6);
                else if ( _t.startsWith('tax') )
                  _v = _v.substring( _v.indexOf(':') + 1 )
              models[mod][col.f][ids[l]] = _v
              _filled += 1;
            } 
            else 
              models[mod][col.f][ids[l]] = null
            _total += 1
        } 
        col_nr += 1;
      } 
      let mod_keys = Object.keys(models);
      
      for ( let m = 0; m < mod_keys.length; m += 1) {
        const _model = mod_keys[m]
        if ( _model ) {
          let node = { key: m, data: { name: mod_keys[m] }, icon: 'pi pi-fw pi-book', children : [] }
          for ( let l = 0; l < ids.length; l+=1 ) { 
            let _id = ids[l] 
            if ( !_model.startsWith('LayerStructure') ){
              if ( layers[l][mod_keys[m].toLowerCase()] ){
                const response = await ProfileService.get(document.cookie, _id, models_ep[_model]);
                if ( response && response.data ) {
                  Object.keys(response.data).forEach(function(key, index) {
                    if ( models[_model][key] ){
                      if (response.data[key] && models[_model][key].type ) {
                        let _v = response.data[key]
                        let _t = models[_model][key].type 
                        if ( _t.startsWith('num') ) 
                          _v = Number.parseFloat(_v).toFixed(6);
                        else if ( _t.startsWith('tax') ){
                          _v = _v.substring( _v.indexOf(':') + 1 )
                        }
                        models[_model][key][ids[l]] = _v
                        _filled += 1;
                      }
                      else models[_model][key][ids[l]] = null
                      _total += 1; 
                    }
                  });
                }
              }
            }
            else {
              const response = await ProfileService.getStructures(document.cookie, _id ) 
              if ( response && response.data && Array.isArray(response.data) ) { 
                for ( let st = 0; st < response.data.length; st+=1 ) {
                  let structure = response.data[st]
                  let st_id = 'LayerStructure' + structure.id.substring(17 + _id.length )
                  Object.keys(structure).forEach(function(key, index) {
                    if ( models[st_id][key] ){
                      if ( structure[key] && models[st_id][key].type ) {
                        let _v = structure[key]
                        let _t = models[st_id][key].type 
                        if ( _t.startsWith('num') ) 
                          _v = Number.parseFloat(_v).toFixed(6);
                        else if ( _t.startsWith('tax') )
                          _v = _v.substring( _v.indexOf(':') + 1 )
                        models[st_id][key][_id] = _v
                        _filled += 1;
                      }
                      else models[st_id][key][_id] = null
                      _total += 1;   
                    }
                  });
                }
              }
            }
          }
          Object.keys(models[_model]).forEach(function(key, index) {
            node.children.push(
              { key: '' + m + '-' + index,  data: models[_model][key], icon: null, children : [] }
            )
          })
          _nodes.push(node)
        }
        else console.log(ids)  
      }
      if ( _nodes && _nodes.length > 0 )
        return { nodes : _nodes, filled: _filled, total: _total}

    }  
    catch( error ) { 
      console.log(error)
    }
    return { nodes : [], filled: 0, total: 0, depths: depths, colours: colours} 
  }
  
  async function generateLabDataTree ( mapping, id) {
    try {      
      let resp = await ProfileService.getLabData(document.cookie, id);
      let ids = [];
      let _lab = null;
      let _filled = 0;
      let _total = 0;
      let _columns = []
      if ( resp && resp.data && Array.isArray(resp.data) ) {
        _lab = resp.data
        for ( let ln = 0; ln < _lab.length; ln+=1 ) {
          let name = null
          if ( _lab[ln] && _lab[ln].l_number ) 
            name = 'layer' + Number(_lab[ln].l_number).toFixed(0);
          else if ( _lab[ln] && _lab[ln].upper && _lab[ln].lower ) 
            name = _lab[ln].upper + 'cm|'+_lab[ln].lower + 'cm'
          if (name) {
            _columns.push({ f : name, h : name  })
            ids.push( name )
          }
        }
      }
      setLabDataColumns(_columns);
      let col_nr = 1;
      let col = null;
      let _data = []
      while ( col = mapping[''+col_nr]) {
        let row =  {
          name : col.f,
          type : col.check,
          taxonomy : col.t,
          model : col.m,
          descr : col.n,
          ep : col.ep 
        }
        for ( let ln = 0; ln < _lab.length; ln+=1 ) {
          if ( ids[ln] )
            if ( _lab[ln] && _lab[ln][col.f] ) {
              let _v = _lab[ln][col.f] 
              if (_v && col.check )
                if ( col.check.startsWith('num') ) 
                  _v = Number.parseFloat(_v).toFixed(6);
                else if ( col.check.startsWith('tax') )
                  _v = _v.substring( _v.indexOf(':') + 1 )
                if ( col.f === 'l_number' ) 
                  _v = Number.parseFloat(_v).toFixed(0);
              row[ids[ln]] = _v
              _filled += 1;
            }
            else row[ids[ln]] = null
            _total += 1;   
        }
        _data.push(row) 
        col_nr += 1;
      } 
      return { data : _data, filled: _filled, total: _total}     
    }  
    catch( error ) { 
      console.log(error)
    }
    return [];
  }
  
  async function  saveField (field) {
    console.log(field)
  }
 
  //      
  const actionTemplate = (rowData) => {
    return (
      <>
      {( rowData && ( !rowData.children || rowData.children.length === 0 )) && (
        <div className="flex flex-wrap gap-2">
          {( rowData.data && ( rowData.data.name !== 'id' && rowData.data.name !== 'point' ) ) && (
            <Button type="button" icon="pi pi-pencil" onClick={(e) => { resetSelectEdit(rowData.data); }} severity="success" rounded></Button>
          )}
           <Button type="button" icon="pi pi-question" onClick={(e) => { resetSelectInfo(rowData.data); }} rounded></Button>
          
        </div>
      )}
      </>
    )
  };

  const actionTemplate2 = (rowData) => {
    return (
      <>
      {( rowData ) && (
        <div className="flex flex-wrap gap-2">
          {( rowData.name !== 'point' ) && (
            <Button type="button" icon="pi pi-pencil" onClick={(e) => { resetSelectEdit(rowData); }} severity="success" rounded></Button>
          )}
          <Button type="button" icon="pi pi-question" onClick={(e) => { resetSelectInfo(rowData); }} rounded></Button>
        </div>
      )}
      </>
    )
  };

  const imageTemplate = (item) => {
    return <img src={item.image} alt={item.alt} style={{ width: '100%' }} />
  }

  const headerTemplate = () => {
    return (
      <h4 className="font-bold text-green-500">{t('EDIT_FIELD')}</h4>
    )
  };
  
  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      <Dialog 
        headerTemplate={headerTemplate}
        visible={visibleEdit} style={{ width: '50vw' }} 
        onHide={() => {if (!visibleEdit) return; setVisibleEdit(false);}} 
      >
                    
        <div className="card m-2">
          {( !formValues ) && (
            <h2>Loading values...</h2>
          )}
          {( formValues && Object.keys(formValues).length === 0 ) && (
            <h2>Errors reading values data...</h2>
          )}
          {( formValues && Object.keys(formValues).length > 0 ) && (
            <div className="flex w-full">
              <div className="flex-column">
                <div><h4 className="font-bold text-green-500">{t('SECTION')}: <span className="text-blue-500">{selected.model}</span> </h4></div>
                <div><h4 className="font-bold text-green-500">{t('FIELD')}: <span className="text-blue-500">{selected.name}</span></h4></div>
                <div className="flex flex-column gap-2">
                  <h4 className="font-bold text-green-500">{t('FIELD_VALUE')}: </h4>
                  {( selected.type === 'numeric(%)' || selected.type === 'numeric' ||  selected.type === 'latitude' ||  selected.type === 'longitude' ) && (
                    <>
                    { Object.keys(formValues).map((v) => (
                      <div key={v} className="flex flex-row gap-2">
                        <label htmlFor={v} className="font-bold text-blue-500" >{v}</label>
                        <InputText id={v} value={formValues[v].value} onChange={(e) => {formValues[v].value = e.target.value;console.log(e.target.value)}} keyfilter="num" placeholder="Number" />
                      </div>
                    ))}
                    </>
                  )}
                  {( selected.type === 'numeric(0)' ) && (
                    <>
                    { Object.keys(formValues).map((v) => (
                      <div key={v} className="flex flex-row gap-2">
                        <label htmlFor={v} className="font-bold text-blue-500" >{v}</label>
                        <InputText id={v} value={formValues[v].value} onChange={(e) => {formValues[v].value = e.target.value;console.log(e.target.value)}} keyfilter="pnum" placeholder="Number" />
                      </div>
                    ))}
                    </>
                  )}
                  {( selected.type === 'text' ) && (
                    <>
                    { Object.keys(formValues).map((v) => (
                      <div key={v} className="flex flex-row gap-2">
                        <label htmlFor={v} className="font-bold text-blue-500" >{v}</label>
                        <InputTextarea id={v} value={formValues[v].value} onChange={(e) => {formValues[v].value = e.target.value;console.log(e.target.value)}} rows={2} cols={30} />
                      </div>
                    ))}
                    </>
                  )}
                  {( selected.type === 'taxonomy' ) && (
                    <>
                    { Object.keys(formValues).map((v) => (
                      <div key={v} className="flex flex-row gap-2">
                        <label htmlFor={v} className="font-bold text-blue-500" >{v}</label>
                        <Dropdown id={v} value={formValues[v].value} onChange={(e) => { formValues[v].value = e.value;console.log(e.target.value)  }}
                          options={taxList}  optionValue="id" optionLabel="value"
                          placeholder="Select a class" className="w-full md:w-14rem" aria-describedby={v+'descr'}/>
                        <small id={v+'descr'}> {taxList.find((el) => el.id === formValues[v].value)?.descr}</small>
                      </div> 
                    ))}
                    </>
                  )}  
                  {( selected.type === 'boolean' ) && (
                    <>
                    { Object.keys(formValues).map((v) => (
                      <div key={v} className="flex flex-row gap-2">
                        <label htmlFor={v} className="font-bold text-blue-500" >{v}</label>
                        <Checkbox onChange={e => formValues[v].value = e.checked} checked={formValues[v].value}></Checkbox>
                      </div>  
                    ))}
                    </>
                  )}
                  {( selected.type === 'date' ) && (
                    <>
                    { Object.keys(formValues).map((v) => (
                      <div key={v} className="flex flex-row gap-2">
                        <label htmlFor={v} className="font-bold text-blue-500" >{v}</label>
                        <Calendar value={formValues[v].value} onChange={(e) => {formValues[v].value = e.value;console.log(e.target.value)}} />
                      </div>  
                    ))}
                    </>
                  )}
                  
                </div>
                <div className="flex flex-row m-2" >
                  <Button type="button" className="m-2" icon="pi pi-save" label={t('IMPORT_DATA')} onClick={(e) => saveField(selected) } severity="success" ></Button>
                  <Button type="button" className="m-2" icon="pi pi-times" label={t('CANCEL')} onClick={(e) => setVisibleEdit(false)}></Button>
                </div>
              </div>  
            </div>
          )}
        </div>
      </Dialog>
      <Dialog 
          visible={visibleInfo} style={{ width: '50vw' }} 
          onHide={() => {if (!visibleInfo) return; setVisibleInfo(false); }}>
        <div className="card m-2">
          {( !taxList ) && (
            <h4 className="font-bold">Loading values...</h4>
          )}
          {( taxList ) && (
          <div className="flex flex-column">
            <h4 className="font-bold"> {t('FIELD')}: {selected?.name} </h4>
            <h5> {selected?.descr} </h5>
            {( taxList.length > 0 ) && (
            <>  
              <h4>{t('VALUES')}:</h4>
              <DataTable value={taxList} className="mt-4" tableStyle={{ minWidth: '30rem' }} >
                <Column field="value" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} headerClassName="w-10rem"></Column>
                <Column field="descr" header={(<span className='text-xl font-bold'>{t('DESCR')}</span>)}></Column>
              </DataTable>
            </>
            )}
          </div>  
          )}  
        </div>
      </Dialog>
      {(!pointData && !loading ) && (
        <h4>No point soil data found</h4>
      )}
      {(loading) && (
        <h4>Loading point soil data...</h4>
      )}
      {(pointData && point) && (
      <>  
      <div className="grid">
        <div className="col-4 flex " >
          <div className="card w-full border-round flex flex-column" style={{ height: '450px' }}>
            <div><h5 className="font-bold text-green-500">{t('IDENTIFIER')}: <span className="text-blue-500">{id}</span> </h5></div>
            <div><h5 className="font-bold text-green-500">{t('LATITUDE')}: <span className="text-blue-500">{point[0]}</span></h5></div>
            <div><h5 className="font-bold text-green-500">{t('LONGITUDE')}: <span className="text-blue-500">{point[1]}</span></h5></div>
            <div><h5 className="font-bold text-green-500">{t('LAYER_NUMBER')}: <span className="text-blue-500">{layerNumber}</span></h5></div>
            <div><h5 className="font-bold text-green-500">{t('HORIZON_SEQUENCE')}: <span className="text-blue-500">{horizonSequence}</span></h5></div>
            {( total > 0 ) && ( 
              <div><h5 className="font-bold text-green-500">{t('TOTAL_FIELDS')}: <span className="text-blue-500">{total}</span></h5></div>
            )}
            {( filled > 0 ) && (
              <div><h5 className="font-bold text-green-500">{t('FILLED_FIELD')}: <span className="text-blue-500">{filled}</span></h5></div>
            )}
          </div>
        </div>
        <div className="col-4 flex">
          <div className="card w-full border-round" style={{ height: '450px' }}>
            {(chartData && chartOptions) && (
            <Chart type="bar" data={chartData} options={chartOptions} />
            )}
            {(!chartData || !chartOptions) && (
              <h2>Loading chart data...</h2>
            )}
          </div>  
        </div>
        <div className="col-4 flex">
          <div className="card w-full border-round" style={{ height: '450px' }}>
            <MyMap point={point} />
          </div>    
        </div>
      </div>
      <TabView activeIndex={topTabIndex} onTabChange={(e) => setTopTabIndex(e.index)}>
        <TabPanel header={(<span><i className="pi pi-book mr-2" />{t('POINT_GENERAL')}</span>)} >
          <div className="card">
            <TreeTable value={pointData} expandedKeys={expandedKeys1} onToggle={(e) => setExpandedKeys1(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
              <Column field="name" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} expander headerClassName="w-18rem"></Column>
              <Column field="type" header={(<span className='text-xl font-bold'>{t('TYPE')}</span>)}></Column>
              <Column field="value" header={(<span className='text-xl font-bold'>{t('VALUE')}</span>)}></Column>
              <Column body={actionTemplate} headerClassName="w-10rem" />
            </TreeTable>
          </div> 
        </TabPanel>
        <TabPanel header={(<span><i className="pi pi-book mr-2" />{t('POINT_LAYERS')}</span>)}>
          <div className="card">
            <TreeTable value={layersData} expandedKeys={expandedKeys2} onToggle={(e) => setExpandedKeys2(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
              <Column field="name" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} expander headerClassName="w-18rem"></Column>
              <Column field="type" header={(<span className='text-xl font-bold'>{t('TYPE')}</span>)}></Column>
              {layerColumns.map((col) => (
                <Column key={col.f} field={col.f} header={(<span className='text-xl font-bold'>{col.h}</span>)}></Column>
              ))}  
              <Column body={actionTemplate} headerClassName="w-10rem" />
            </TreeTable>
          </div>
        </TabPanel>
        <TabPanel header={(<span><i className="pi pi-book mr-2" />{t('POINT_LABDATA')}</span>)}>
          <div className="card">
            <DataTable value={labData} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
              <Column field="name" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} headerClassName="w-18rem"></Column>
              <Column field="type" header={(<span className='text-xl font-bold'>{t('TYPE')}</span>)}></Column>
              {labDataColumns.map((col) => (
                <Column key={col.f} field={col.f} header={(<span className='text-xl font-bold'>{col.h}</span>)}></Column>
              ))}  
              <Column body={actionTemplate2} headerClassName="w-10rem" />
            </DataTable>
          </div>
        </TabPanel>
        <TabPanel header={(<span><i className="pi pi-book mr-2" />{t('PHOTOS')}</span>)}>
          <div className="card">
            {(images && images.length > 0) && (
              <Galleria value={images} style={{ maxWidth: '640px' }} showThumbnails={false} showIndicators item={imageTemplate} />
            )}
            {(!images || images.length === 0) && (
              <h2>No photos</h2>
            )}   
          </div>
        </TabPanel>
      </TabView>
      </>
      )}
    </div> 
  );
};
  
export async function getStaticPaths() {
  return {
    paths: [],
    fallback: 'blocking',
  }
}

export async function getStaticProps(context) {
  return {
    props: { 
      messages: (await import(`../../translations/${context.locale}.json`)).default
    },
  }
}



