
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudUploadAlt, faPlus } from '@fortawesome/free-solid-svg-icons';
import { Col, Row, Button, Dropdown } from '@themesberg/react-bootstrap';

import React, { useState, useEffect } from 'react';
import { Toast } from '@themesberg/react-bootstrap';
import { faBootstrap } from '@fortawesome/free-brands-svg-icons';
import Progress from "../components/progress/progress";
import { Form } from '@themesberg/react-bootstrap';
import { Alert } from '@themesberg/react-bootstrap';
import  UploadService from '../services/upload' 
import Moment from 'moment';
import DatePicker from 'react-datepicker'
import "react-datepicker/dist/react-datepicker.css";
import HourGlass from "../components/loading/hour-glass";

import axios from "axios";
export const BASE_URL = process.env.REACT_APP_API_V1

export default () => {
  const [showDefault, setShowDefault] = useState(true);
  const [fileObject, setFileObject] = useState(undefined);
  const [password, setPassword] = useState("");
  const [verifyPassword, setVerifyPassword] = useState("");
  const [sheetName, setSheetName] = useState("");
  const [showAlert, setShowAlert] = useState(false) 
  const [alertStatus, setAlertStatus] = useState("")
  const [alertDescription, setAlertDescription] = useState("")
  const [progress, setProgress] = useState(0);
  const nowTime = Moment(Date.now()).format('YYYY-MM-DD')
  const [loading, setLoading] = useState(false);
  const [startDate, setStartDate] = useState(new Date());
  const [roleCheck, setRoleCheck] = useState(false)

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
            if (['superuser', 'pnl'].indexOf(item) > -1){
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

  function handleCloseDefault(){
    setShowDefault(false)
  }

  function onChangeInput(e){
    e.preventDefault();
    var file = e.target.files[0]
    if (file === undefined) {}
    else if ((file.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") || (file.type === "application/vnd.ms-excel")) {
      setShowAlert(false)
      setFileObject(file)
    }
    else{
      setShowAlert(true)
      setAlertStatus("danger")
      setAlertDescription("Just support for .xlsx and .xls!")
    }
  }

  function uploadFile(){
    setLoading(true)
    if (fileObject === undefined) {
      setLoading(false)
      setShowAlert(true)
      setAlertStatus("danger")
      setAlertDescription("missing file!")
    }else if (password === "" || verifyPassword === ""){
      setLoading(false)
      setShowAlert(true)
      setAlertStatus("danger")
      setAlertDescription("missing password!")
    }else if (sheetName === ""){
      setLoading(false)
      setShowAlert(true)
      setAlertStatus("danger")
      setAlertDescription("missing sheetname!")
    }
    else if (password !== verifyPassword){
      setLoading(false)
      setShowAlert(true)
      setAlertStatus("danger")
      setAlertDescription("pass not match!")
    }
    else {
      let month = startDate.getMonth() + 1
      let year = parseInt(startDate.getFullYear())
      setProgress(0);
      UploadService.uploadNas(fileObject, password, sheetName, month, year, (event) => {
      })
        .then((response) => {
          if (response.status === 200) {
            setLoading(false)
            setProgress(100)
            setShowAlert(true)
            setAlertStatus("success")
            setAlertDescription("completed!")
          }
          else {
            setLoading(false)
            setShowAlert(true)
            setProgress(0)
            setAlertStatus("danger")
            setAlertDescription(response.statusText)
          }
        })
        .catch(() => {
          setLoading(false)
          setShowAlert(true)
          setProgress(0);
          setAlertStatus("danger")
          setAlertDescription("error")

        });      
    }
    setFileObject(undefined)
    setPassword("")
    setVerifyPassword("")
    setSheetName("")
  }

    if (roleCheck === true)
      return (
        <>
          <div className="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center py-4">
            <Dropdown className="btn-toolbar">
              <Dropdown.Toggle as={Button} variant="primary" size="sm" className="me-2">
                <FontAwesomeIcon icon={faPlus} className="me-2" />New Task
              </Dropdown.Toggle>
              <Dropdown.Menu className="dashboard-dropdown dropdown-menu-left mt-2">
                <Dropdown.Item className="fw-bold" onClick={() => setShowDefault(true)}>
                  <FontAwesomeIcon icon={faCloudUploadAlt} className="me-2"/> Upload Files
                </Dropdown.Item>
                <Dropdown.Divider />
              </Dropdown.Menu>
            </Dropdown>

            </div>
            <div>
            <Row className="justify-content-md-center">
              <Col xs = {12} m={6}  xl={4} className="mb-4">
                <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                    <Toast.Header className="text-primary" closeButton={false}>
                        <FontAwesomeIcon icon={faBootstrap} />
                        <strong className="me-auto ms-2">Upload Pnl</strong>
                        <small>{nowTime}</small>
                        <Button variant="close" size="xs" onClick={handleCloseDefault} />
                    </Toast.Header>
                    <Toast.Body>
                      {loading === true? <HourGlass size={10} color="#00bfff" sizeUnit="px" /> : ""}
                      <Form>
                        {showAlert === true ? 
                          <Alert variant={alertStatus}>
                            {alertDescription}
                          </Alert> : ""
                        }
                        <Form.Group className="mb-3">
                          <Form.Label>Select File</Form.Label>
                          <Form.Control type='file' onChange={(e) => onChangeInput(e)}/>
                        </Form.Group> 
                        <Form.Group className="mb-3">
                          <Form.Label>Sheet Name</Form.Label>
                          <Form.Control type="input"  placeholder={sheetName !== "" ? null : "Enter Sheet Name"} onChange={(e) => setSheetName(e.target.value)} value={sheetName}/>
                        </Form.Group> 
                        <Form.Group className="mb-3">
                          <Form.Label>Password</Form.Label>
                          <Form.Control type="password" placeholder={password !== "" ? null : "Enter Password"}  onChange={(e) => setPassword(e.target.value)} value={password}/>
                        </Form.Group> 
                        <Form.Group className="mb-3">
                        <Form.Label>Password Again</Form.Label>
                          <Form.Control type="password" placeholder={verifyPassword !== "" ? null : "Enter Verify Password"} onChange={(e) => setVerifyPassword(e.target.value)} value={verifyPassword}/>
                        </Form.Group>
                        <Form.Group className="mb-3">
                          <Form.Label>Select Month</Form.Label>
                          <div  className="myContainter" >
                          <DatePicker  className="myDatePicker"
                                selected={startDate}
                                onChange={(date) => setStartDate(date)}
                                dateFormat="MM/yyyy"
                                showMonthYearPicker
                                fixedHeight
                            />
                        </div> 
                        </Form.Group>
                        <Button variant="secondary" className="m-1 width-200" onClick={uploadFile}>Upload</Button>
                        
                      </Form>
                      
                      <Progress variant="primary" label="" value={progress} />
                    </Toast.Body>
                </Toast>
              </Col>
            </Row>
            </div>
            <div className='pds-bottom-100'></div>

          </>
        );
  else return (<>
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
