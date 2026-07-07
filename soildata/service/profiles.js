import { doFetchBackOffice, doFetchCatalogue, doFetchGeoserver }  from '../utilities/api-client';

export const ProfileService = {

  FILTER_DEPTH : {
    DEPTH0_20: "DEPTH0_20",
    DEPTH20_50: "DEPTH20_50",
  },
  
  DATASET_CONTEXT : {
    POINTS_SOIL_DATA: "POINTS_SOIL_DATA",
    SOIL_INDICATOR: "SOIL_INDICATOR",
    AOI_SOIL_INDICATOR: "AOI_SOIL_INDICATOR",
    LABDATA_EXTRA_MEASURE: "LABDATA_EXTRA_MEASURE" 
  },

  DATASET_STATUSES : {
    CREATED : "CREATED",
    CONFIGURED : "CONFIGURED",
    IN_PROCESS : "IN_PROCESS",
    VALIDATED : "VALIDATED",
    PUBLISHED : "PUBLISHED",
    ERRORS : "ERRORS"
  },

  BASE_DATASET_STATUSES : {
    "TO_CONFIGURE": "TO_CONFIGURE",
    "CREATED": "CREATED",
    "IN_PROCESS": "IN_PROCESS",
    "PUBLISHED": "PUBLISHED",
    "ERRORS": "ERRORS"
  },

  BASE_DATASET_TYPES : {
    "SOIL_INDICATOR": "SOIL_INDICATOR",
    "POINT_SOIL_DATA_SECTION": "POINT_SOIL_DATA_SECTION"
  },

  async getDataset(typename, bboxFilter, token) { 
    if ( typename && token ) 
      return await doFetchGeoserver ( typename, bboxFilter, token );
    else 
      return { ok: false }
  },

  async getDatasetsByAlternate(alternate, ck) { 
    if ( ck ) 
      return await doFetchCatalogue( 'datasets?filter{alternate}='+alternate+ '&format=json', null, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async getDatasetsByCategory(category, ck) { 
    if ( ck ) 
      return await doFetchCatalogue( 'datasets?filter{category.identifier}='+category+ '&filter{srid}=EPSG:4326&format=json', null, 'GET', null, ck );
    else 
      return { ok: false }
  },

  // keywords is a slugs' list comma separated  
  async getDatasetsByKeyword( keywords, page, ck) {
    let filter = ''; 
    for ( let i = 0; i < keywords.length; i += 1 )
      filter += 'filter{keywords.slug.in}=' + keywords[i] + '&'
    if ( ck )  
      return await doFetchCatalogue( 'datasets?f=dataset&' + filter + 'filter{srid}=EPSG:4326&page=' + page + '&page_size=100&format=json', null, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async get(ck, id, endpoint) { 
    if ( ck ) 
      return await doFetchBackOffice ( endpoint, id, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async calculateVariogram(ck, id, payload) { 
    const endpoint = `variogram/?id=${id}`
    return await doFetchBackOffice ( endpoint, null, 'POST', payload, ck );
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
      let response = await doFetchBackOffice ( endpoint, id, 'PUT', payload, ck );
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
