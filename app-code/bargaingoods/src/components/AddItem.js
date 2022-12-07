import React from "react";

export default function AddItem({ newItem, setNewItem, handleSubmit }) {

  return (
    <>
    <form className="inputBlock"  onSubmit={handleSubmit}>
      <input 
        spellCheck="true"
        type="text" 
        id="grocery_item" 
        name="grocery_item" 
        required
        minLength="4" 
        onChange={(e) => setNewItem(e.target.value)}
      />
      <button type="submit">ADD</button>
      </form>
    </>
    
  );
}