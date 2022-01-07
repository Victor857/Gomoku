import React from 'react';

class Posn extends React.Component {
  constructor(props){
	  super(props);
	  this.click = this.click.bind(this);
  }

  click(){
	  this.props.click(this.props.index);
  }

  render() {
    return (
      <button className={"posn " + this.props.piece}
	      onClick={this.click} />
    );
  }
}

class Board extends React.Component {
  constructor(props){
	  super(props);
	  this.state={pieces: [], player: 0, computer: -1, won: 1};
	  this.clicker = this.click.bind(this);
	  this.click1 = this.click1.bind(this);
	  this.boardUpdate = this.boardUpdate.bind(this);
	  this.showStatus = this.showStatus.bind(this);
  }
  
  click1(){
	  this.click(1);
  }
  
  fakeClick(i){}

  click(i){
    fetch('/api/click', 
	    {method: 'POST',
	    headers: {'Content-type': 'application/json'},
	    body: JSON.stringify({index:i})}).then(res=>this.boardUpdate(res))
	  .then(res =>
      	    fetch('/api/computer')).then(res=>this.boardUpdate(res));
  }

  boardUpdate(retrieved){
    retrieved.json()
	  .then(res=>{if (res.updated) 
		  {if (res.won !== 1) {console.log(res.won); this.clicker = this.fakeClick;}
	          console.log(res.won);
		  this.setState({pieces: res.pieces, player: res.player, won: res.won});}});
  } 

  componentDidMount(){
  	fetch('/api/board').then(res=>this.boardUpdate(res))
  }

  renderPosn(i) {
    return <Posn key={i} index={i} piece={this.state.pieces[i]} click={this.clicker}/>;
  }
  
  showStatus(){
      if (this.state.won === 1){
          return (<><Posn piece={'player '+this.state.player}/><p>next player </p></>);
      }
      return(<><Posn piece={'player ' + this.state.won}/> <p>   Is the winner this time ! </p></>);
  }

  render() {
    return(
      <>
	<div className = 'status'>
	    {this.showStatus()}
	</div>
        <div id = "game-board">
	  {Array.from(new Array(15), (x, r) => (
	    <div key={r} className="board-row">
	      {Array.from(new Array(15), (x, c) => this.renderPosn(c+r*15))}
	    </div>
	  ))}
        </div>
      </>
    );
  }
  
  
}

export default class Game extends React.Component {		
    render() {
        return (
            <div className="game">
      	        <Board/> 
            </div>
        );
    }
}

