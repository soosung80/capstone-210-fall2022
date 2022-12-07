import React, { useState, useEffect } from "react";
import { Flex } from '@aws-amplify/ui-react';
import { MagnifyingGlass } from 'react-loader-spinner';

import Modal from 'react-modal';

import GroceryList from './../components/GroceryList';
import {UserPreferences} from './../components/UserPreferences';
import Outputs from './../pages/Outputs';

const Inputs = () => {
    // *** default settings for user preference and empty grocery list *** //
    const initialState = {
        user_preference: {
            user_location: {
              lat: 40.76104711377761,
              lng: -73.98332121025068,
              address: "New York, New York"
            },
            travel_mode: "walking",
            distance: 2,
            budget: 20,
            dietary_restrictions: {
              kosher: false,
              pescatarian: false,
              no_red_meat: false,
              dairy_free: false,
              gluten_free: false
            }
          },
          groceries: []
      };
    
    // *** error message modal states *** //
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [errorMessage, setErrorMessage] = useState("Something went wrong. Please try again a little later.");
    
    // *** State handler for API call ***
    const [outputData, setOutputData] = useState();
    const [waitingForOutput, setWaitingForOutput] = useState(false);
    
    // only disable when waiting for location lookup
    const [submitDisabled, setSubmitDisabled] = React.useState(false);
    
    // *** API endpoint for the model ***
    const apiEndpoint = "https://2h18j1m48b.execute-api.us-east-1.amazonaws.com/default/BargainGoodsModel";
    //const apiEndpoint = "https://cors-anywhere.herokuapp.com/https://2h18j1m48b.execute-api.us-east-1.amazonaws.com/default/BargainGoodsModel";
    //const apiEndpoint = "	https://3hwp8zcowj.execute-api.us-east-1.amazonaws.com/default/hello"
    
    // *** if there's anything saved locally, get that, otherwise set to initial state json *** 
    const [inputData, setInputData] = useState(JSON.parse(localStorage.getItem("inputData")) || initialState);

    // *** Methods for updating props (one per user pref and the grocery list) *** //
      useEffect(() => {
        localStorage.setItem("inputData", JSON.stringify(inputData));
      }, [inputData]);
    
    const updateDistanceProps = (distance) => {
        
        setInputData(current => {
          // using spread syntax (...)
          const user_preference = {...current.user_preference};
          
          user_preference.distance = distance;
    
          return {...current, user_preference};
        });
    }
    
    const updateTravelModeProps = (travel_mode) => {
      setInputData(current => {
          // using spread syntax (...)
          const user_preference = {...current.user_preference};
          
          user_preference.travel_mode = travel_mode;
    
          return {...current, user_preference};
        });
    }
    
    const updateBudgetProps = (budget) => {

        setInputData(current => {
          // using spread syntax (...)
          const user_preference = {...current.user_preference};
          
          user_preference.budget = budget;
    
          return {...current, user_preference};
        });
    }
    
    const updateUserLocProps = (lat, lng, address) => {
      console.log(lat, lng);
        setInputData(current => {
          // using spread syntax (...)
      
          return {
            ...current,
            user_preference: {
              ...current.user_preference,
              
              user_location: {
                ...current.user_preference.user_location,
                 // override value for nested country property
                lat: lat,
                lng: lng,
                address: address
              }
            },
          };
        });
    }
    
    const updateKosherProps = (kosher) => {
        setInputData(current => {
          // using spread syntax (...)
      
          return {
            ...current,
            user_preference: {
              ...current.user_preference,
              
              dietary_restrictions: {
                ...current.user_preference.dietary_restrictions,
                 // override value for nested country property
                kosher: kosher
              }
            },
          };
        });
    }
    
    const updatePescatarianProps = (pescatarian) => {
        setInputData(current => {
          // using spread syntax (...)
      
          return {
            ...current,
            user_preference: {
              ...current.user_preference,
              
              dietary_restrictions: {
                ...current.user_preference.dietary_restrictions,
                 // override value for nested country property
                pescatarian: pescatarian
              }
            },
          };
        });
    }
    
    const updateNoRedMeatProps = (no_red_meat) => {
        setInputData(current => {
          // using spread syntax (...)
      
          return {
            ...current,
            user_preference: {
              ...current.user_preference,
              
              dietary_restrictions: {
                ...current.user_preference.dietary_restrictions,
                 // override value for nested country property
                no_red_meat: no_red_meat
              }
            },
          };
        });
    }
    
    const updateDairyFreeProps = (dairy_free) => {
        setInputData(current => {
          // using spread syntax (...)
      
          return {
            ...current,
            user_preference: {
              ...current.user_preference,
              
              dietary_restrictions: {
                ...current.user_preference.dietary_restrictions,
                 // override value for nested country property
                dairy_free: dairy_free
              }
            },
          };
        });
    }
    
    const updateGlutenFreeProps = (gluten_free) => {
        setInputData(current => {
          // using spread syntax (...)
      
          return {
            ...current,
            user_preference: {
              ...current.user_preference,
              
              dietary_restrictions: {
                ...current.user_preference.dietary_restrictions,
                 // override value for nested country property
                gluten_free: gluten_free
              }
            },
          };
        });
    }
    
    const updateGroceriesProps = (groceries) => {
      setInputData(current => {
        // using spread syntax (...)
    
        return {
          ...current,
          groceries: groceries 
        };
      });
    }

    // *** EVENT HANDLERS ***
    
    // *** error methods *** //
    const handleError = (errorMsg) => {
      setIsModalOpen(true);
      setErrorMessage(errorMsg);
    };
  
    const handleCloseModal = () => {
      setIsModalOpen(false);
    };
    
    // *** submit method *** //
    const handleClick = e => {
      
      if (inputData.groceries.length === 0) {
        handleError("Please enter at least one grocery item.");
        return;
      }
      setWaitingForOutput(true);
       
       // Call the API with the JSON data
      fetch(apiEndpoint, { /* global fetch */
        method: 'POST',
        //mode: 'no-cors',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputData)
      })
        .then(response => {
          return response.text();
          })
        .then(data => {
          setWaitingForOutput(false);
          // use eval because we trust the source and because NaN causes json parse failure.
          let jsondata = eval('('+data+')');
          
          // check for -777 for no input grocery, -888 for low limit for distance, -999 for low limit for budget
          if(jsondata.length <= 0) {
            handleError("No stores matched your criteria, please adjust your preferences and try again.");
          }
          else if (jsondata[0].lat === -777) {
            handleError("Please enter at least one grocery item.");
          }
          else if (jsondata[0].lat === -888) {
            handleError("No store matched your distance criteria. Please adjust the limit and try again.");
          }
          else if (jsondata[0].lat === -999) {
            handleError("No stores matched budget criteria. Please adjust the limit and try again.");
          }
          else {
            setOutputData({ jsondata });
          }
        })
        .catch((error) => {
          handleError("there was an error calling the model api: " + error);
          setWaitingForOutput(false);
        });
    };
    
    
    // *** RETURN ***
    
/*    return (
      <>
        {waitingForOutput && !outputData && 
          <FallingLines
            color="#4fa94d"
            width="200"
            visible={true}
            ariaLabel='falling-lines-loading'
          />
        }
        {!waitingForOutput && outputData && 
          <Outputs outputData={outputData} inputdata={inputData} />
        }
        {!waitingForOutput && !outputData && 
          <div>
              <Flex
                direction="row"
                justifyContent="flex-start"
                alignItems="stretch"
                alignContent="flex-start"
                wrap="nowrap"
                gap="1rem"
              >
                  <UserPreferences 
                      inputData={inputData}
                      updateDistanceProps={updateDistanceProps}
                      updateBudgetProps={updateBudgetProps}
                      updateUserLocProps={updateUserLocProps}
                      updateKosherProps={updateKosherProps}
                      updatePescatarianProps={updatePescatarianProps}
                      updateNoRedMeatProps={updateNoRedMeatProps}
                      updateDairyFreeProps={updateDairyFreeProps}
                      updateGlutenFreeProps={updateGlutenFreeProps}
                  />
                      
                  <GroceryList 
                      setGroceryList={setGroceryList}
                      grocerylist={groceryList}
                  />
              </Flex>
              <button onClick={handleClick}>Find stores for my groceries</button>
          </div>
        }
      </>);*/

    if (waitingForOutput && !outputData) {
      // show a loading indicator here
      return <MagnifyingGlass
                visible={true}
                height="150"
                width="150"
                ariaLabel="MagnifyingGlass-loading"
                wrapperStyle={{}}
                wrapperClass="MagnifyingGlass-wrapper"
                glassColor = '#c0efff'
                color = 'green'
              />
    }
    else if (!waitingForOutput && outputData) {
        return <Outputs outputData={outputData} inputData={inputData} />;
    }
    else {
       return (
        <div>
            <Flex
              direction="row"
              justifyContent="flex-start"
              alignItems="stretch"
              alignContent="flex-start"
              wrap="nowrap"
              gap="1rem"
            >
                <UserPreferences 
                    inputData={inputData}
                    updateDistanceProps={updateDistanceProps}
                    updateBudgetProps={updateBudgetProps}
                    updateUserLocProps={updateUserLocProps}
                    updateKosherProps={updateKosherProps}
                    updatePescatarianProps={updatePescatarianProps}
                    updateNoRedMeatProps={updateNoRedMeatProps}
                    updateDairyFreeProps={updateDairyFreeProps}
                    updateGlutenFreeProps={updateGlutenFreeProps}
                    updateTravelModeProps={updateTravelModeProps}
                    setSubmitDisabled={setSubmitDisabled}
                />
                    
                <GroceryList 
                    setGroceryList={updateGroceriesProps}
                    inputData={inputData}
                />
            </Flex>
            <button onClick={handleClick} isdisabled={submitDisabled.toString()}>Find stores for my groceries</button>
            <Modal isOpen={isModalOpen} onRequestClose={handleCloseModal} ariaHideApp={false}>
              <h3>{errorMessage}</h3>
              <button onClick={handleCloseModal}>Close</button>
            </Modal>
        </div>
       );
    }
};

export default Inputs;