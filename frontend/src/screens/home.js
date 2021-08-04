
import React, { useState, useEffect } from 'react';
import { Redirect, Route, Switch } from "react-router-dom";
import { Routes } from "../routes";

import Login from "./login.js";

import Preloader from "../components/preloader/preloader";
import Sidebar from "../components/sidebar/sidebar";
import Navbar from "../components/navbar/navbar";
import Footer from "../components/footer/footer";

// page
import Overview from "./oveview"
import Pnl from "./pnl"
import QaQc from "./qa_qc"
import DocumentClassify from './document_classify'
import isUserLogin from '../services/token'



const RouteWithSidebar = ({ component: Component, ...rest }) => {

  const [loaded, setLoaded] = useState(false);
  useEffect(() => {
    const timer = setTimeout(() => setLoaded(true), 1000);
    return () => clearTimeout(timer);
  }, []);

  const localStorageIsSettingsVisible = () => {
    return localStorage.getItem('settingsVisible') === 'false' ? false : true
  }

  const [showSettings, setShowSettings] = useState(localStorageIsSettingsVisible);

  const toggleSettings = () => {
    setShowSettings(!showSettings);
    localStorage.setItem('settingsVisible', !showSettings);
  }
  return (
      <Route {...rest} render={props => (
        <>
          <Preloader show={loaded ? false : true} />
          <Sidebar />
          <main className="content">
            <Navbar />
            <Component {...props} />
            <Footer toggleSettings={toggleSettings} showSettings={showSettings} />
          </main>
        </>
      )}
    />
  );
};


const RouteWithLoader = ({ component: Component, ...rest }) => {
    const [loaded, setLoaded] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => setLoaded(true), 1000);
        return () => clearTimeout(timer);
      }, []);

    return (
        <Route {...rest} render={props => ( 
          
        <><Preloader show={loaded ? false : true} /> <Component {...props} /> </> ) 

      } />
    );
};


export default () => (
    <Switch>
      <RouteWithLoader exact path={Routes.Login.path} component={Login} />
       { isUserLogin() === false ? <Redirect to={Routes.Login.path}/>: 
          <>
          <RouteWithSidebar exact path={Routes.Overview.path} component={Overview} />
          <RouteWithSidebar exact path={Routes.Pnl.path} component={Pnl} />
          <RouteWithSidebar exact path={Routes.QaQc.path} component={QaQc} />
          <RouteWithSidebar exact path={Routes.DocumentClassify.path} component={DocumentClassify} />
          </>
        }
      {/* <RouteWithSidebar exact path={Routes.DocumentClassify.path} component={DocumentClassify} />
      <RouteWithSidebar exact path={Routes.Overview.path} component={Overview} />
      <RouteWithSidebar exact path={Routes.Pnl.path} component={Pnl} />
      <RouteWithSidebar exact path={Routes.QaQc.path} component={QaQc} /> */}
    </Switch>
  );

