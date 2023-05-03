import './App.css';
import {io} from 'socket.io-client'
import React, {useState, useEffect, useMemo} from 'react';
import {GoogleMap, MarkerF, LoadScript, CircleF} from '@react-google-maps/api'
let socket;



function App() {
  const [data, setData] = useState([]);
  const [markers, setMarkers] = useState([{ lat: 38.032750, lng:  -78.510423, speed: 5.0, battery: 100}]);


  const center = useMemo(() => ({ lat: 38.032750, lng:  -78.510423 }), []);

  useEffect(() => {
    
    socket = io('http://localhost:5000',{forceNew:true});

    socket.on('hello', (new_data) => {
      console.log(new_data)
      setData(data => [...data, new_data])
    })

    socket.on("ttn_data",(new_marker) => {
      console.log(new_marker)
      setMarkers(markers => [...markers, new_marker])

    })

    return (() => {
      socket.disconnect();
    })
  }, [])

  return (
    <div className="App">
      <LoadScript googleMapsApiKey={process.env.REACT_APP_API_KEY}>
        <GoogleMap
            mapContainerClassName='map-container'
            center={center}
            zoom={18.5}
          >
            <MarkerF 
                    position={{lat: 38.031770, lng: -78.511003}}
                    label={{text: "Home Base", fontWeight: "bolder"}}
                    key={-1}
                    >

            </MarkerF>
            {
              markers.map((marker, i) => {
                return(
                  <div>
                    <MarkerF 
                      position={{lat:marker.lat, lng:marker.lng}}
                      label={{text: marker.speed+"m/s", fontWeight: "bolder"}}
                      key={i}
                      >

                    </MarkerF>
                    <CircleF
                      visible={(i == markers.length-1)}
                      radius={2*marker.battery}
                      fillColor={"#ff0000"}
                      fillOpacity={0.35}
                      center={{lat:marker.lat, lng:marker.lng}}
                    ></CircleF>
                  </div>
                )
              })
            }
        </GoogleMap>
      </LoadScript>
        
    </div>
  );
}

export default App;
