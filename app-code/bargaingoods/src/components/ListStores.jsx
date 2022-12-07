import { useState } from "react";
import Modal from 'react-modal';

import { Button, Table, TableHead, TableRow, TableCell, TableBody } from '@aws-amplify/ui-react';
import { Link } from "react-router-dom";
import StoreList from './../components/StoreList';

export default function ListStores(props) {
    const stores = props.stores;
    let storeList = [];
     // limit output to top 5 stores
    
    if (stores.length > 5) {
        storeList = stores.slice(0, 5);
    }
    
    // *** modal states *** //
    const [isModalOpen, setIsModalOpen] = useState(false);
    //storeName={store_name} total={total} groceries={groceries}
    const [storeName, setStoreName] = useState("");
    const [total, setTotal] = useState("");
    const [groceries, setGroceries] = useState([]);

    
    // *** modal methods *** //
    const handleModal = (index) => {
      console.log(storeList[index]);
      
      setStoreName(storeList[index].store_name);
      setTotal(storeList[index].total);
      setGroceries(storeList[index].grocery_list);
      setIsModalOpen(true);
    };
  
    const handleCloseModal = () => {
      setIsModalOpen(false);
    };
    
    return (
        <>
          <Table
            caption=""
            highlightOnHover={false}>
            <TableHead>
              <TableRow>
                <TableCell as="th">Store name</TableCell>
                <TableCell as="th">Distance</TableCell>
                <TableCell as="th">Total Price</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {storeList.map((item, i) => (
                <TableRow key={i}>
                  
                  <TableCell>
                    <Link onClick={() => handleModal(i)}>{item.store_name}</Link>
                  </TableCell>
                  
                  <TableCell>{item.distance}mi</TableCell>
                  <TableCell>${item.total}</TableCell>
                </TableRow>
               ))}
            </TableBody>
          </Table>
          <Modal isOpen={isModalOpen} onRequestClose={handleCloseModal} ariaHideApp={false}>
            <StoreList storeName={storeName} total={total} groceries={groceries}/>
            <button onClick={handleCloseModal}>Close</button>
          </Modal>
        </>
    );
}