import "./permission.scss"
import { Toast } from '@themesberg/react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudUploadAlt, faPlus } from '@fortawesome/free-solid-svg-icons';
import { Col, Row, Button, Dropdown } from '@themesberg/react-bootstrap';

import React, { useState } from 'react';
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


export default () => {
    return (
        <>
            <div>
                <Row className="justify-content-md-center">
                    <Col xs = {12} m={6}  xl={4} className="mb-4">
                        <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                            <Toast.Header className="text-primary" closeButton={false}>
                                <FontAwesomeIcon icon={faBootstrap} />
                                <strong className="me-auto ms-2">Permission Denied</strong>
                                <small>{nowTime}</small>
                                <Button variant="close" size="xs" onClick={handleCloseDefault} />
                            </Toast.Header>
                            <Toast.Body>
                                {loading === true? <HourGlass size={10} color="#00bfff" sizeUnit="px" /> : ""}
                                {/* <Form>
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
                                
                                </Form> */}
                    
                
                            </Toast.Body>
                        </Toast>
                    </Col>
                </Row>
            </div>
        </>
    )
}