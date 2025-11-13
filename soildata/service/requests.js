export const RequestService = {
   
  STATUSES : {
    CREATED :  "Created", 
    ASSIGNED : "Assigned",  
    ELABORATED : "Elaborated",
    ELABORATING : "Elaborating", 
    CANCELLED : "Cancelled", 
  },
  TYPES : {
    POINTDATA :  "Soil Point data", 
    INDICATOR : "Soil Indicator", 
  },
  /* structure:
  return fetch('/demo/data/files.json', {
            headers: { 'Cache-Control': 'no-cache' }
        })
            .then((res) => res.json())
            .then((d) => d.data);
    },



  //// const _request = { 
          'id': router.query.id,  ///auto-increment
          'name': 'Request3',
          'user': 1004, 
          'date': new Date('2025/05/25'),
          'manager': 1001,
          'data_type' : 'indicator', 
          'data_key': 'pluto',
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
 
      }
  */
  async get(id) { 
    data = null;
    try { 
      let res = fetch( `/api/backoffice/requests/${id}`)
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  },

  async list() {  
    let data = [];
    try {  
      let res = fetch('/api/backoffice/requests')
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
      let res = fetch(`/api/backoffice/requests`, {
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

  async update(id,request) {
    let data = null;
    try {  
      let res = fetch(`/api/backoffice/requests/${id}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      });
      if ( res && res.status == 200 ) 
        data = await res.json();
    } catch (e) { 
    } 
    return data;
  }
}

export default RequestService


