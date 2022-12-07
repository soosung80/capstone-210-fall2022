import { useRef, useEffect } from "react";

const AutoComplete = ({updateUserLocProps}) => {
   const autoCompleteRef = useRef();
   const inputRef = useRef();
   const options = {
    componentRestrictions: { country: "us" },
    fields: ["place_id", "geometry", "name", "formatted_address"],
    types: ["address"]
   };
   
   useEffect(() => {
     autoCompleteRef.current = new window.google.maps.places.Autocomplete(
     inputRef.current,
     options
    );
     autoCompleteRef.current.addListener("place_changed", async function () {
     const place = await autoCompleteRef.current.getPlace().geometry.location;
     const address = await autoCompleteRef.current.getPlace().formatted_address;
     updateUserLocProps(place.lat(), place.lng(), address);
    });
   }, []);
   return (
    <div>
     <label>Enter your starting address:</label>
     <input ref={inputRef} />
    </div>
   );
};
export default AutoComplete;

// this is from: https://www.telerik.com/blogs/integrating-google-places-autocomplete-api-react-app