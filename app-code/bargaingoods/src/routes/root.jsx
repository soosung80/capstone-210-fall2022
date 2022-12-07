import { Outlet } from "react-router-dom";

export default function Root() {
  
  return (
    <>
      <div id="sidebar">
        <h1>Bargain Goods</h1>
        <nav>
          <ul>
            <li>
              <a href={`inputs`}>Enter preferences and grocery list</a>
            </li>
          </ul>
        </nav>
      </div>
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}
/*
            <li>
              <a href={`map-test`}>Map Test</a>
            </li>*/