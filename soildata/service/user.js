import { doFetchBackOffice }  from '../utilities/api-client';

export const UserService = {
    async getProfile(ck) { 
        if ( ck ) { 
            const response = await doFetchBackOffice ( 'buser-info', null, 'POST', {}, ck );
            if ( !response || !response.ok )
                return null
            else {
                const profile = response.data
                if ( profile.groups.indexOf('admin') !== -1 ||  profile.groups.indexOf('data-managers') !== -1 ) {
                    profile.forbidden = false;
                }
                else profile.forbidden = true;
                return profile 
            }
        }
        else 
            return null
    }

}

export default UserService