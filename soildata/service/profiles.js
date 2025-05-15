export const ProfileService = {
  
  
  MODELS : {
    ProfileGeneral :  {  label : "Profile General Section", parts: ['WRB2022 General par. 8.2.1','WRB2022 Location par 8.2.2','Notes'],},
    LandformTopography :  {  label : "Profile Landform Topography Section", parts: ['WRB2022 Landform Topography par. 8.2.3'],},
    ProfileGeneral :  {  label : "Profile General Section", parts: ['WRB2022 General par. 8.2.1','WRB2022 Location par 8.2.2','Notes'],},
    ProfileGeneral :  {  label : "Profile General Section", parts: ['WRB2022 General par. 8.2.1','WRB2022 Location par 8.2.2','Notes'],},
    ProfileGeneral :  {  label : "Profile General Section", parts: ['WRB2022 General par. 8.2.1','WRB2022 Location par 8.2.2','Notes'],},
    ProfileGeneral :  {  label : "Profile General Section", parts: ['WRB2022 General par. 8.2.1','WRB2022 Location par 8.2.2','Notes'],},
    ProfileGeneral :  {  label : "Profile General Section", parts: ['WRB2022 General par. 8.2.1','WRB2022 Location par 8.2.2','Notes'],},
  },

  UPLOAD_STATUS : {
    "EMPTY" : "XSLx data sent to server",
    "PROCESSING"   : "XSLx processing",
    "ERROR"   : "System error",
    "WARNING" : "Data partially saved (errors)",
    "SUCCESS" : "Data sucessfully saved",
  },

  async getUpload(id) { 
    fetch( `/backoffice/api/v2/uploads/${id}`);
  },

  async getUploads() {  
    let res = [];
    try {  
      fetch('/backoffice/api/v2/uploads')
        .then((res) => res.json())
        .then((data) => {
          res = data
      });
    } catch (e) { 
      res = [];
    } 
    return res;
  },  

// formData: ( title, date, file, type }
  async save(upload) {
    fetch(`/backoffice/api/v2/uploads`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(upload),
    });
  },


  async remove(id) {
    fetch(`/backoffice/api/v2/uploads/${id}`, {
      method: "DELETE",
    });
  }
}


export default UploadService;


