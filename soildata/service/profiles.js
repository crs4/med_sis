import doFetch  from '../utilities/api-client';

export const ProfileService = {

  async get(ck, id, endpoint) { 
    if ( ck ) 
      return await doFetch ( endpoint, id, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async getLabData(ck, id) { 
    const ep = `lab-data?point=${id}`
    return await get(ck, null, ep);
  },
  
  async getLayers(ck, id) { 
    const ep = `point-layers?point=${id}`
    return await get(ck, null, ep);
  },

  async getPhotos(ck, id) { 
    const ep = `photos?point=${id}`
    return await get(ck, null, ep);
  },

  async getStructures(ck, id) { 
    const ep = `layer-structures?layer=${id}`
    return await get(ck, null, ep);
  },

  async list(ck, endpoint) {
    if ( ck ) 
      return await doFetch ( endpoint, null, 'GET', null, ck );
    else 
      return { ok: false }
  },  
 
  async update (ck, id, payload, endpoint) {
    if ( ck ) 
    { 
      let response = await doFetch ( endpoint, null, 'PATCH', payload, ck );
      return response;
    }
    else return { ok: false }
  },

  async remove(ck, id, endpoint) {
    if ( ck ) 
    { 
      let response = await doFetch ( endpoint, id, 'DELETE', null, ck );
      return response;
    }
    else return { ok: false }
  }
}

export default ProfileService