import doFetch from "../utilities/api-client";

export const TaxonomyService = {

  async list(ck) { 
    if ( ck )
      return await doFetch( 'taxonomies' , null, 'GET', null, ck );
    else return { data: null, ok: false, status: null }
  },

  async listValues(ck, id) { 
    if ( ck )
      if ( id )
        return await doFetch( 'taxonomy-values', '?taxonomy='+id, 'GET', null, ck );
      else return await doFetch( 'taxonomy-values', null, 'GET', null, ck );
    else return { data: null, ok: false, status: null }
  },

  async createTaxonomy(ck, payload) { 
    if ( ck && payload )
      return await doFetch( 'taxonomies', null, 'POST', payload, ck );
    else return { data: null, ok: false, status: null }
  },

  async createClassification(ck, payload) { 
    if ( ck && payload )
      return await doFetch( 'taxonomy-values', null, 'POST', payload, ck );
    else return { data: null, ok: false, status: null }
  },

  async updateClassification(ck, id, payload) {
    if ( ck && payload )
      return await doFetch( 'taxonomy-values', id, 'PUT', payload, ck );
    else return { data: null, ok: false, status: null }
  },

  async updateTaxonomy(ck, id, payload) {
    if ( ck && payload )
      return await doFetch( 'taxonomies', id, 'PUT', payload, ck );
    else return { data: null, ok: false, status: null }
  },

  async deleteTaxonomy(ck, id) { 
    if ( ck && id )
      return await doFetch( 'taxonomies', id, 'DELETE', null, ck );
    else return { data: null, ok: false, status: null }
  },

  async deleteClassification(ck, id) { 
    if ( ck && id )
      return await doFetch( 'taxonomy-values', id, 'DELETE', null, ck );
    else return { data: null, ok: false, status: null }
  },

}

export default TaxonomyService


