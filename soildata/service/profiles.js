import Taxonomies from '../service/taxonomies';

export const ProfileService = {
  
  
  
}

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};

export default ProfileService