import React, {useState, useEffect} from 'react'
import { useHistory } from 'react-router-dom'

export default function  Header(props){
    const [loggedin, setLoggedin] = useState(true);
    const [username, setUsername] = useState('');

    useEffect(()=>{
	fetch('api/header').then(response=>response.json())
            .then(j=>{if (j.loggedin) {setUsername(j.username)}
                      setLoggedin(j.loggedin);});
    })
    
    let history = useHistory();   

    function logout(){
	fetch('api/logout');
        setLoggedin(false);
        history.push("/")
    }

    function user(){
	
    }

    function storelink(){
        var link;
        if (props.redirect){
	    link = props.link;
	}
        else{
            link = '/';
	}
	fetch('/api/storelink', {
            method: 'POST', 
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify({'link': link})
            });
    }

    function login(){
	storelink();
	history.push("/login");
    }

    function signup(){
        storelink();
        history.push('/signup');
    }

    function home(){
        history.push('/');
    }

    function historyPage(){
        history.push('/history');
    }

    return(
	<div className = 'navbar'>
	    <button className='navelem title' key={1} onClick = {home}>Gomoku</button>
	    <button className='navelem' key={2} onClick={home}>Play</button>
	    <button className='navelem' key={3} onClick={historyPage}>History</button>
	    {loggedin ? 
	       [<button className='navelem' key={4} onClick={logout}>Log Out</button>,
	        <button className='navelem' key={5} onClick={user}>{username}</button>]
	      :[<button className='navelem' key={6} onClick={login}>Log In</button>,
	        <button className='navelem' key={7} onClick={signup}>Sign Up</button>]
	     }
	</div>
    )     
}

