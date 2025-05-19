
export const SampleService = {
  
  
  GENERAL_SECTIONS : [
    {  label : 'General', parts: ['8.2.1','8.2.2','Notes'],},
    {  label : 'Landform&Topography', parts: ['8.2.3'],},
    {  label : 'Climate&Weather', parts: ['8.2.4'], others:[]},
    {  label : "Land Use", parts: ['8.2.5',], others:[]},
    {  label : "Surface", parts: ['8.3.2','8.3.3','8.3.4','8.3.5','8.3.6','8.3.7','8.3.8','8.3.9','8.3.10','8.3.12'],},
    {  label : "Surface Unevenness", parts: ['8.3.11'],}
  ],

  LAYER_SECTIONS : [
    {  label : 'Identification', parts: ['8.4.1','8.4.2','8.4.3','8.4.4','8.4.5','8.4.6','8.4.9','8.4.21','8.4.22','8.4.28','8.4.29','8.4.32','8.4.33','8.4.40','Notes'],},
    {  label : 'Coarse Fragments', parts: ['8.4.7'],},
    {  label : 'Artefacts', parts: ['8.4.8'],},
    {  label : "Land Structure", parts: ['8.4.10','8.4.12','8.4.13','8.4.14',],},
    {  label : "Colours", parts: ['8.4.17','8.4.18','8.4.19','8.4.20',],},
    {  label : "Coatings and Bridges", parts: ['8.4.23'],},
    {  label : "Ribbonlike Accumulations", parts: ['8.4.24'],},
    {  label : "Carbonates", parts: ['8.4.25'],},
    {  label : "Gypsum", parts: ['8.4.26'],},
    {  label : "Secondary Silica", parts: ['8.4.27'],},
    {  label : "Consistence", parts: ['8.4.30'],},
    {  label : "Surface Crust", parts: ['8.4.31'],},
    {  label : "Permafrost", parts: ['8.4.34'],},
    {  label : "Soil Organic Carbon", parts: ['8.4.36'],},
    {  label : "Roots", parts: ['8.4.37'],},
    {  label : "Animal Activity", parts: ['8.4.38'],},
    {  label : "Human Alterations", parts: ['8.4.39'],},
    {  label : "Degree of decomposition", parts: ['8.4.41'],},
  ],

 async get(id) { 
    data = null;
    try { 
      let res = fetch( `/api/backoffice/samples/${id}`)
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async list() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/samples')
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },  

// formData: 
  async save(sample) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/samples`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(sample),
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async remove(id) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/samples/${id}`, {
        method: "DELETE",
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async update(sample) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/samples/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(sample),
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  }
}

export default SampleService