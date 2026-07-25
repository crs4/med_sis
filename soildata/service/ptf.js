/* Service to manage back end request for Hydro Ptf Elaborations 
  @Author: Roberto Demontis 
*/

import doFetch, { doFetchBackOffice, doFetchCatalogue, doFetchGeoserver }  from '../utilities/api-client';

export const PTFService = {

  HYDRO_PTF_ELABORATION_STATUSES : { 
    CREATED : "CREATED",
    IN_PROCESS : "IN_PROCESS",
    SUCCESS : "SUCCESS",
    ERRORS: "ERRORS",
  },

  async postSingleShot(ck, payload) { 
    if ( ck ) 
      return await doFetchBackOffice ( 'hydro-ptf-prediction', null, 'POST', payload, ck );
    else 
      return { result: null }
  },

  async get(ck, id) { 
    if ( ck ) 
      return await doFetchBackOffice ( 'hydro-ptf-elaborations', id, 'GET', null, ck );
    else 
      return { ok: false }
  },

  async list(ck) {
    if ( ck ) 
      return await doFetchBackOffice ( 'hydro-ptf-elaborations', null, 'GET', null, ck );
    else 
      return { ok: false }
  },  

  async create (ck, payload) {
    if ( ck ) 
      return await doFetchBackOffice ( 'hydro-ptf-elaborations', null, 'POST', payload, ck );
    else 
      return { ok: false }
  },

  async update (ck, id, payload) {
    if ( ck ) 
      return await doFetchBackOffice ( 'hydro-ptf-elaborations', id, 'PUT', payload, ck );
    else 
      return { ok: false }
  },

  async remove(ck, id) {
    if ( ck ) 
      return await doFetchBackOffice ( 'hydro-ptf-elaborations', id, 'DELETE', null, ck );
    else 
      return { ok: false }
  }
}

export default PTFService


