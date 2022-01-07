import React from 'react'
import GameSettings from '../Components/GameSettings'
import Header from '../Components/Header'

export default class Home extends React.Component{
    render(){
        return (
            <>
            <Header/>
	    <GameSettings/>
            </>
	);
    }
}
