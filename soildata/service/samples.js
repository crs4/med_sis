export const UploadService = {
  /*
     UPLOAD
     UPLOAD_RESULTS = [
        ("0" , "Created"),
        ("1" , "Importing"),
        ("2" , "Imported"),
        ("3" , "Errors importing data"),
    ]
    type : TYPES
    title : text
    report = JSON
    data = JSON    
    editor: text 
    date: date
    status : STATUS



  */
  STATUS : {
    UPLOADED : "UPLOADED",
    IMPORT_SUCCESS : "IMPORT_SUCCESS",
    IMPORT_WITH_ERROR : "IMPORT_WITH_ERROR",
    CRITICAL_ERROR: "CRITICAL_ERROR",
  },

  TYPES : {
    XLS_P :  {  name : "PROFILES", label : 'Excel Soil Profiles Spreadsheets', sheets: ['General and Surface','Layer descriptions','Soil classification','Lab data'],},
    XLS_S :   {  name : "SAMPLES", label : 'Excel Soil Samples Spreadsheets', sheets: ['General and Surface','Layer descriptions','Lab data'],},
    XLS_PG : { name : "PROFILES_GENEALOGY", label : 'Excel Soil Profiles Genealogy Spreadsheets', sheets: ['Genealogy','Project'],},
    XLS_PG : {  name : "PROFILES_GENEALOGY", label : 'Excel Soil Samples Genealogy Spreadsheets', sheets: ['Genealogy','Project'],},
    XLS_PH : {  name : "PHOTOS", label : 'Photos Metadata', sheets: ['photos'],},
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


