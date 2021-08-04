import React from 'react';
import ReactDOM from 'react-dom';
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import './index.css';

// core styles
import "./styles/scss/volt.scss";

// vendor styles
import "@fortawesome/fontawesome-free/css/all.css";
import "react-datetime/css/react-datetime.css";


import Home from './screens/home.js'
import ScrollToTop from "./components/scoll/scoll_top";
import { HashRouter } from "react-router-dom";



ReactDOM.render(
  <HashRouter>
    <ScrollToTop />
    <Home />
  </HashRouter>,
  document.getElementById("root")
);


