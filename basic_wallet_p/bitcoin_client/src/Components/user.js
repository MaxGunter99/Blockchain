
import React from "react";
import axios from 'axios';
import { Link } from 'react-router-dom';

export default class user extends React.Component {
    state = {
        user: '',
        settings: false,
        newUser: ''
    }

    componentDidMount() {
        axios
            .get(`http://0.0.0.0:5000/userid` )
            .then(res => {
                console.log( res.data )
                this.setState({
                    user: res.data,
                    newUser: res.data
                });

            })
            .catch(error => console.error(error));
    }

    changeHandler = event => {
        event.preventDefault();
        this.setState({
            user: {
                ...this.state.user.message,
                [event.target.name]: event.target.value
            }
        });
    };

    toggleSettings = () => {
        if ( this.state.settings === false ) {
            this.setState({ settings: true })
        } else {
            this.setState({ settings: false })
        }
    }

    updateUser = event => {
        event.preventDefault()
        console.log( this.state.user )
        axios
            .post(`http://0.0.0.0:5000/useridupdate` , this.state.user  )
            .then(res => {
                console.log( 'success' )
                this.toggleSettings()
            })
            .catch(error => console.error(error));
    }

    render() {
        return (
            <> 
                <div className = 'CurrentUser'>
                    <div className = 'userInfo'>
                        <p><strong>Username: </strong>{this.state.user.message}</p>
                    </div>
                    { this.state.settings === true ? (

                        <form onSubmit = { this.updateUser } >
                            <label>Change User ID</label>
                            <input
                                id = 'username'
                                type = 'text'
                                name = 'message'
                                value = { this.state.user.message }
                                placeholder = 'Username'
                                onChange = { this.changeHandler }
                            />
        
                            <button type = 'submit' className = 'submitButton'> Done </button>
    
                        </form>
                    ) : null }
                    <div className = 'settingsButtonContainer'>
                        <button onClick = {this.toggleSettings}>Change Username</button>
                    </div>
                </div>
            </>
        );
    }
}