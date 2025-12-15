export const RequestService = {
    STATUSES : {
        CREATED : "CREATED",
        IN_PROCESS : "IN_PROCESS",
        ASSIGNED : "ASSIGNED",
        IMPORT_WITH_ERROR : "ELABORATED",
        ERRORS: "ERRORS",
    },
  
  
}

export const getMyCookie = (cookie, name) => {
  const cookieValue = cookie.split('; ')
      .find((row) => row.startsWith(`${name}=`))?.split('=')[1];  
  return cookieValue;
};


export default RequestService


