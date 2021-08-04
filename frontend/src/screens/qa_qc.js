
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Col, Row, Button, Dropdown } from '@themesberg/react-bootstrap';

import React, { useState, useEffect } from 'react';
import { Toast } from '@themesberg/react-bootstrap';
import { faBootstrap } from '@fortawesome/free-brands-svg-icons';
import "react-datepicker/dist/react-datepicker.css";


import axios from "axios";
export const BASE_URL = process.env.REACT_APP_API_V1


export default () => {
  const [roleCheck, setRoleCheck] = useState(false)
  const [showDefault, setShowDefault] = useState(true);
  function handleCloseDefault(){setShowDefault(false)}

  useEffect(() => {
    const token = localStorage.getItem("accessToken")
    axios({
      method: "get",
      url: BASE_URL + "account/role/role-name",
      headers: { "Content-Type": "application/json" , "Authorization": "Bearer " + token,},
    }).then(response => {
        let check = false
        if (response.status === 200){
          const data = response.data
          data.every(item =>{
            if (['superuser', 'qa/qc'].indexOf(item) > -1){
              check = true
              return false
            }
            else return true
          })
        }
        setRoleCheck(check)
      }).catch(err => {
        console.log(err);
      });
  });
  if (roleCheck === true)
    return (
      <></>
    );
  else return (
    <>
      <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4">
        <Row className="justify-content-md-center">
        <Col xs = {12} m={6}  xl={4} className="mb-4">
          <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
            <Toast.Header className="text-primary" closeButton={false}>
              <FontAwesomeIcon icon={faBootstrap} />
              <strong className="me-auto ms-2">Notification</strong>
            </Toast.Header>
            <Toast.Body> permission denied!
            </Toast.Body>
          </Toast>
        </Col>
        </Row>
        </div>
      </>);
}
