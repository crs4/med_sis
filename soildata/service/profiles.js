import { doFetchBackOffice, doFetchCatalogue, doFetchGeoserver }  from '../utilities/api-client';

export const ProfileService = {

  DATASET_CONTEXT : {
    POINTS_SOIL_DATA: "POINTS_SOIL_DATA",
    SOIL_INDICATOR: "SOIL_INDICATOR"
  },

  DATASET_STATUSES : {
    CREATED : "CREATED",
    CONFIGURED : "CONFIGURED",
    IN_PROCESS : "IN_PROCESS",
    PROCESSED : "PROCESSED",
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

  async getDatasetsByCategory(category, page, ck) { 
    if ( ck ) 
      return await doFetchCatalogue( 'datasets?f=dataset&filter{category.identifier}='+category+ '&page=' + page + '&page_size=100&format=json', null, 'GET', null, ck );
    else 
      return { ok: false }
  },

  // keywords is a slugs' list comma separated  
  async getDatasetsByKeyword( keywords, page, ck) {
    let filter = ''; 
    for ( let i = 0; i < keywords.length; i += 1 )
      filter += 'filter{keywords.slug.in}=' + keywords[i] + '&'
    if ( ck )  
      return await doFetchCatalogue( 'datasets?f=dataset&' + filter + 'page=' + page + '&page_size=100&format=json', null, 'GET', null, ck );
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
    const ep = `lab-data/?point=${id}`
    return await doFetchBackOffice ( ep, null, 'GET', null, ck );
  },

  async getExtraLabData(ck, id) { 
    const ep = `lab-data-extra-measures/?point=${id}`
    return await doFetchBackOffice ( ep, null, 'GET', null, ck );
  },
  
  async getLayers(ck, id) { 
    const ep = `point-layers/?point=${id}`
    return doFetchBackOffice ( ep, null, 'GET', null, ck );
  },

  async getPhotos(ck, id) { 
    const ep = `photos/?point=${id}`
    return doFetchBackOffice ( ep, null, 'GET', null, ck );
  },

  async getStructures(ck, id) { 
    const ep = `layer-structures/?layer=${id}`
    return doFetchBackOffice ( ep, null, 'GET', null, ck );
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