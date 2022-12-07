import React from "react";
import {
  Card,
  Heading,
  SliderField,
  CheckboxField,
  SelectField,
  Text
} from '@aws-amplify/ui-react';
import AutoComplete from './AutoComplete'
import '@aws-amplify/ui-react/styles.css';

export const UserPreferences = (props) => {
  
  const inputData = props.inputData;
  const updateDistanceProps = props.updateDistanceProps;
  const updateBudgetProps=props.updateBudgetProps;
  const updateUserLocProps=props.updateUserLocProps;
  const updateKosherProps=props.updateKosherProps;
  const updatePescatarianProps=props.updatePescatarianProps;
  const updateNoRedMeatProps=props.updateNoRedMeatProps;
  const updateDairyFreeProps=props.updateDairyFreeProps;
  const updateGlutenFreeProps=props.updateGlutenFreeProps;
  const updateTravelModeProps=props.updateTravelModeProps;
  const setSubmitDisabled=props.setSubmitDisabled;

  const [userLocation, setUserLocation] = React.useState(false);
  const [status, setStatus] = React.useState(null);
  
    const handleUserLocationBoxChange = (e) => {
      setUserLocation(e.target.checked);
      if (e.target.checked) {
        // then get the user's coordinates
        if (!navigator.geolocation) { 
			    alert('Geolocation is not supported by your browser, please enter an address');
    		} else {
                setStatus('Locating...');
                setSubmitDisabled(true);
                navigator.geolocation.getCurrentPosition((position) => {
                    setStatus(null);
                    setSubmitDisabled(false);
                    updateUserLocProps(position.coords.latitude, position.coords.longitude, "Your current location");
                }, (error) => {
                    setStatus(null);
                    setSubmitDisabled(false);
                    alert('Unable to retrieve your location, please enter an address.');
                    alert(error);
                });
            }
      }
    }
  
    return (
      <form>
        <Card
          borderRadius="medium"
          maxWidth="20rem"
          variation="outlined"
          marginBottom="1rem"
        > 
          Enter your preferences 
        </Card>
        <Card 
          borderRadius="medium"
          maxWidth="20rem"
          variation="outlined"
          marginBottom="1rem"
        >

          <AutoComplete updateUserLocProps={updateUserLocProps}/>

          <CheckboxField
            marginTop="0.5rem"
            name="user_location"
            value="user_location"
            checked={userLocation}
            onChange={handleUserLocationBoxChange}
            label="Use my current location."
          />
          <Text
              variation="info"
              as="p"
              lineHeight="1.5em"
              fontWeight={400}
              fontSize="0.8em"
              fontStyle="normal"
              textDecoration="none"
              width="100%"
              marginTop="10px"
            >
              (Current location: {inputData.user_preference.user_location.address})
          </Text>
        </Card>
        
        <Card
          borderRadius="medium"
          maxWidth="20rem"
          variation="outlined"
          marginBottom="1rem"
        >
            <SelectField
              label="Travel Mode"
              descriptiveText="Select preferred mode of travel"
              value={inputData.user_preference.travel_mode}
              onChange={(e) => updateTravelModeProps(e.target.value)}
            >
              <option value="walking">walking</option>
              <option value="driving">driving</option>
              <option value="bicycling">bicycling</option>
              <option value="transit">transit</option>
            </SelectField>
          </Card>
      
        <Card
          borderRadius="medium"
          maxWidth="20rem"
          variation="outlined"
          marginBottom="1rem"
        >
          <Heading
            width='30vw'
            level={6} 
            marginBottom="0.5rem"
          >
             Constraints settings
          </Heading>
          <SliderField label="Distance"
            name="distance"
            min={1}
            max={50}
            step={1}
            value={inputData.user_preference.distance}
            onChange={(e) => updateDistanceProps(e)}
          />
          <SliderField label="Budget" 
            name="budget"
            min={10}
            max={500}
            step={1}
            value={inputData.user_preference.budget}
            onChange={(e) => updateBudgetProps(e)}
          />
        </Card>
        
        <Card
          borderRadius="medium"
          maxWidth="20rem"
          variation="outlined"
          marginBottom="1rem"
        >
          <Heading
            width='30vw'
            level={6} 
            marginBottom="0.5rem"
          >
             Dietary Restrictions
          </Heading>
          <CheckboxField
            name="kosher"
            value="kosher"
            checked={inputData.user_preference.dietary_restrictions.kosher}
            onChange={(e) => updateKosherProps(e.target.checked)}
            label="Kosher"
          />
          <CheckboxField
            name="pescatarian"
            value="pescatarian"
            checked={inputData.user_preference.dietary_restrictions.pescatarian}
            onChange={(e) => updatePescatarianProps(e.target.checked)}
            label="Pescatarian"
          />
          <CheckboxField
            name="no_red_meat"
            value="no_red_meat"
            checked={inputData.user_preference.dietary_restrictions.no_red_meat}
            onChange={(e) => updateNoRedMeatProps(e.target.checked)}
            label="No red meat"
          />
          <CheckboxField
            name="dairy_free"
            value="dairy_free"
            checked={inputData.user_preference.dietary_restrictions.dairy_free}
            onChange={(e) => updateDairyFreeProps(e.target.checked)}
            label="Dairy free"
          />
          <CheckboxField
            name="gluten_free"
            value="gluten_free"
            checked={inputData.user_preference.dietary_restrictions.gluten_free}
            onChange={(e) => updateGlutenFreeProps(e.target.checked)}
            label="Gluten free"
          />
        </Card>
      </form>
    );
}

        //<input type="submit" disabled={submitDisabled} value="Create grocery list" />
