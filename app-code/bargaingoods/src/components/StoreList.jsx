import React from 'react';
import {useNavigate, useLocation} from 'react-router-dom';

import { Table, TableHead, TableRow, TableCell, TableBody, Card } from '@aws-amplify/ui-react';
import { Amplify } from 'aws-amplify';


import '@aws-amplify/ui-react/styles.css';

import awsExports from './../aws-exports';

Amplify.configure(awsExports);

export default function StoreList(props) {
  
  const location = useLocation()
  //const {store, total, groceries} = location.state;
  const store = props.storeName;
  const total = props.total;
  const groceries = props.groceries;
  
  const navigate = useNavigate();

  let altTotal = 0;
  
  for (let i in groceries){
    altTotal = altTotal + groceries[i].alternative_price;
  }
  
  return (
    <>
      <Card>
        <label>{store}</label>
        <Table
          caption=""
          highlightOnHover={false}
          variation="bordered"
        >
          <TableHead>
            <TableRow>
              <TableCell as="th">Item</TableCell>
              <TableCell as="th">Price</TableCell>
              <TableCell as="th">Alternative</TableCell>
              <TableCell as="th">Alternative Price</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {groceries.map((item, i) => (
              <TableRow key={i}>
                <TableCell>{item.item_name}</TableCell>
                <TableCell>{item.price}</TableCell>
                <TableCell>{item.alternative}</TableCell>
                <TableCell>{item.alternative_price}</TableCell>
              </TableRow>
             ))}
             <TableRow>
              <TableCell as="th">Total</TableCell>
              <TableCell as="th">{total}</TableCell>
              <TableCell as="th">Total</TableCell>
              <TableCell as="th">{altTotal.toFixed(2)}</TableCell>
             </TableRow>
          </TableBody>
        </Table>
      </Card>
    </>

  );
}