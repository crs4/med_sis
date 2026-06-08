import { doFetchBackOffice, doFetchCatalogue, doFetchGeoserver }  from '../utilities/api-client';

export const ProfileService = {

  FILTER_DEPTH : {
    DEPTH0_20: "DEPTH0_20",
    DEPTH20_50: "DEPTH20_50",
  },
  
  DATASET_CONTEXT : {
    POINTS_SOIL_DATA: "POINTS_SOIL_DATA",
    SOIL_INDICATOR: "SOIL_INDICATOR"
  },

  DATASET_STATUSES : {
    CREATED : "CREATED",
    CONFIGURED : "CONFIGURED",
    IN_PROCESS : "IN_PROCESS",
    VALIDATED : "VALIDATED",
    PUBLISHED : "PUBLISHED",
    ERRORS : "ERRORS"
  },

  async getDataset(typename, bboxFilter, token) { 
    if ( typename && token ) 
      return await doFetchGeoserver ( typename, bboxFilter, token );
    else 
      return { ok: false }
  },

  async getDatasetsByCategory(category, page, ck) { 
    if ( ck ) 
      return await doFetchCatalogue( 'datasets?f=dataset&filter{category.identifier}='+category+ '&filter{srid}=EPSG:4326&page=' + page + '&page_size=100&format=json', null, 'GET', null, ck );
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


/*  AREA di lavoro da cancellare via boot or published ????? /tmp/ dataset:id:time:time
1)  aggregate points: points.geojson
2)  trasformation: if points and or aoi not exist 
    gdal vector reproject -s EPSG:4326 -t EPSG:xx6yy points.geojson points.shp
    //// reproject aoi bbox  West	 East	 South	 North	
    gdal vector reproject -s EPSG:4326 -t EPSG:xx6yy aoibbox.geojson aoibbox.shp
    write cmd.txt ( to elaborate )
3a)  clean diagram.csv -> elaborate for diagram -> generate.csv  
4a)  python add csv as json to dataset
3b)  clean tiff    

*/