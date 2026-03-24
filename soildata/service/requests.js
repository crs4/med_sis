import doFetch  from '../utilities/api-client';

export const RequestService = {
    STATUSES : {
        CREATED : "CREATED",
        IN_PROCESS : "IN_PROCESS",
        UPDATED : "UPDATED",
        IMPORT_WITH_ERROR : "ELABORATED",
        ERRORS: "ERRORS",
    },

    async list(ck) { 
        if ( ck ) 
            return await doFetch ( 'requests', null, 'GET', null, ck );
        else 
            return { ok: false }
    },
    
    async create(ck, payload) {
        if ( ck ) 
            return await doFetch ( 'requests', null, 'GET', payload, ck );
        else 
            return { ok: false }
    },
    
    async update(ck, id, payload) { 
        if ( ck ) 
            return await doFetch ( 'requests', id, 'PATCH', payload, ck );
        else 
            return { ok: false }
    },
    
    async delete(ck, id) { 
        if ( ck ) 
            return await doFetch ( 'requests', id, 'DELETE', null, ck );
        else 
            return { ok: false }
    },  
}

export default RequestService


