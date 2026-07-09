import Mapping from '../data/mapping';
import { point, clone, bbox, bboxPolygon, featureCollection, pointsWithinPolygon } from '@turf/turf';
import { pointsWithinPolygon } from turf

// Filters:  Area Of Interest; depth; project; type; method; date  ),
export default filter = async (filter,points) => {
  if ( points && filter )
    let result = points
    if ( filter.aoi )
      result = pointsWithinPolygon( points, filter.aoi)
  let perc;
  let workbook = new ExcelJS.Workbook();
  try {
    const blob = new Blob([files[0]], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8' });
    const buffer = await blob.arrayBuffer();
    await workbook.xlsx.load(buffer);
  } catch (e) {
    console('Error reading file')
    return null;
  }
  let vresult = { 'validated' : 0,'data' : [], report : { 'errors': [], 'tree': [] } };
  let total_rows = 0;
  let total_valid = 0;
  
  if ( uploadType && UploadService.TYPES[uploadType] && UploadService.TYPES[uploadType].sheets ) {
    let sheets = UploadService.TYPES[uploadType].sheets;
    for ( let s=0; s<sheets.length; s+=1 ) {
      try {
        let worksheet = null;
        for ( let si=0; si<workbook.worksheets.length; si+=1 ) {
          if ( sheets[s].trim() === workbook.worksheets[si].name.trim())
            worksheet = workbook.worksheets[si]; 
        }
        if ( worksheet ) {
          vresult['data'][sheets[s]] = [];
          const sheet_mapping = Mapping[uploadType+':'+sheets[s]];
          if ( sheet_mapping ) {
            worksheet.eachRow({ includeEmpty: true }, function(row, rowNumber) {
              if ( rowNumber >= sheet_mapping['startRow'] )  {
                if ( row.values[1] ){
                  row.values[1] = row.values[1].toString().trim();
                  vresult['data'][sheets[s]][rowNumber] = row.values;
                  total_rows+=1;
                }
              }
            })  
          }
          if ( uploadType === 'XLS_P')
            total_valid += validatePointSheet(taxonomies, sheets[s], sheet_mapping, vresult);
          else if ( uploadType === 'XLS_PJ' || uploadType === 'XLS_PH' )
            total_valid += await validateSingleSheet(taxonomies, sheets[s], sheet_mapping, vresult);
          perc = (total_valid/total_rows)*100;
          vresult['validated'] =  Math.trunc(Number(perc).toPrecision(4));
        }
        else  {
          console.log('Error worksheet'+sheets[s]);
        }
      } catch (e) {
        console.log(e);
      }
    }  
  } 
  return vresult; 
}
