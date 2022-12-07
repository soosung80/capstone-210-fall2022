import { Card, Divider, View } from '@aws-amplify/ui-react';
import AddItem from './AddItem';
import ItemList from './ItemList';
import { useState } from 'react';
import { v4 as uuidv4 } from 'uuid';

export default function GroceryList(props) {
  const inputData = props.inputData;
  const setGroceryList = props.setGroceryList;
  const [items, setItems] = useState(JSON.parse(localStorage.getItem("shoppinglist")) || []);
  const [newItem, setNewItem] = useState("");
    
  const setAndSaveItems = (newItems) => {
    setItems(newItems);
    localStorage.setItem("shoppinglist", JSON.stringify(newItems));

    //create array of items for inputData
    let itemArr = [];
    for (let item in newItems) {
      itemArr.push(newItems[item].item);
    }
    setGroceryList(itemArr);
  }

  const addItem = (item) => {
    // increment item id or set it as 1
    const id = uuidv4();
    // create new item object
    const nextNewItem = { id: id, checked: false, item };
    // create new array to update state
    const listItems = [...items, nextNewItem];
    setAndSaveItems(listItems);
  }

  const handleCheck = (id) => {
    const listItems = items.map((item) => item.id === id ? { ...item, checked: !item.checked } : item);
    setAndSaveItems(listItems);
  }

  const handleDelete = (id) => {
    const listItems = items.filter((item) => item.id !== id);
    setAndSaveItems(listItems);
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    // check that there is something to submit
    if (!newItem) return;
    // addItem
    addItem(newItem);
    // set state back to empty
    setNewItem("");
  }

  return (
    <Card
      padding="0"
    >
      <Card
            borderRadius="medium"
            maxWidth="20rem"
            variation="outlined"
            marginBottom="1rem"
          > 
            Enter your grocery list 
      </Card>
      <Card 
        borderRadius="medium"
        maxWidth="20rem"
        variation="outlined"
        marginBottom="1rem"
      >
        <AddItem
          newItem={newItem}
          setNewItem={setNewItem}
          handleSubmit={handleSubmit}
        />
        <Divider
          orientation="horizontal" 
          marginTop="10px"
          marginBottom="10px"/>
        <ItemList
          items={items.filter(item => ((item.item).toLowerCase()))}
          handleCheck={handleCheck}
          handleDelete={handleDelete}
        />
      </Card>
    </Card>
  );
}