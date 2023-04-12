import React, { useState, useEffect } from "react";
import axios from "axios";
import { MapContainer, Marker, TileLayer } from "react-leaflet";
import { Icon } from "leaflet";
import "./App.css"
import "leaflet/dist/leaflet.css";


function App() {
  const [position, setPosition] = useState({ lat: 52.517304, long: 13.407008 });

  const myIcon = new Icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/744/744465.png",
    iconSize: [80, 80]
  })

  useEffect(() => {
    const interval = setInterval(() => {
      axios.get("http://127.0.0.1:8000/get-position/40ad23c6-5072-460f-9d1d-acddff5472fa").then((response) => {
        setPosition({ lat: response.data.lat, long: response.data.long });
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);


  return (
    <div>
    <MapContainer center={[52.517304, 13.407008]} zoom={11}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <Marker position={[position.lat, position.long]} icon={myIcon}/>
    </MapContainer>
    </div>
  );
}

export default App;
