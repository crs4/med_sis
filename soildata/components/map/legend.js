"use client"
import L from 'leaflet';
import { useMap } from 'react-leaflet';
import { useEffect } from 'react';

const MapLegend = ({ legend, data, position }) => {
  const map = useMap();
 
  const renderLegend = (legend) => {
    console.log('render')
    console.log(legend)
    if (!legend.elements) {
        return;
    }
    const elements = legend.elements;
    const block = L.DomUtil.create('div', 'leaflet-control leaflet-bar leaflet-html-legend');
    
    if (legend.name) {
      const header = L.DomUtil.create('h4', null, block);
      L.DomUtil.create('div', 'legend-caret', header);
      L.DomUtil.create('span', null, header).innerHTML = legend.name;
      L.DomEvent.on(header, 'click', () => {
          if (L.DomUtil.hasClass(header, 'closed')) {
              L.DomUtil.removeClass(header, 'closed');
          }
          else {
              L.DomUtil.addClass(header, 'closed');
          }
      }, this);    
    }

    const elementContainer = L.DomUtil.create('div', 'legend-elements', block);
    
    for ( let e = 0; e < elements.length; e += 1 ) {
      console.log(elements[e])
      if ( elements[e] )
        addElement(elements[e].html, elements[e].label, elements[e].style, elementContainer);
    };
    return block;
  }

  const addElement = (html, label, style, container) => {
    const row = L.DomUtil.create('div', 'legend-row', container);
    const symbol = L.DomUtil.create('span', 'symbol', row);
    if (style) {
      Object.entries(style).forEach(([k, v]) => { symbol.style[k] = v; });
    }
    symbol.innerHTML = html;
    if (label) {
      L.DomUtil.create('label', null, row).innerHTML = label;
    }
  }
  
  useEffect(() => {
    if (!map  || !data || (legend && legend.current)) 
      return;
    const _legend = [];
    if ( data.pointsFilter )  {
      _legend = {
        name: "Points Filtering ",
        layer: null,
        opacity: 1,
        elements: [
          {
            label: 'Points Soil Data',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#3767ab',
              'width': '15px',
              'height': '15px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          },
          {
            label: 'Area of interest',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#00aa00',
              'width': '15px',
              'height': '15px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          }
        ]
      }
    }
    else if ( data.aoiSelection )  {
      _legend = {
        name: "Area of interest Selection ",
        layer: null,
        opacity: 1,
        elements: [
          {
            label: 'Points Soil Data',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#267bf3',
              'width': '15px',
              'height': '15px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          },
          {
            label: 'Areas',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#bb9a45',
              'width': '15px',
              'height': '15px',
              'position': 'relative',
              'margin': '3.75px 0',
            }
          },
          {
            label: 'Area of interest',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#00aa00',
              'width': '15px',
              'height': '15px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          }
        ]
      }
    }
    else if ( data.xlsUploads )  {
      _legend = {
        name: "Point Soil Data status ",
        layer: null,
        opacity: 1,
        elements: [{
            label: 'OK - profiles without errors',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#0805a2',
              'width': '20px',
              'height': '20px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          },
          {
            label: 'KO - profiles with errors',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#d0526c',
              'width': '20px',
              'height': '20px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          },
          {
            label: 'Warn - profiles with warnings',
            html: '',
            style: {
              'text-align': 'left',
              'background-color': '#777777',
              'width': '20px',
              'height': '20px',
              'position': 'relative',
              'margin': '3.75px 0',
            },
          }
        ]
      }
    }
    else if ( data.points )  {
      _legend = {
        name: "Point Soil Data",
        layer: null,
        opacity: 1,
        elements: [{
          label: 'Selected Point soil data',
          html: '',
          style: {
            'text-align': 'left',
            'background-color': '#0000aa',
            'width': '20px',
            'height': '20px',
            'position': 'relative',
            'margin': '3.75px 0',
          },
        },
        {
          label: 'Area of Interest',
          html: '',
          style: {
            'text-align': 'left',
            'background-color': '#00aa00',
            'width': '20px',
            'height': '20px',
            'position': 'relative',
            'margin': '3.75px 0',
          },
        }]
      }
    }
    else return;
    legend.current = L.control({position: position});
    legend.current.myleg = _legend
    legend.current.onAdd = function (map) {
      this._div = renderLegend(this.myleg); 
      return this._div;
    }  
    legend.current.addTo(map);  
  }, [map, legend]); // eslint-disable-line      
  return null  
}; 

export default MapLegend;