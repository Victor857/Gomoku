import React from 'react';
import {Redirect} from 'react-router-dom'

export default class GameSettings extends React.Component{
    constructor(props){
	super(props);
	this.state = {difficulty: "Beginner", colour: "Black", started: false};
	this.setDifficulty = this.setDifficulty.bind(this);
	this.setColour = this.setColour.bind(this);
        this.startGame = this.startGame.bind(this);
    }
    
    setDifficulty(e){
	this.setState({difficulty: e.target.value});
    }
    
    setColour(e){
	this.setState({colour: e.target.value});
    }
    
    makeButton(t, val, click){
	return (
	    <button className = {"setter " + t + " " + val} 
	    onClick = {click} type = {t} value = {val}>{val}</button>
	)
    }

    startGame(){
        fetch('/api/settings',
		{method:'POST',
		headers:{'Content-type':'application/json'},
	        body: JSON.stringify({colour:this.state.colour, 
			difficulty: this.state.difficulty})})
        .then(()=>setTimeout(this.setState({started:true})));
    }

    render(){
        if (this.state.started){
	    return <Redirect to='/play'/>;
        }
	return(
            <div className="homePage">
            <h1>Gomoku</h1>
	    <div className="settings">
	        <h3> New Game </h3>
		<div className="difficulty">
                    <div>{"Difficulty: " + this.state.difficulty}</div>
	            {this.makeButton("difficulty", "Beginner", this.setDifficulty)}
	            {this.makeButton("difficulty", "Intermediate", this.setDifficulty)}
                    {this.makeButton("difficulty", "Experienced", this.setDifficulty)}
	            {this.makeButton("difficulty", "Advanced", this.setDifficulty)}
                    {this.makeButton("difficulty", "Ultimate", this.setDifficulty)}
                </div>
                <div className="colour">
		    <div>{"Colour: " + this.state.colour}</div>
                    {this.makeButton("colour", "Black", this.setColour)}
                    {this.makeButton("colour", "White", this.setColour)}
                </div>
	        <button id="startGame" onClick = {this.startGame}> Start Game </button>
	    </div>
            <div className='rules'>
                <h3>Rules</h3>
                <p>Gomoku is a board game where players alternate turns placing a 
                   piece of their colour on an empty intersection of the board. Black 
                   plays first. The winner is the first player to form an unbroken 
                   chain of five pieces horizontally, vertically, or diagonally.</p>
            </div>
            </div>
	)  
    }
}

