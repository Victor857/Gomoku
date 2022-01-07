import React from 'react'
import {Redirect} from 'react-router-dom'
import Header from '../Components/Header'

export default class Login extends React.Component{
    constructor(props){
	super(props);
	this.state={username: '', pwd: '', pwdConfirm: '', 
                    success: false, msg : '', link:'/'};
	this.chgUsername = this.chgUsername.bind(this);
        this.chgPwd = this.chgPwd.bind(this);
        this.chgPwdConfirm = this.chgPwdConfirm.bind(this);
	this.submitForm = this.submitForm.bind(this);
    }
    
    chgUsername(e){
	this.setState({username: e.target.value});
    }

    chgPwd(e){
	this.setState({pwd: e.target.value});
    }

    chgPwdConfirm(e){
        this.setState({pwdConfirm: e.target.value});
    }
    
    submitForm(){
	fetch('/api/signup',
		{method: 'POST',
		headers: {'Content-type': 'application/json'},
 		body: JSON.stringify({
			username: this.state.username, 
			pwd: this.state.pwd,
                        pwdConfirm: this.state.pwdConfirm
		})})
	    .then(response=>response.json())
	    .then(j=>{this.setState({username: j.username, pwd: j.pwd, 
                                   pwdConfirm: j.pwdConfirm,
 	                           success: j.success, msg: j.msg, link:j.link});
                       console.log(j)});
    }

    render(){
	if (this.state.success){
	    return <Redirect to={this.state.link}/>;
	}
	return (
            <>
            <Header/>
	    <div className = 'signup'>
		<h3> Sign Up </h3>
		<form>
		    <h6 className = 'errormsg'> {this.state.msg} </h6>
                    <label>Username</label><br/> 
		    <input type='text' value = {this.state.username} onChange = {this.chgUsername}></input><br/>
                    <label>Password</label><br/>
		    <input type='password' value = {this.state.pwd} onChange = {this.chgPwd}></input><br/>
                    <label>Confrim Password</label><br/>
		    <input type='password' value = {this.state.pwdConfirm}
                           onChange = {this.chgPwdConfirm}/>
		</form>
                <button className='submit' onClick = {this.submitForm}>Register</button>
	    </div>
            </>
	);
    }
}
