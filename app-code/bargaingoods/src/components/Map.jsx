// App.js - https://www.freakyjolly.com/google-maps-in-react-example-application/
/*import React from 'react';
import './App.css';
import GoogleMap from './GoogleMap';


function Maps() {

  return (
    <div className="main-wrapper">
      <GoogleMap />
    </div>
  );
}

export default Maps;*/

// https://aws.amazon.com/blogs/mobile/add-maps-to-your-app-in-3-steps-with-aws-amplify-geo/
import { createMap } from "maplibre-gl-js-amplify"; 
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect } from 'react';

import Amplify from 'aws-amplify'; 
import awsconfig from './../aws-exports'; 

Amplify.configure(awsconfig);

async function initializeMap() {
    const map = await createMap({
        container: "map", // An HTML Element or HTML element ID to render the map in https://maplibre.org/maplibre-gl-js-docs/api/map/
        center: [-73.98597609730648, 40.751874635721734], // center in New York
        zoom: 11,
    })
    return map;
}

function Maps() {
    
    useEffect(() => {
      async function getMap() {
        // You can await here
        const map = await initializeMap();
        // ...
      }
      getMap();
    }, []); // Or [] if effect doesn't need props or state

    return (
      <div className="App">
        <h1>My Restaurant</h1>
        <ul id="locations">
          <li><b>My Restaurant - Upper East Side</b> <br/> 300 E 77th St, New York, NY 10075 </li>
          <li><b>My Restaurant - Hell's Kitchen</b><br/> 725 9th Ave, New York, NY 10019</li>
          <li><b>My Restaurant - Lower East Side</b><br/> 102 Norfolk St, New York, NY 10002</li>
        </ul>
        <div id="map"></div>
      </div>
    );
}

export default Maps;

/*import { MapView, Heading, Text } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';
import { useState } from 'react';
import { Marker, Popup } from 'react-map-gl';

import '@aws-amplify/ui-react/styles.css';

import awsExports from './../aws-exports';

Amplify.configure(awsExports);

function MarkerWithPopup({ latitude, longitude }) {
  const [showPopup, setShowPopup] = useState(false);

  const handleMarkerClick = ({ originalEvent }) => {
    originalEvent.stopPropagation();
    setShowPopup(true);
  };

  return (
    <>
      <Marker
        latitude={latitude}
        longitude={longitude}
        onClick={handleMarkerClick}
      />
      {showPopup && (
        <Popup
          latitude={latitude}
          longitude={longitude}
          offset={{ bottom: [0, -40] }}
          onClose={() => setShowPopup(false)}
        >
          <Heading level={2}>Marker Information</Heading>
          <Text>Some information about a location.</Text>
        </Popup>
      )}
    </>
  );
}

export default function MapWithMarkerPopup() {
  return (
    <MapView initialViewState={{ latitude: 40, longitude: -100, zoom: 3.5 }}>
      <MarkerWithPopup latitude={40} longitude={-100} />
    </MapView>
  );
}*/