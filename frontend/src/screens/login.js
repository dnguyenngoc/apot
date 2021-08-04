import React, { Component } from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleLeft, faEnvelope, faUnlockAlt } from "@fortawesome/free-solid-svg-icons";
import { Col, Row, Form, Card, Button, FormCheck, Container, InputGroup } from '@themesberg/react-bootstrap';
import { Link } from 'react-router-dom';
import loginAccessToken from "../services/account"
import { Routes } from "../routes";
// import isUserLogin from '../services/token'

class Login extends Component {
    constructor(props) {
    super(props);
      this.state = {
        username: undefined,
        password: undefined,
        isRemember: false,
        isLogin: false,
        from: '/',
      }
      this.handleLogin = this.handleLogin.bind(this)
      this.handleChangeEmail = this.handleChangeEmail.bind(this)
      this.handleChangePassword = this.handleChangePassword.bind(this)
      this.handleChangeRemember = this.handleChangeRemember.bind(this)
    }
    componentDidMount(){
      console.log(this.state.isLogin)
      if (this.check === true){
        this.setState({isLogin: true})
        window.location.href = "/operation/pnl"
      }
    }
    handleLogin(){
      if (this.state.username !== undefined && this.state.password !== undefined){
        const isLogin = loginAccessToken(this.state.username, this.state.password, this.state.isRemember, this.state.from);
        this.setState({isLogin: isLogin})
      }
    }

    handleChangeEmail(e){this.setState({username: e.target.value},)}
    handleChangePassword(e){this.setState({password: e.target.value},)}
    handleChangeRemember(e){
      if (this.state.isRemember === false) this.setState({isRemember: true})
      else this.setState({isRemember: false})
    }
    render() {
       return (
            <main>
              <section className="d-flex align-items-center my-5 mt-lg-6 mb-lg-5 padding-top">
                <Container>
                  <Row className="justify-content-center form-bg-image" style={{ backgroundImage: `url("${""}")` }}>
                    <Col xs={12} className="d-flex align-items-center justify-content-center">
                      <div className="bg-white shadow-soft border rounded border-light p-4 p-lg-5 w-100 fmxw-500">
                        <div className="text-center text-md-center mb-4 mt-md-0">
                          <h3 className="mb-0">Sign in to platform</h3>
                        </div>
                        <Form className="mt-4">
                          <Form.Group id="email" className="mb-4">
                            <Form.Label>Your Email</Form.Label> 
                            <InputGroup>
                              <InputGroup.Text>
                                <FontAwesomeIcon icon={faEnvelope} />
                              </InputGroup.Text>
                              <Form.Control autoFocus required type="email" placeholder="example@company.com" onChange={this.handleChangeEmail}/>
                            </InputGroup>
                          </Form.Group>
                          <Form.Group>
                            <Form.Group id="password" className="mb-4">
                              <Form.Label>Your Password</Form.Label>
                              <InputGroup>
                                <InputGroup.Text>
                                  <FontAwesomeIcon icon={faUnlockAlt} />
                                </InputGroup.Text>
                                <Form.Control required type="password" placeholder="Password" onChange={this.handleChangePassword}/>
                              </InputGroup>
                            </Form.Group>
                            <div className="d-flex justify-content-between align-items-center mb-4">
                              <Form.Check type="checkbox" >
                                <FormCheck.Input id="defaultCheck5" className="me-2" onChange={this.handleChangeRemember}/>
                                <FormCheck.Label htmlFor="defaultCheck5" className="mb-0">Remember me</FormCheck.Label>
                              </Form.Check>
                              <Card.Link className="small text-end">Lost password?</Card.Link>
                            </div>
                          </Form.Group>
                          <Button variant="primary" type="button" className="w-100" onClick={this.handleLogin}>
                            Sign in
                          </Button>
                        </Form>
                        
                        <div className="d-flex justify-content-center align-items-center mt-4">
                          <p className="text-left pds-top-15 mgs-right-3 pds-right-12">
                            <Card.Link as={Link} to={Routes.Overview.path} className="text-gray-700">
                              <FontAwesomeIcon icon={faAngleLeft} className="me-2" /> Back to homepage
                            </Card.Link>
                          </p>
                          <span className="fw-normal">
                            Not registered?
                            <Card.Link as={Link} to={Routes.Signup.path} className="fw-bold">
                              {` Create account `}
                            </Card.Link>
                          </span>
                        </div>
                      </div>
                    </Col>
                  </Row>
                </Container>
              </section>
            </main>
        );
    }
}
export default Login;
