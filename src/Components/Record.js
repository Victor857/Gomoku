import React from 'react';

export default class Record extends React.Component {
    
    constructor(props){
        super(props);
	this.state={loggedin: true, fetched : []};
    }

    componentDidMount(){	
	fetch('/api/history')
            .then(response=>response.json())
	    .then(j=>{
	        this.setState({loggedin: j.loggedin, fetched: j.games});
             });
    }

	
    componentWillUnmount() {
        this.setState = (state,callback)=>{
	    return;
        };
    }
	
    showGame(game, i){
        console.log(game)
        var won = (game.side === game.result) ? ("Won") : ("Lost");
	var difficulty = (game.difficulty === 0) ? ("Beginner") :
	                 (game.difficulty === 1) ? ("Intermediate") :
	 	         (game.difficulty === 2) ? ("Experienced") :
			 (game.difficulty === 3) ? ("Advanced") :
			 ("ultimate");
	return (
            <div className = {"record "+ won} key={i}>
		<h3>
		    <button className={"posn player "+ game.side}/> 
		    - {difficulty} difficulty, You {won} 
		</h3>
		{game.plays.length} moves, {game.time} 
            </div>
        );
    }

    render() {
        if (this.state.loggedin){
            return (
                <div className="History">
                   <h1>Your Past Games: </h1>
	           {Array.from(this.state.fetched, (x,i) => this.showGame(x, i))} 
                   {(this.state.fetched.length === 0) ? "No record was found. Start playing now!" : null}
	        </div>
            );
	}
	return (
            <div className="History">
                <p>
                    Sign up or log in so you can store and view past games.
                </p>
            </div>
        )
    }
}

