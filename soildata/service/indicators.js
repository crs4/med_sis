export const IndicatorService = {
  
  STATUS : {
    CREATED : "CREATED",
    INITIALIZED : "INITIALIZED",
    CRITICAL_ERROR: "CRITICAL_ERROR",
  },

  TYPES : {
    SIMPLE :  {  name : "SIMPLE", label : 'Simple index  ', note: 'Index calculated using a known formula'},
    COMPLEX :  {  name : "COMPLEX", label : 'Complex index  ', note: 'Index via model application'},
    CUSTOM :   {  name : "CUSTOM", label : 'Custom index', note: 'Index calculated using a known formula'},
  },

  async get(id) { 
    data = null;
    try { 
      let res = fetch( `/api/backoffice/indicators/${id}`)
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async list() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/indicators')
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },  

// formData: 
  async save(indicator) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/indicators`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(indicator),
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
      let res = fetch(`/api/backoffice/indicators/${id}`, {
        method: "DELETE",
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async update(indicator) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/indicators/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(indicator),
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  }
}

export default IndicatorService


