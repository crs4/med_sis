import { doFetchBackOffice, doFetchCatalogue, doFetchGeoserver }  from '../utilities/api-client';

export const ProfileService = {

  DATASET_STATUSES : {
    CREATED : "CREATED",
    CONFIGURED : "CONFIGURED",
    IN_PROCESS : "IN PROCESS",
    PREPROCESSED : "PROCESSED",
    VALIDATED : "VALIDATED",
    INTERPOLATED : "INTERPOLATED",
    VALIDATED : "VALIDATED",
    PUBLISHED : "PUBLISHED",
    ERRORS : "ERRORS"
  },
  
  async getDataset(dataset, ck) { 
    
    if ( ck ) 
      return await doFetchGeoserver ( dataset, ck );
    else 
      return { ok: false }
  },

  async getDatasetsByCategory(category, ck) { 
    if ( ck ) 
      return await doFetchCatalogue( 'datasets?filter{category.identifier}='+category, ck );
    else 
      return { ok: false }
  },

  async getDatasetsByKeyword( keyword, ck) { 
    if ( ck ) 
      return await doFetchCatalogue( 'datasets?filter{keywords.name}='+keyword, ck );
    else 
      return { ok: false }
  },

  async get(ck, id, endpoint) { 
    if ( ck ) 
      return await doFetchBackOffice ( endpoint, id, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async getLabData(ck, id) { 
    const ep = `lab-data?point=${id}`
    return await get(ck, null, ep);
  },
  
  async getLayers(ck, id) { 
    const ep = `point-layers?point=${id}`
    return doFetchBackOffice ( ep, null, 'GET', null, ck );
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
      return await doFetchBackOffice ( endpoint, null, 'GET', null, ck );
    else 
      return { ok: false }
  },  
 
  async update (ck, id, payload, endpoint) {
    if ( ck ) 
    { 
      let response = await doFetchBackOffice ( endpoint, null, 'PATCH', payload, ck );
      return response;
    }
    else return { ok: false }
  },
  
  async save (ck, payload, endpoint ) {
    if ( ck ) 
      return await doFetchBackOffice ( endpoint, null, 'POST', payload, ck );
    else 
      return { ok: false }
  },

  async remove(ck, id, endpoint) {
    if ( ck ) 
    { 
      let response = await doFetchBackOffice ( endpoint, id, 'DELETE', null, ck );
      return response;
    }
    else return { ok: false }
  }
}

export default ProfileService