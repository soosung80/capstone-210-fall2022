import MapStores from './../components/MapStores';
import ListStores from './../components/ListStores';

const Outputs = (props) => {
    const outputData = props.outputData.jsondata;
    const inputData = props.inputData;

    console.log(outputData);
    
   return (
    <div>
        <ListStores stores={outputData} />
        <MapStores stores={outputData} userLoc={inputData}/>
    </div>
   );
};

export default Outputs;