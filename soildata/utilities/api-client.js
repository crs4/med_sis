export const doFetch = async ( base_url, endpoint, id, method, payload, cookie) =>  
{ 
  try { 
    if ( !cookie || !endpoint || !method )
      return { data: null, ok: false, status: null }
    let csrftoken = getMyCookie(cookie, 'csrftoken');
    let response = null;
    let headers = {
      "Content-Type": "application/json",
      "X-CSRFToken" : csrftoken,
      Accept: "application/json"
    };
    let url = base_url + '/' + endpoint ;
    let body = null
    if ( id )
      url += '/' + id ;
    if ( payload )
      body = JSON.stringify(payload)
    response = await fetch( url, { method: method, headers: headers, body: body } )
    if ( !response || !response.ok ) {
      return { data: null, ok: false, status: response.status }
    }
    const isJson = response.headers.get('content-type')?.includes('application/json');
    const data = isJson && await response.json();
    return { data: data, ok: true, status: response.status }   
  }
  catch( error )  {
    console.log(error)  
  }
  return { data: null, ok: false, status: null }
}

export const doFetchBackOffice = async ( endpoint, id, method, payload, cookie) =>  
{ 
  if ( !id )
    endpoint += '/';
  return doFetch (process.env.NEXT_PUBLIC_BACKOFFICE_API_BASE_URL, endpoint , id, method, payload, cookie)
}

export const doFetchGeoserver = async (dataset, cookie) =>  
{ 
  try { 
    if ( !cookie || !dataset )
      return { data: null, ok: false, status: null }
    let csrftoken = getMyCookie(cookie, 'csrftoken');
    let url = process.env.NEXT_PUBLIC_GEOSERVER_BASE_URL 
    url += '/ows?SERVICE=WFS&VERSION=1.3.0&REQUEST=GetFeature&outputFormat=application%2Fjson&'
    url += 'typename=' + dataset + '&access_token=' + csrftoken;
    let headers = {
      Accept: "application/json"
    };
    let response = await fetch( url, { method: 'GET', headers: headers } )
    if ( !response || !response.ok ) {
      return { data: null, ok: false, status: response.status }
    }
    const data = await response.json();
    return { data: data, ok: true, status: response.status }   
  }
  catch( error )  {
    console.log(error)  
  }
  return { data: null, ok: false, status: null }
}

export const doFetchCatalogue = async ( endpoint, id, method, payload, cookie) => 
{ 
  return doFetch (process.env.NEXT_PUBLIC_CATALOGUE_API_BASE_URL, endpoint, id, method, payload, cookie)
}

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};

export default doFetch;
