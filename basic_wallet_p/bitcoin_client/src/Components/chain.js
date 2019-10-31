import React from 'react';
import '../App.css';
// import { Route, NavLink } from 'react-router-dom'
import axios from 'axios'
import Blockchain from '../images/blockchain.png'

export default class chain extends React.Component {

    state = {
        chain: [],
    };


    componentDidMount() {

        axios
            .get('http://0.0.0.0:5000/chain')
            .then(res => {
                console.log("SUCCESS")
                this.setState({
                    chain: res.data
                });
            })
            .catch(error => console.error(error));

    }

    render() {
        console.log('THIS STATE', this.state.chain)
        return (
            <>
                <div className = 'coinContainer'>
                    {this.state.chain.length > 0 ?
                        <div className='coin'>
                            {this.state.chain.chain.map(x => (
                                <div className={`coininfo ${x.index}`}>
                                    <p>Index: {x.index}</p>
                                    <p>Proof: {x.proof}</p>
                                    <p>Previous Hash: {x.previous_hash}</p>
                                </div>
                            ))}
                        </div> : console.log('NO')
                    }
                </div>
            </>
        )
    }
}