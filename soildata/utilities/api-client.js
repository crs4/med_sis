export const doFetch = async (endpoint, id, method, payload, cookie) =>  
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
    let url = process.env.NEXT_PUBLIC_URL_BACKOFFICE_API_BASE_URL + '/' + endpoint + '/';
    let body = null
    if ( id )
      url += id ;
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

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};

export default doFetch;
