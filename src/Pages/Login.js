import React from 'react'
import {Redirect} from 'react-router-dom'
import Header from '../Components/Header'

export default class Login extends React.Component{
    constructor(props){
	super(props);
	this.state={username: '', pwd: '', success: false, msg : '', link:'/'};
	this.chgUsername = this.chgUsername.bind(this);
        this.chgPwd = this.chgPwd.bind(this);
	this.submitForm = this.submitForm.bind(this);
    }
    
    chgUsername(e){
	this.setState({username: e.target.value});
    }

    chgPwd(e){
	this.setState({pwd: e.target.value});
    }
    
    submitForm(){
	fetch('/api/login',
		{method: 'POST',
		headers: {'Content-type': 'application/json'},
 		body: JSON.stringify({
			username: this.state.username, 
			pwd: this.state.pwd
		})})
	    .then(response=>response.json())
	    .then(j=>{this.setState({username: j.username, pwd: j.pwd,
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
	    <div className='login'>
		<h3> Log In </h3>
		<form>
		    <h6 className = 'errormsg'> {this.state.msg} </h6>
                    <label>Username</label><br/>
		    <input type='text' value = {this.state.username} onChange = {this.chgUsername}></input><br/>
                    <label>Password</label><br/>
		    <input type='password' value = {this.state.pwd} onChange = {this.chgPwd}></input>
		</form>
                <button className='submit' onClick = {this.submitForm}>Log In</button>
	    </div>
            </>
	);
    }
}
