import { MapContainer, Marker, Popup, TileLayer } from "react-leaflet";
import { Icon } from "leaflet";
import "./App.css"
import "leaflet/dist/leaflet.css";


function App() {
  const myIcon = new Icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/744/744465.png",
    iconSize: [80, 80]
  })

  return (
    <div>
    <MapContainer center={[52.517304, 13.407008]} zoom={11}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[52.573732,13.209456]} icon={myIcon}/>
    </MapContainer>
    </div>
  );
}

export default App;
