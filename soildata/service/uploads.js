export const UploadService = {
  STATUSES : { 
    UPLOADED : "UPLOADED",
    IN_PROCESS : "IN_PROCESS",
    IMPORT_SUCCESS : "IMPORT_SUCCESS",
    IMPORT_WITH_ERROR : "IMPORT_WITH_ERROR",
    CRITICAL_ERROR: "CRITICAL_ERROR",
  },

  TYPES : {
    XLS_P :  {  name : "XLS_P", label : 'Point Soil Data', sheets: ['General and Surface','Layer descriptions','Lab data','Lab data by sampling depth'],},
    XLS_PJ :   {  name : "XLS_PJ", label : 'Data Genealogy', sheets: ['Project'],},
    XLS_PH :   {  name : "XLS_PH", label : 'Photos', sheets: ['Photos'],},
  },

  ACTIONS : {
    POST :  {  name : "POST", label : 'CREATE IF NOT EXIST', info: 'For each item in the upload the SIS tries to write it in the database. If an item with same id already exists, it throws an error.'},
    PUT :   {  name : "PUT", label : 'CREATE IF NOT EXIST OR REPLACE IF EXIST', info: 'For each item uploaded, the SIS attempts to replace it with the one in the database. If the item doesn\'t exist, it creates it.'},
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
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/xlsx-uploads/${id}`, { 
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken" : csrftoken
          },
        })
        if ( !response || !response.ok) {
          // get error message from body or default to response status
          return { data: null, error: true }
        }
        const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = isJson && await response.json();
        return { data: data, error: null }
      }
      catch( error )  {
        console.log(error)
        return { data: null, error: error }
      }
    }
  },

  async list(ck) {  
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    try { 
      let response = await fetch( '/api/backoffice/xlsx-uploads/', { 
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken" : csrftoken
        },
      })
      const isJson = response.headers.get('content-type')?.includes('application/json');
      const data = isJson && await response.json();
      if ( !response || !response.ok) {
            // get error message from body or default to response status
          const error = (data && data.message) || response.status;
          return { data: null, error: error }
      }
      return { data: data, error: null }
    }
    catch( error ) {
      return { data: null, error: `Error: ${error}` }
    }
    else return { data: null, error: 'Error: wrong token' }
  },  

// formData: 
  async save (ck, upload) {
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
      try { 
        let response = await fetch(`/api/backoffice/xlsx-uploads/`, { 
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken" : csrftoken
          },
          body: JSON.stringify(upload),
        })
        const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = isJson && await response.json();
        if ( !response || !response.ok) {
            return { ok: false, msg: 'Errors sending data' }
        }
        return { ok: true, msg: 'Data has been sent' }
      }
      catch( error ) {
          return { ok: false, msg: `Error: ${error}` }
      }  
    else return { ok: false, msg: 'Error: Bad token' }
  },

  async remove(ck, id) {
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
      try { 
        let response = await fetch(`/api/backoffice/xlsx-uploads/${id}`, { 
          method: "DELETE", 
          headers: {
            "X-CSRFToken" : csrftoken
        }})
        const isJson = response.headers.get('content-type')?.includes('application/json');
        const data = isJson && await response.json();
        if ( !response || !response.ok) {
          const error = (data && data.message) || response.status;
          return { status: response.status, message: error }
        }
        return { status: response.status, message: 'Delete successful' }
      }
      catch(error) {
        return { status: null, message: error }
      }
    return { status: null, message: 'Bad Token' }
  }
}

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};


export default UploadService


