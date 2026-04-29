"use client"

import React, { useState, useEffect, useRef } from 'react';
import { useTranslations } from 'next-intl';
import { useRouter } from 'next/router';
import dynamic from "next/dynamic";
import { TreeTable } from 'primereact/treetable';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Card } from 'primereact/card';
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
import Loading from '../../components/Loading';
import Mapping from '../../data/mapping';
import { Chart } from 'primereact/chart';
import * as munsell from 'munsell';

const MyMap = dynamic(() => import("../../components/PointMap"), { ssr:false })

export default function Page()  {
  const router = useRouter();
  const t = useTranslations('default');
  const id = router.query.id
  const user = useUser();
  const toast = useRef(null);
  
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(false);

  const [pointData, setPointData] = useState(null);
  const [layersData, setLayersData] = useState(null);
  const [labData, setLabData] = useState(null);
  const [labExtData, setLabExtData] = useState(null);
  const [images, setImages] = useState(null);
  const [isMonitoring, setIsMonitoring] = useState(false);
  
  const [point, setPoint] = useState(null);
  const [horizonSequence,setHorizonSequence] = useState("");
  const [colours,setColours] = useState([]);
  const [layerNumber,setLayerNumber] = useState(0);
  const [chartData, setChartData] = useState({});
  const [chartOptions, setChartOptions] = useState({});
  const [filled, setFilled] = useState(0);
  const [total, setTotal] = useState(0);
  
  const [layerColumns, setLayerColumns] = useState([]);
  const [labDataColumns, setLabDataColumns] = useState([]); 
  const [topTabIndex, setTopTabIndex] = useState(0);
  const [expandedKeys1, setExpandedKeys1] = useState(null);
  const [expandedKeys2, setExpandedKeys2] = useState(null);
  const [visibleInfo, setVisibleInfo] = useState(false); 
  const [visibleEdit, setVisibleEdit] = useState(false);
  
  const [taxList, setTaxList] = useState(null);
  const [formValues, setFormValues] = useState(null);
  const [selected, setSelected] = useState(null);
  const [selectedId, setSelectedId] = useState(null);
  const [selectedValue, setSelectedValue] = useState(null);
  
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
        setColours(_colours)
        setLayersData(result.nodes);
        mapping = Mapping['XLS_P:Lab data'];
        result = await generateLabDataTree ( mapping, id, true)
        _total += result.total
        _filled += result.filled
        setLabData(result.data); 
        setFilled(_filled)
        setTotal(_total)     
        const response = await ProfileService.getExtraLabData(document.cookie, id);
        if ( response && response.ok && response.data)
          setLabExtData(response.data);
        const documentStyle = getComputedStyle(document.documentElement);
        const textColor = documentStyle.getPropertyValue('--text-color');
        const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
        const surfaceBorder = documentStyle.getPropertyValue('--surface-border');
        const datasets = [];
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
                    image: '/documents/' + _photos[m].id +'/link',
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
    if (!pointData || !labData || !layersData || !labExtData ) 
      fetchData(id);
  },[user]);  // eslint-disable-line

  const resetInfo = ( async(newData) => {
    setSelected(newData)
    setTaxList(null) 
    setVisibleInfo(true)
    if ( newData && newData.data && newData.data.taxonomy)  {
      try {
        const taxonomies = await TaxonomyService.listValues ( document.cookie, newData.data.taxonomy )
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

  const resetEdit = ( async(newData) => {
    setSelected(newData)
    setFormValues(null);
    setSelectedValue(null);
    setSelectedId(null);
    setTaxList([]) 
    if ( newData && newData.data )
    {
      if ( newData.data.taxonomy )  
      {
        try {
          const taxonomies = await TaxonomyService.listValues ( document.cookie, newData.data.taxonomy )
          if ( taxonomies && taxonomies.data ) 
            setTaxList(taxonomies.data);
        }  
        catch( error ) { 
           console.log(error)
        }
      } 
      let _values = {}
      const others = ["id", "name", "type", "taxonomy", "model", "descr", "ep"] 
      Object.keys(newData.data).forEach( function(key, index) {
        if ( !others.includes(key) ) {
          if ( key === 'value')  
            _values[newData.data['id']] = { id : newData.data['id'], value: newData.data[key] } 
          else _values[key] = { id : key , value: newData.data[key] } 
        }
      })
      setFormValues(_values);
      if ( Object.keys(_values).length === 1 )
      {
        setSelectedId(newData.data['id'])
        setSelectedValue(newData.data['value'])
      }
      setVisibleEdit(true)
    }
    else setVisibleEdit(false); 
  })

  async function generatePointTree ( mapping, pid) {
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
          id : pid
        }
        col_nr += 1;
      } 
      let _filled = 0
      let _total = 0
      let mod_keys = Object.keys(models);
      const main_resp = await ProfileService.get(document.cookie, pid, 'point-generals');
      if ( main_resp && main_resp.data ) {
        let main = main_resp.data;
        Object.keys(main).forEach(
          function(key, index) {
            if ( models[mod_keys[0]][key] && main[key] ) 
            { 
              let _v = main[key];
              let _t = models[mod_keys[0]][key].type;
              if ( _t ) 
                if ( key === 'lat_wgs84' || key === 'lon_wgs84' ) 
                  _v = Number.parseFloat(_v).toFixed(6);
                if ( key === 'type' ) 
                  setIsMonitoring( _v !== 'POINT_DATA_TYPES:P' );
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
            const response = await ProfileService.get(document.cookie, pid, models_ep[mod_keys[m]]);
            if ( response && response.data ) {
              Object.keys(response.data).forEach(
                function(key, index) {
                  if ( models[mod_keys[m]][key] ) {
                    if (response.data[key] && models[mod_keys[m]][key] ) 
                    {
                      let _v = response.data[key]
                      let _t = models[mod_keys[m]][key].type 
                      if ( _t.startsWith('tax') )
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
            if ( models[mod_keys[m]][key] )
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
  
  async function generateLayerTree ( mapping, pid) {
    try {
      let resp = await ProfileService.getLayers(document.cookie, pid);
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
          if ( layers[l] && layers[l].id ){
            if ( mod === 'PointLayer' && layers[l][col.f] )
            {
              let _v = layers[l][col.f]
              let _t = col.check
              if ( _t )
                if ( _t.startsWith('tax') )
                  _v = _v.substring( _v.indexOf(':') + 1 )
              models[mod][col.f][ids[l]] = _v
              _filled += 1;
            } 
            else 
              models[mod][col.f][ids[l]] = null
            _total += 1;
          } 
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
                if ( response && response.data ) 
                {
                  Object.keys(response.data).forEach( function(key, index) {
                    if ( models[_model][key] )
                    {
                      if ( _model === 'LayerMatrixColours' && key === 'munsell_m1' && response.data[key])
                      {
                        if ( response.data[key] )
                          colours.push(response.data[key])
                        else colours.push('no data') 
                      }
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
                      else 
                        models[_model][key][ids[l]] = null
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
      }
      if ( _nodes && _nodes.length > 0 )
        return { nodes : _nodes, filled: _filled, total: _total, depths: depths, colours: colours}

    }  
    catch( error ) { 
      console.log(error)
    }
    return { nodes : [], filled: 0, total: 0, depths: [], colours: []} 
  }
  
  async function generateLabDataTree ( mapping, pid) {
    try {      
      let resp = await ProfileService.getLabData(document.cookie, pid);
      let ids = [];
      let _lab = null;
      let _filled = 0;
      let _total = 0;
      let _columns = []
      if ( resp && resp.data && Array.isArray(resp.data) ) {
        _lab = resp.data
        for ( let ln = 0; ln < _lab.length; ln+=1 ) {
          let name = _lab[ln].id
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
                if ( col.check.startsWith('tax') )
                  _v = _v.substring( _v.indexOf(':') + 1 )
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

  async function generateExtraLabDataTree ( mapping, pid) {  
    return [];
  }
  
  async function  saveField () {
    setVisibleEdit(false)
    if ( !selectedId || !selectedValue )
      return null;
    if ( selected && selected.data )
    try {
      const fielddObj =  { };
      fielddObj[selected.data.name] = selectedValue;
      const response = await ProfileService.update( document.cookie, selectedId, fielddObj, selected.data.ep);
      const nvalue = selectedValue;
      if ( selected.data.taxonomy )
        nvalue = selectedValue.substring(selectedValue.lastIndexOf(':'))
      if ( selected.data.id && selected.key )
      { 
        const data = pointData.slice();
        const section = selected.key.charAt(0);
        (data[section].children.find((el) => el.key === selected.key)).data['value'] = nvalue;
        setPointData(data)
      }
      else if ( selected.key )
      { 
        const data = layersData.slice();
        const section = selected.key.charAt(0);
        (data[section].children.find((el) => el.key === selected.key)).data[selectedId] = nvalue;
        setLayersData(data)
      }
      else 
      {
        const data = labData.slice();
        (data.find((el) => el.field === selected.data.field)).data[selectedId] = nvalue;
        setLabData(data)
      }
      if ( !response || !response.ok ) 
        toast.current.show({severity:'error', summary: 'Errors!', detail: 'Errors saving field data', life: 3000});
      else toast.current.show({severity:'success', summary: 'Success!', detail: 'Success, field saved!' , life: 3000});
    }  
    catch( error ) { 
        console.log(error)
    }  
  }

  const changeLayer = ( (layerName) => {
    setSelectedId(layerName)
    if ( formValues && layerName )
      setSelectedValue( formValues[layerName]?.value ) ;
  })
 
  //      
  const actionTemplate = (rowData) => {
    return (
      <>
      {( rowData && ( !rowData.children || rowData.children.length === 0 )) && (
        <div className="flex flex-wrap gap-2">
          {( rowData.data && ( rowData.data.name !== 'id' && rowData.data.name !== 'point' ) ) && (
            <Button type="button" icon="pi pi-pencil" onClick={(e) => { resetEdit(rowData); }} severity="success" rounded></Button>
          )}
           <Button type="button" icon="pi pi-question" onClick={(e) => { resetInfo(rowData.data); }} rounded></Button> 
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
            <Button type="button" icon="pi pi-pencil" onClick={(e) => { resetEdit(rowData); }} severity="success" rounded></Button>
          )}
          <Button type="button" icon="pi pi-question" onClick={(e) => { resetInfo(rowData); }} rounded></Button>
        </div>
      )}
      </>
    )
  };

  const actionTemplate3 = (rowData) => {
    return (
      <>
      {( rowData ) && (
        <div className="flex flex-wrap gap-2">
          <Button type="button" icon="pi pi-plus" onClick={(e) => { }} severity="danger" rounded></Button>
        </div>
      )}
      </>
    )
  };

  const imageTemplate = (item) => {
    return <img src={item.image} alt={item.alt} style={{ width: '100%' }} />
  }

  const noDataTemplate = () => {
    return <h6> No data found </h6>
  }

  const headerTemplate1 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }} >FIELD EDITING</h4>
  };
  
  const headerTemplate2 = () => {
    return  <h4 className="font-bold shadow-1 p-3 bg-cyan-900 text-white" style={{ width: '90%' }}> FIELD DESCRIPTION</h4>
  };
  
  const className1 = 'col-6 font-bold text-cyan-800 mt-1 mb-1';
  const className2 = 'col-6 text-green-800 mt-1 mb-1';

  return (
    <div className="layout-dashboard">
      <Toast ref={toast} /> 
      <Dialog  header={headerTemplate1} visible={visibleEdit} style={{ width: '50vw' }} onHide={() => { resetEdit() }} className="surface-200" > 
        { selected && selected.data && (                   
        <div className="text-cyan-800 w-full">
          {( !formValues ) && (
            <h5>Loading values...</h5>
          )}
          {( formValues && Object.keys(formValues).length === 0 ) && (
            <h5>Errors loading data...</h5>
          )}
          {( formValues && Object.keys(formValues).length > 0 ) && (
            <div className="card w-full justify-content-center">
            {( Object.keys(formValues).length > 1 ) && (
              <Dropdown value={selectedId} placeholder="Select a layer" className="w-14rem m-2"
                onChange={(e) => {changeLayer(e.value)}} options={Object.keys(formValues)}/>
            )}
            { selectedId && (
              <>  
              <div className="flex w-full flex-column text-cyan-800 gap-2 m-3 p-3">
                <span className="font-bold text-xl block">{selected.data.name}</span>
                <span className="font-italic">{selected.data.descr}:</span>
                {( selected.data.type === 'numeric(%)' || selected.data.type === 'numeric' ||  selected.data.type === 'latitude' ||  selected.data.type === 'longitude' ) && (
                  <InputText id="inputValue" value={selectedValue} onChange={(e) => {setSelectedValue(e.target.value)}} keyfilter="num" placeholder="Insert a value" />
                )}
                {( selected.data.type === 'numeric(0)' ) && (
                  <InputText id="inputValue" value={selectedValue} onChange={(e) => {setSelectedValue(e.target.value)}} keyfilter="pnum" placeholder="Insert a value" />
                )}
                {( selected.data.type === 'text' ) && (
                  <InputTextarea id="inputValue" value={selectedValue} onChange={(e) => {setSelectedValue(e.target.value)}} rows={2} cols={30} />
                )}
                {( selected.data.type === 'taxonomy' ) && (
                <>
                  <Dropdown id="inputValue" value={selectedValue}  onChange={(e) => { setSelectedValue(e.value) }}
                      options={taxList}  optionValue="id" optionLabel="value"
                      placeholder="Select a class" className="w-full md:w-14rem" aria-describedby='descr'/>
                  <small id={'descr'}> {taxList.find((el) => el.id === selectedValue)?.descr}</small>
                </>
                )}
                {( selected.data.type === 'boolean' ) && (
                  <Checkbox id="inputValue" onChange={(e) => { setSelectedValue(e.checked) }} checked={selectedValue}></Checkbox>
                )}
                {( selected.data.type === 'date' ) && (
                  <Calendar id="inputValue" value={selectedValue} onChange={(e) => {setSelectedValue(e.value)}} />
                )}
              </div>
              <div className="flex flex-row m-2 justify-content-center" >
              <Button type="button" className="m-2" icon="pi pi-save" label={t('IMPORT_DATA')} onClick={(e) => saveField() } severity="success" ></Button>
              <Button type="button" className="m-2" icon="pi pi-times" label={t('CANCEL')} onClick={(e) => resetEdit() }></Button>
              </div>
              </>
            )}
            </div>             
          )}  
        </div>
        )}
      </Dialog>
      <Dialog  header={headerTemplate2} visible={visibleInfo} style={{ width: '50vw' }} 
        onHide={() => {if (!visibleInfo) return; setVisibleInfo(false); }} className="surface-200">
        { selected && (  
        <div className="card grid text-cyan-800 w-full">
          <h5 className={className1}> SECTION: </h5>
          <h5 className={className2}> {selected.data?.model} </h5>
          <h5 className={className1}> FIELD NAME: </h5>
          <h5 className={className2}> {selected.data?.name} </h5>
          <h5 className={className1}> DESCRIPTION: </h5>
          <h5 className={className2}> {selected.data?.descr} </h5>
          <h5 className={className1}> TYPE: </h5>
          <h5 className={className2}> {selected.data?.type} </h5>
        
        {( taxList && taxList.length > 0 ) && (
        <>  
          <h5 className="col-12 font-bold text-cyan-800 mt-1 mb-1">VALUES:</h5>
          <DataTable value={taxList} className="ml-5 col-12 mt-1" tableStyle={{ minWidth: '30rem' }} >
            <Column field="value" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} headerClassName="w-10rem"></Column>
            <Column field="descr" header={(<span className='text-xl font-bold'>{t('DESCR')}</span>)}></Column>
          </DataTable>
        </>
        )} 
        </div>
        )}
      </Dialog>
      <h5 className="w-full font-bold text-cyan-800 p-3 mb-3 shadow-2">POINT SOIL DATA: <span className="font-bold text-green-800">{id}</span></h5>
      <Card className="text-cyan-800 flex w-full">
        {(loading) && ( <Loading  title="loading data..." /> )}
        {(!pointData && !loading) && ( <span class="font-bold text-cyan-800">point data not found</span> )} 
        {(pointData && point && !loading) && (
        <>  
        <div className="grid">
          <div className="col-4 flex">
            <div className="card w-full border-round flex flex-column text-cyan-800 justify-content-center font-bold" style={{  height: '450px' }}>
              <div className="grid text-xl">
                <h6 className={className1}>{t('IDENTIFIER')}:</h6> <h6 className={className2}>{id}</h6>
                <h6 className={className1}>{t('LATITUDE')}:</h6> <h6 className={className2}>{point[0]}</h6>
                <h6 className={className1}>{t('LONGITUDE')}:</h6> <h6 className={className2}>{point[1]}</h6>
                <h6 className={className1}>{t('LAYER_NUMBER')}:</h6> <h6 className={className2}>{layerNumber}</h6>
                <h6 className={className1}>{t('HORIZON_SEQUENCE')}:</h6> <h6 className={className2}>{horizonSequence}</h6>
                {( total > 0 ) && (
                <>   
                <h6 className={className1}>{t('TOTAL_FIELDS')}:</h6><h6 className={className2}>{total}</h6>
                </>
                )}
                {( filled > 0 ) && (
                <>
                <h6 className={className1}>{t('FILLED_FIELD')}:</h6> <h6 className={className2}>{filled}</h6>
                </>
                )}
                <h6 className={className1}>Munsell Colours:</h6>
                <h6 className={className2}>
                { colours.map((v, i) => (
                <>
                <div key={v}>Layer {i+1}: &apos;{v}&apos;</div>
                </>
                ))}
                </h6>
              </div>    
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
          <TabPanel header={(<span><i className="pi pi-book mr-2" />GENERAL INFO</span>)} >
            <div className="card">
              <TreeTable value={pointData} expandedKeys={expandedKeys1} onToggle={(e) => setExpandedKeys1(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
                <Column field="name" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} expander ></Column>
                <Column field="type" header={(<span className='text-xl font-bold'>{t('TYPE')}</span>)}></Column>
                <Column field="value" header={(<span className='text-xl font-bold'>{t('VALUE')}</span>)}></Column>
                <Column body={actionTemplate} headerClassName="w-10rem" />
              </TreeTable>
            </div> 
          </TabPanel>
          <TabPanel header={(<span><i className="pi pi-book mr-2" />LAYERS DESCRIPTION</span>)}>
            <div className="card">
              <TreeTable value={layersData} expandedKeys={expandedKeys2} onToggle={(e) => setExpandedKeys2(e.value)} className="mt-4" tableStyle={{ minWidth: '50rem' }}>
                <Column field="name" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)} expander></Column>
                <Column field="type" header={(<span className='text-xl font-bold'>{t('TYPE')}</span>)}></Column>
                {layerColumns.map((col) => (
                  <Column key={col.f} field={col.f} header={(<span className='text-xl font-bold'>{col.h}</span>)}></Column>
                ))}  
                <Column body={actionTemplate} headerClassName="w-10rem" />
              </TreeTable>
            </div>
          </TabPanel>
          <TabPanel header={(<span><i className="pi pi-book mr-2" />LABORATORY DATA</span>)}>
            <div className="card">
              <DataTable value={labData} className="mt-4" tableStyle={{ minWidth: '50rem' }} emptyMessage={noDataTemplate}>
                <Column field="name" header={(<span className='text-xl font-bold'>{t('NAME')}</span>)}></Column>
                <Column field="type" header={(<span className='text-xl font-bold'>{t('TYPE')}</span>)}></Column>
                {labDataColumns.map((col) => (
                  <Column key={col.f} field={col.f} header={(<span className='text-xl font-bold'>{col.h}</span>)}></Column>
                ))}  
                <Column body={actionTemplate2} headerClassName="w-10rem" />
              </DataTable>
            </div>
          </TabPanel>
          <TabPanel header={(<span><i className="pi pi-book mr-2" />EXTRA LABORATORY DATA</span>)}>
            <div className="card">
              <DataTable value={labExtData} paginator dataKey="id" className="mt-4" tableStyle={{ minWidth: '50rem' }}
                   rows={20} responsiveLayout="scroll" emptyMessage={noDataTemplate}>
                <Column header="Id" sortable field="id" style={{ minWidth: '8rem' }} />
                <Column header="Point" sortable field="point" style={{ minWidth: '8rem' }} />
                <Column header="LabData" sortable field="labdata" style={{ minWidth: '8rem' }} />
                <Column header="Measure" sortable field="measure" style={{ minWidth: '8rem' }} />
                <Column header="Method" sortable field="method" style={{ minWidth: '8rem' }} />
                <Column header="Unit" sortable field="unit" style={{ minWidth: '8rem' }} />
                <Column header="Value" sortable field="value" style={{ minWidth: '8rem' }} />
                <Column header="Actions" frozen body={actionTemplate3} style={{ minWidth: '6rem' }} />
              </DataTable>
            </div>
          </TabPanel>
          <TabPanel header={(<span><i className="pi pi-book mr-2" />PHOTOS</span>)}>
            <div className="card">
              {(images && images.length > 0) && (
                <Galleria value={images} style={{ maxWidth: '640px' }} showThumbnails={false} showIndicators item={imageTemplate} />
              )}
              {(!images || images.length === 0) && (
                <h6> No data found </h6>
              )}   
            </div>
          </TabPanel>
        </TabView>
        </>
        )}
      </Card>
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



