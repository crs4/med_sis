import doFetch, { doFetchBackOffice, doFetchCatalogue, doFetchGeoserver }  from '../utilities/api-client';



export const UploadService = {
  STATUSES : { 
    UPLOADED : "UPLOADED",
    IN_PROCESS : "IN_PROCESS",
    IMPORT_SUCCESS : "IMPORT_SUCCESS",
    IMPORT_WITH_ERROR : "IMPORT_WITH_ERROR",
    CRITICAL_ERROR: "CRITICAL_ERROR",
  },

  TYPES : {
    XLS_P :  {  name : "XLS_P", label : 'Point Soil Data XLSx upload', sheets: ['General and Surface','Layer descriptions','Lab data','Lab data by sampling depth'],},
    XLS_EM :   {  name : "XLS_EM", label : 'Laboratory Extra Measure XLSx upload', sheets: ['Measures'],},
    XLS_PJ :   {  name : "XLS_PJ", label : 'Projet metadata XLSx upload', sheets: ['Projects'],},
    XLS_PH :   {  name : "XLS_PH", label : 'Photo metadata XLSx upload', sheets: ['Photos'],},
  }, 

  ACTIONS : {
    POST :  {  name : "POST", label : 'CREATE IF NOT EXIST'},
    PUT :   {  name : "PUT", label : 'REPLACE IF EXIST'}, 
    PATCH : { name : "PATCH", label : 'UPDATE IF EXIST'}     
  },

  GET_TYPES_ARRAY() {
    const keys = Object.keys(UploadService.TYPES);
    let arr = [];
    keys.forEach( k => {
      arr.push(this.TYPES[k])
    }); 
    return arr
  },
  
  GET_ACTIONS_ARRAY() {
    const keys = Object.keys(UploadService.ACTIONS);
    let arr = [];
    keys.forEach( k => {
      arr.push(this.ACTIONS[k])
    }); 
    return arr
  },
  
  async get(ck, id) { 
    if ( ck ) 
      return await doFetchBackOffice ( 'xlsx-uploads', id, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async list(ck) {
    if ( ck ) 
      return await doFetchBackOffice ( 'xlsx-uploads', null, 'GET', null, ck );
    else 
      return { ok: false }
  },  

  async save (ck, payload) {
    if ( ck ) 
      return await doFetchBackOffice ( 'xlsx-uploads', null, 'POST', payload, ck );
    else 
      return { ok: false }
  },

  async remove(ck, id) {
    if ( ck ) 
      return await doFetchBackOffice ( 'xlsx-uploads', id, 'DELETE', null, ck );
    else 
      return { ok: false }
  }
}

export default UploadService


