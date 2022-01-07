import React from 'react';
import GamePage from './Pages/GamePage';
import History from './Pages/History';
import Home from './Pages/Home';
import Login from './Pages/Login'
import SignUp from './Pages/SignUp'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
} from 'react-router-dom';


function App(){
  return (
    <Router>
      <Switch>
	<Route exact path='/'>
	  <Home/>
	</Route>
	<Route path='/play'>
	  <GamePage/>
	</Route>
	<Route path='/history'>
	  <History/>
	</Route>
	<Route path='/login'>
	  <Login/>
        </Route>
        <Route path='/signup'>
          <SignUp/>
        </Route>
	<Redirect from='*' to='/' />
      </Switch>
    </Router>
  );
}

export default App;
