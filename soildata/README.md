# Diamond-React
https://doodle.com/group-poll/participate/elEvogla
https://medium.com/analytics-vidhya/integrating-a-machine-learning-model-with-django-79dd47eabef1


This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.js`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
# diamond-next

Section =======
ProfileGeneral
LandformTopography
ClimateAndWeather
LandUse - Cultivated - NotCultivated
LitterLayer
Surface
SurfaceCracks
CoarseFragments
SurfaceUnevenness
Section =======

Layer Section =======




Filters
step 1: create S4M_Filter
- chose extends (sections) 
- chhose type ( mapping )
- choose fields (mapping) max 20
step 2: create rules for each field
- for each field
    - set match : ANY, ALL
    - add rules ( type, value)
step 3: test apply
 - API GET data with  filters  (profiles/, samples/) 
 - View map and table ( id, lat, lon added)
 - SAVE FILTER, SAVE FILTER + PUBLISH new GEONODE LAYER 
step 4: 
 - RESULT new FILTER
 - RESULT new GEONODE LAYER

new models: filter, s4m_dataset


mapping -> forms + save su model 







S4M_filter:
{
    mapping: type
    extends: [fieldnames] use sections
    filters: [
        {
            fieldname : -----,
            match : ANY,ALL (or/and),
            rules : [{
                type   : type,
                value  : ----,
            }],
        }
    ]
}
(max 20 fields)


subsetFields  legare agli ids mapping , array 
rules array di rule  
[(, AND, OR,), NOT]
type profile/samples, general(+classification),layer,label data,

s4m_dataset:
geonode_id
filetr_id


/////inverse distance, inverse distance nearest-neighbor, moving average, nearest neighbor, and linear interpolation



---users 2 data manager, 1 admin, 2 user + landsupport



https://opengeo.tech/maps/leaflet-search/examples/outside.html


npm install piexifjs

DateTimeOriginal

 GPSLatitude, GPSLatitudeRef, GPSLongitude, GPSLongitudeRef



 // Show the dates and times when the palm tree photos were taken
for (const [index, exif] of palmExifs.entries()) {    
    const dateTime = exif['0th'][piexif.ImageIFD.DateTime];
    const dateTimeOriginal = exif['Exif'][piexif.ExifIFD.DateTimeOriginal];
    const subsecTimeOriginal = exif['Exif'][piexif.ExifIFD.SubSecTimeOriginal];
    
    console.log(`Date/time taken - Image ${index}`);
    console.log("-------------------------");
    console.log(`DateTime: ${dateTime}`);
    console.log(`DateTimeOriginal: ${dateTimeOriginal}.${subsecTimeOriginal}\n`);
}

// Show the latitudes and longitudes where the palm tree photos were taken 
for (const [index, exif] of palmExifs.entries()) {    
    const latitude = exif['GPS'][piexif.GPSIFD.GPSLatitude];
    const latitudeRef = exif['GPS'][piexif.GPSIFD.GPSLatitudeRef];
    const longitude = exif['GPS'][piexif.GPSIFD.GPSLongitude];
    const longitudeRef = exif['GPS'][piexif.GPSIFD.GPSLongitudeRef];
    
    console.log(`Coordinates - Image ${index}`);
    console.log("---------------------");
    console.log(`Latitude: ${latitude} ${latitudeRef}`);
    console.log(`Longitude: ${longitude} ${longitudeRef}\n`);

    const open = require('open');
    
    // Convert the latitude and longitude into the format that Google Maps expects
    // (decimal coordinates and +/- for north/south and east/west)
    const latitudeMultiplier = latitudeRef == 'N' ? 1 : -1;
    const decimalLatitude = latitudeMultiplier * piexif.GPSHelper.dmsRationalToDeg(latitude);
    const longitudeMultiplier = longitudeRef == 'E' ? 1 : -1;
    const decimalLongitude = longitudeMultiplier * piexif.GPSHelper.dmsRationalToDeg(longitude);
    
    const url = `https://www.google.com/maps?q=${decimalLatitude},${decimalLongitude}`;
    open(url);
    
    const latitudeDegrees = piexif.GPSHelper.dmsRationalToDeg(latitude);
    const longitudeDegrees = piexif.GPSHelper.dmsRationalToDeg(longitude);
    console.log("Original coordinates");

    const altitudeRational = exif['GPS'][piexif.GPSIFD.GPSAltitude];
    const altitudeDecimal = rationalToDecimal(altitudeRational);
    const altitudeRef = exif['GPS'][piexif.GPSIFD.GPSAltitudeRef];
    
    console.log(`Altitude - Image ${index}`);
    console.log("------------------");
    console.log(`${formatAltitude(altitudeDecimal, altitudeRef)}\n`);

}


// Copy the original photo’s picture and Exif data
const newImageData = getBase64DataFromJpegFile('./images/hotel original.jpg');
const newExif = {
    '0th': { ...hotelExif['0th'] },
    'Exif': { ...hotelExif['Exif'] },
    'GPS': { ...hotelExif['GPS'] },
    'Interop': { ...hotelExif['Interop'] },
    '1st': { ...hotelExif['1st'] },
    'thumbnail': null
};



// Change the latitude to Area 51’s: 37° 14' 3.6" N
const newLatitudeDecimal = 37.0 + (14 / 60) + (3.6 / 3600);
newExif['GPS'][piexif.GPSIFD.GPSLatitude] = piexif.GPSHelper.degToDmsRational(newLatitudeDecimal);
newExif['GPS'][piexif.GPSIFD.GPSLatitudeRef] = 'N';
       
// Change the longitude to Area 51’s: 115° 48' 23.99" W
const newLongitudeDecimal = 115.0 + (48.0 / 60) + (23.99 / 3600);
newExif['GPS'][piexif.GPSIFD.GPSLongitude] = piexif.GPSHelper.degToDmsRational(newLongitudeDecimal);
newExif['GPS'][piexif.GPSIFD.GPSLongitudeRef] = 'W';

// Convert the new Exif object into binary form
const newExifBinary = piexif.dump(newExif);

// Embed the Exif data into the image data
const newPhotoData = piexif.insert(newExifBinary, newImageData);

// Save the new photo to a file
let fileBuffer = Buffer.from(newPhotoData, 'binary');
fs.writeFileSync('./images/hotel revised.jpg', fileBuffer);


// Create a “scrubbed” copy of the original hotel photo and save it
const hotelImageData = getBase64DataFromJpegFile('./images/hotel original.jpg');
const scrubbedHotelImageData = piexif.remove(hotelImageData);
fileBuffer = Buffer.from(scrubbedHotelImageData, 'binary');
fs.writeFileSync('./images/hotel scrubbed.jpg', fileBuffer);