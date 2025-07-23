export const IndicatorService = {
/*
    id = models.TextField(primary_key=True, db_comment='identifier')    
    name = models.TextField( db_comment='Name') 
    creation = models.DateField( blank=True, null=True, db_comment='Date of the creation')
    description = models.TextField( db_comment='Description') 
    type = models.ForeignKey( Taxonomy, on_delete=models.SET_NULL, db_comment='Type of the indicator', related_name='indicators_type_set', blank=True, null=True)
    keywords = models.TextField( db_comment='Geonode dataset keywords')
*/ 
  
  async getAvail() { 
    let data = null;
    try { 
      let res = await fetch( `/soildata/data/labdata.geojson`)
      if ( res && res.status == 200 ) 
        data = await res.json(); 
    } catch (e) { 
    } 
    return data;
  },

  async getTypes() { 
    let data = null;
    try { 
      let res = await fetch( `/soildata/data/indicators_types.json`)
      if ( res && res.status == 200 ) 
        data = await res.json(); 
    } catch (e) { 
    } 
    return data;
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


