import { MapContainer, TileLayer, Circle } from 'react-leaflet';
import L from 'leaflet';
import "leaflet/dist/leaflet.css"

export default function S4Mmap ({point}) {
  
  return (
    <>
      <div className="card w-full">
        <h4 class="font-bold text-green-500">Geo Location</h4>
        <MapContainer
          doubleClickZoom={false}
          id='S4MMap'
          zoom={14}
          center={point}
          style={{ height: '300px' }}
        >
          <TileLayer
            url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}'
            attribution='Tiles &copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri'
          />
          <Circle
            center={point}
            pathOptions={{ color: 'green', fillColor: 'green' }}
            radius={100}
          />
        </MapContainer>
      </div>
    </>  
  );
};


        