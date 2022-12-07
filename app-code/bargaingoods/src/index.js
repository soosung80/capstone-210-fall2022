import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import "./index.css";

import ErrorPage from "./pages/ErrorPage";
import Root from "./routes/root";
import MapStores from "./components/MapStores";
import GroceryList from "./components/GroceryList";
import StoreList from "./components/StoreList";
import Inputs from "./pages/Inputs";
import Outputs from "./pages/Outputs";
import Maps from './components/Map';


import reportWebVitals from './reportWebVitals';

import { Amplify } from 'aws-amplify';
import awsExports from './aws-exports';
Amplify.configure(awsExports);


const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "inputs",
        element: <Inputs />
      },
      {
        path: "create-list",
        element: <GroceryList />
      },
      {
        path: "outputs",
        element: <Outputs />
      },
      {
        path: "map",
        element: <MapStores />
      },
      {
        path: "store-list",
        element: <StoreList />
      },
      {
        path: "map-test",
        element: <Maps />
      }
    ]
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
