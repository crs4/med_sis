
export const ProfileService = {

  async get(ck, id, model_ep) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/${model_ep}/${id}`, { 
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

  async getLabData(ck, id) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/lab-data?point=${id}`, { 
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
        return { data: null, error: error }
      }
    }
  },
  
  async getLayers(ck, id) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/point-layers?point=${id}`, { 
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
        return { data: null, error: error }
      }
    }
  },

  async getPhotos(ck, id) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/photos/?point=${id}`, { 
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
        return { data: null, error: error }
      }
    }
  },

  async getStructures(ck, id) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/layer-structures?layer=${id}`, { 
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
        return { data: null, error: error }
      }
    }
  },

  async list(ck, model_ep) {  
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    try { 
      let response = await fetch ( `/api/backoffice/${model_ep}`, { 
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
 
  async update (ck, id, field, model_ep) {
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
      try { 
        let response = await fetch ( `/api/backoffice/${model_ep}/${id}`, { 
          method: "PATCH",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken" : csrftoken
          },
          body: JSON.stringify(field),
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

  async remove(ck, id, model_ep) {
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
      try { 
        let response = await fetch(`/api/backoffice/${model_ep}/${id}`, { 
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

export default ProfileService