import React from 'react';
import Game from '../Components/GameParts';
import Header from '../Components/Header'
import {Redirect} from 'react-router-dom';

export default class GamePage extends React.Component { 
  constructor(props){
	  super(props);
	  this.state={check:'True'};
  }
  componentDidMount(){
    fetch('/api/checksettings').then(res=>res.json())
	    .then(res=>{console.log(res); this.setState({check:res.res})});
  }

  render(){
    console.log(this.state.check);
    if (this.state.check === 'True'){
      return (
        <>
        <Header/>
        <Game/>
        </>
      );
    }
    return (<Redirect to='/'/>);
  }
}

