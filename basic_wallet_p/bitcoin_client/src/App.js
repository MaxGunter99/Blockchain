import React from 'react';
import './App.css';
import { Route, NavLink } from 'react-router-dom'
// import axios from 'axios'
import Blockchain from './images/blockchain.png'
import myAccount from './Components/user'
import chain from './Components/chain'

function App() {
  return (
    <div className="App">
      <div className='Header'>
        <div>
          <img src={Blockchain} />
          <h1>Bitcoin Wallet!</h1>
        </div>
        <div>
          <NavLink exact to='/Account'>My Account</NavLink>
          <NavLink exact to='/Chain'>My Chain</NavLink>
        </div>
      </div>
      <Route exact path='/Account' component={myAccount} />
      <Route exact path='/Chain' component={chain} />
    </div>
  )
}
  
export default App;
