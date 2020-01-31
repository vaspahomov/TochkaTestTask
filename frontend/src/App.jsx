import React from 'react';
import './App.css';
import AccountCard from "./AccountCard/AccountCard";

class App extends React.Component {
    constructor() {
        super();
        this.state = {
            ids: []
        }
    }

    componentDidMount() {
        fetch('/api/accounts')
            .then(resp => resp.json())
            .then(json => {
                this.setState({
                    ids: json.addition.map(x => x.id)
                })
            });
    }

    render() {
        return (
            <div className="App" >
                {
                    this.state.ids ? this.state.ids.map(x => <div style={{margin: '10px 0'}}><AccountCard id={x}/></div>) : undefined
                }
            </div>
        );
    }
}

export default App;
