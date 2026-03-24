import doFetch  from '../utilities/api-client';

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
    POST :  {  name : "POST", label : 'CREATE IF NOT EXIST', info: 'For each item in the upload the SIS tries to write it in the database. If an item with same id already exists, it throws an error.'},
    PUT :   {  name : "PUT", label : 'REPLACE IF EXIST', info: 'For each item uploaded, the SIS attempts to replace it with the one in the database. If the item doesn\'t exist an error is generated.'},
    PATCH : { name : "PATCH", label : 'UPDATE IF EXIST', info: 'For each item uploaded, the SIS makes partial changes to the item\'s fields in the database. If an item with the same id doesn\'t exist, an error is generated.'},
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
      return await doFetch ( 'xlsx-uploads', id, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async list(ck) {
    if ( ck ) 
      return await doFetch ( 'xlsx-uploads', null, 'GET', null, ck );
    else 
      return { ok: false }
  },  

  async save (ck, payload) {
    if ( ck ) 
      return await doFetch ( 'xlsx-uploads', null, 'POST', payload, ck );
    else 
      return { ok: false }
  },

  async remove(ck, id) {
    if ( ck ) 
      return await doFetch ( 'xlsx-uploads', id, 'DELETE', null, ck );
    else 
      return { ok: false }
  }
}

export default UploadService


