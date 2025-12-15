export const TaxonomyService = {

  async list(ck) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/taxonomies`, { 
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

  async listAllValues(ck) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/taxonomy_values`, { 
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

  async getTaxonomy(ck, id) { 
    let csrftoken = getMyCookie(ck,'csrftoken');
    if ( csrftoken )
    { 
      try { 
        let response = await fetch( `/api/backoffice/taxonomies/${id}`, { 
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
  }
}

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};


export default TaxonomyService


