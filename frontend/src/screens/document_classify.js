
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Col, Row, Button, Dropdown } from '@themesberg/react-bootstrap';

import React, { useState, useEffect, useReducer } from 'react';
import { Toast } from '@themesberg/react-bootstrap';
import { faBootstrap } from '@fortawesome/free-brands-svg-icons';
import {  faPlus, faBoxes, faBookMedical} from "@fortawesome/free-solid-svg-icons";

import "react-datepicker/dist/react-datepicker.css";
import { Form } from '@themesberg/react-bootstrap';
import Lightbox from 'react-image-lightbox';
import DefaulImage from '../assets/img/default-image.png'
import  UploadService from '../services/upload' 


import documentClassifyPDF from "../assets/pdf/document.pdf";
import AllPagesPDFViewer from "../components/pdf/all-pages"


import axios from "axios";
export const BASE_URL = process.env.REACT_APP_API_V1


export default () => {
  const [roleCheck, setRoleCheck] = useState(false)
  const [showDefault, setShowDefault] = useState(true);
  
  // define status of pages int voi prediction
  const [status, setStatus] = useState('predict')

  const [fileObject, setFileObject] = useState(undefined);
  const [urlFileObject, seturlFileObject] = useState(DefaulImage);
  const [alertStatus, setAlertStatus] = useState("")
  const [alertDescription, setAlertDescription] = useState("")
  const [preProcessing, setPreProcessing] = useState(DefaulImage)
  const [classId, setClassId] = useState(null)
  const [className, setClassName] = useState(null)
  const [score, setScore] = useState(null)


  function handleCloseDefault(){setShowDefault(false)}


  function onChangeInput(e){
    setPreProcessing(DefaulImage)

    e.preventDefault();
    var file = e.target.files[0]
    if (file === undefined) {}
    else if ((file.type === "image/jpeg") || (file.type === "image/png")) {
      setFileObject(file)
      seturlFileObject(URL.createObjectURL(file))
    }
    else{
      setAlertStatus("danger")
      setAlertDescription("Just support for .png and .jpeg!")
    }
  };

  function preDictImage() {
    UploadService.uploadDocumentClassify(fileObject, (event) => {
    })
      .then((response) => {
        if (response.status === 200) {
          console.log(response)
          setPreProcessing(response.data.pre_url)
          setScore(response.data.score)
          setClassId(response.data._id)
          setClassName(response.data.name)
        }
        else {

        }
      })
      .catch(() => {
       

      });      
  }



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
            if (['superuser'].indexOf(item) > -1){
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
  // if (roleCheck === false)

    return (
      <>
        <div className="d-flex flex-wrap flex-md-nowrap align-items-center pds-top-20">
          <Dropdown className="btn-toolbar">
            <Dropdown.Toggle as={Button} variant="primary" size="sm" className="me-2" onClick={() => setStatus('predict')}>
              <FontAwesomeIcon icon={faBoxes} className="me-2" />Prediction
            </Dropdown.Toggle>
          </Dropdown>
          <Dropdown className="btn-toolbar">
            <Dropdown.Toggle as={Button} variant="primary" size="sm" className="me-2"  onClick={() => setStatus('manager')}>
              <FontAwesomeIcon icon={faPlus} className="me-2" />Management
            </Dropdown.Toggle>
          </Dropdown>
          <Dropdown className="btn-toolbar">
            <Dropdown.Toggle as={Button} variant="primary" size="sm" className="me-2" onClick={() => setStatus('document')}> 
              <FontAwesomeIcon icon={faBookMedical} className="me-2" />Documentation
            </Dropdown.Toggle>
          </Dropdown>
        </div>
        {status === 'predict' ? 
         <Row>
          <Col xs={12} xl={12} className="mb-4">
            <Row>
              <Col xs={12} xl={8} className="mb-4">
                <Row>
    

                  <Col xs={12} lg={6} className="mb-4">
                    <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                      <Toast.Header className="text-primary" closeButton={false}>
                        <FontAwesomeIcon icon={faBootstrap} />
                        <strong className="me-auto ms-2">Select Image</strong>
                      </Toast.Header>
                      <Toast.Body>
                        <Form.Group className="mb-3">
                          <Form.Label>Select File</Form.Label>
                          <Form.Control type='file' onChange={(e) => onChangeInput(e)}/>
                        <div className='mgs-right-5'>
                          <Button variant="secondary" className="m-1 width-100-per" onClick={preDictImage}>Predict</Button>
                        </div>
                        </Form.Group> 
                          <img className='width-100-per' src={urlFileObject}></img>
                      </Toast.Body>
                    </Toast>
                  </Col>

                  <Col xs={12} lg={6} className="mb-4">
                    <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                      <Toast.Header className="text-primary" closeButton={false}>
                        <FontAwesomeIcon icon={faBootstrap} />
                        <strong className="me-auto ms-2">Image Processing</strong>
                      </Toast.Header>
                      <Toast.Body>
                        <div className='pds-bottom-15'>
                          Description: Using Opencv for pre-procssing image
                          <li className='pds-top-5'>1. Binarization</li>
                          <li className='pds-top-5'>2. Skew Correction</li>
                          <li className='pds-top-5'>3. Noise Removal</li>
                          <li className='pds-top-5'>4. Thinning and Skeletonization</li>

                        </div>
                        <img src={preProcessing}></img>
                      </Toast.Body>
                    </Toast>
                  </Col>
                </Row>
              </Col>

              <Col xs={12} xl={4}>
                <Row>
                  <Col xs={12} className="mb-4">
                    <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                      <Toast.Header className="text-primary" closeButton={false}>
                        <FontAwesomeIcon icon={faBootstrap} />
                        <strong className="me-auto ms-2">Description Classification</strong>
                      </Toast.Header>
                      <Toast.Body>
                        <div className='pds-bottom-15'>
                          Description: Using tesseract, phobert and elasticsearch for classify
                          <li className='pds-top-5'>1. Tesseract get text from image</li>
                          <li className='pds-top-5'>2. Phobert base Bert Model cover text to tensor, dim</li>
                          <li className='pds-top-5'>3. Elasticsearch with similarity search (enhance by Bert search)</li>
                          <li className='pds-top-5'>4. Calculator score and return Output</li>
                        </div>
                      </Toast.Body>
                    </Toast>
                  </Col>
                  <Col xs={12} className="mb-4">
                    <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                      <Toast.Header className="text-primary" closeButton={false}>
                        <FontAwesomeIcon icon={faBootstrap} />
                        <strong className="me-auto ms-2">Result Classification</strong>
                      </Toast.Header>
                      <Toast.Body>
                        <div className='pds-bottom-15'>
                          <li className='pds-top-5'>Class Id: {classId}</li>
                          <li className='pds-top-5'>Class Name: {className}</li>
                          <li className='pds-top-5'>Score: {score}</li>
                        </div>
                      </Toast.Body>
                    </Toast>
                  </Col>
                 
                </Row>
              </Col>
            </Row>
          </Col>
        </Row>
         : status === 'document' ? 
            
         <Row className="justify-content-md-center">
         <Col xs={12} className="mb-4 d-none d-sm-block">
         {/* <div className="width-100-per">
              <AllPagesPDFViewer pdf={documentClassifyPDF} />
            </div> */}
            <div className="width-100-per pds-top-20">
                <iframe
                        style={{ width: "100%", height: "auto", minHeight: "1100px",  overflow:'hidden'}}
                        src={documentClassifyPDF}
                        type='application/pdf'
                        title='title'
                      />
            </div>
         </Col>
         </Row>
         : <div>
           <Toast show={showDefault} onClose={handleCloseDefault} className="my-3 width-700">
                      <Toast.Header className="text-primary" closeButton={false}>
                        <FontAwesomeIcon icon={faBootstrap} />
                        <strong className="me-auto ms-2">Notification</strong>
                      </Toast.Header>
                      <Toast.Body>
                        This feature has not been implemented yet. sorry for this inconvenience!
                      </Toast.Body>
                    </Toast>
           </div>
        }
      </>

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
