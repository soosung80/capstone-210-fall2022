import {
	Flex,
	Heading,
	MapView,
	View,
	Text,
	Link
} from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';

import '@aws-amplify/ui-react/styles.css';

import awsExports from './../aws-exports';

import { useState } from 'react'
import { Marker, Popup, Map } from 'react-map-gl';

Amplify.configure(awsExports);

function MarkerWithPopup({ latitude, longitude, title, total, distance, travel, address }) {
	const [showPopup, setShowPopup] = useState(false)

	const handleMarkerClick = ({ originalEvent }) => {
		originalEvent.stopPropagation()
		setShowPopup(true)
	}
	
	const googleMapURL = "https://maps.google.com/?q="+address;

	return (
		<>
			<Marker
				latitude={latitude}
				longitude={longitude}
				onClick={handleMarkerClick}
				scale={0.8}
				color={'blue'}
			/>
			{showPopup && (
				<Popup
					latitude={latitude}
					longitude={longitude}
					offset={{ bottom: [0, -40] }}
					onClose={() => setShowPopup(false)}
				>
					<Heading level={5}>{title}</Heading>
					<Text>Total: ${total}</Text>
					<Text>Distance: {distance} mi</Text>
					<Text>Travel time: {travel} min</Text>
					<Link href={googleMapURL} color="blue" isExternal={true}>{address}</Link>
				</Popup>
			)}
		</>
	)
}

function MarkerWithPopupRed({ latitude, longitude, title }) {
	const [showPopup, setShowPopup] = useState(false)

	const handleMarkerClick = ({ originalEvent }) => {
		originalEvent.stopPropagation()
		setShowPopup(true)
	}

	return (
		<>
			<Marker
				latitude={latitude}
				longitude={longitude}
				onClick={handleMarkerClick}
				scale={0.8}
				color={'red'}
			/>
			{showPopup && (
				<Popup
					latitude={latitude}
					longitude={longitude}
					offset={{ bottom: [0, -40] }}
					onClose={() => setShowPopup(false)}
				>
					<Heading level={5}>You are here</Heading>
				</Popup>
			)}
		</>
	)
}

export default function MapStores(props) {
	const stores = props.stores;
	const userData = props.userLoc;
	
	let storeList = [];
     // limit output to top 5 stores
    
    if (stores.length > 5) {
        storeList = stores.slice(0, 5);
    }
	
	return (
		<>
			<Flex direction={'column'} alignItems={'left'} marginTop={'10px'}>
				<Heading level={4}>Select a marker to see store details.</Heading>
				<MapView
					initialViewState={{
						longitude: userData.user_preference.user_location.lng,
						latitude: userData.user_preference.user_location.lat,
						zoom: 12,
					}}
					style={{ width: '600px', height: '600px' }}
				>
					{storeList.map((loc, i) => 
						<MarkerWithPopup
							key={i}
							latitude={loc.lat}
							longitude={loc.lng}
							title={loc.store_name}
							total={loc.total}
							distance={loc.distance}
							travel={loc.travel_time}
							address={loc.address}
						/>
					)}
					<MarkerWithPopupRed
							key="user"
							latitude={userData.user_preference.user_location.lat}
							longitude={userData.user_preference.user_location.lng}
							title="You're here"
						/>
				</MapView>
			</Flex>
		</>
	)
}
