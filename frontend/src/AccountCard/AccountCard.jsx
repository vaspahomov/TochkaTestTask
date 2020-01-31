import React from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from "@material-ui/core/Button";
import Slider from "@material-ui/core/Slider";

export default class AccountCard extends React.Component {
    constructor(props) {
        super(props);
        const {id} = props;
        this.state = {
            name: '',
            id: id,
            balance: '',
            hold: '',
            status: '',
            decreaseBalance: 100,
            increaseBalance: 100,
        };

        this.decreaseHandler = () => {
            fetch('/api/substract',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        accountNumber: this.state.id,
                        substraction: this.state.decreaseBalance
                    }),
                }).then(() => this.updateListing())
        };

        this.increaseHandler = () => {
            fetch('/api/add',
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        accountNumber: this.state.id,
                        addition: this.state.increaseBalance
                    }),
                }).then(() => this.updateListing())
        };

        this.decreaseSliderHandler = (object, newValue) => {
            this.setState({decreaseBalance: newValue});
        };

        this.increaseSliderHandler = (object, newValue) => {
            this.setState({increaseBalance: newValue});
        };

        this.updateListing = () => {
            fetch(`/api/status?accountNumber=${this.state.id}`)
                .then(resp => resp.json())
                .then(json => {
                    this.setState({
                        name: json.addition.ownerName,
                        id: json.addition.id,
                        balance: json.addition.balance,
                        hold: json.addition.hold,
                        status: json.addition.status ? 'Открыт' : 'Закрыт',
                    })
                });
        }
    }

    componentDidMount() {
        this.updateListing()
    }

    render() {
        return (
            <Grid item xs={12} md={6} style={{margin: "auto", width: "70%"}}>
                <Card>
                    <div>
                        <CardContent>
                            <Typography component="h2" variant="h5">
                                {this.state.name}
                            </Typography>
                            <Typography variant="subtitle1" color="textSecondary">
                                Уникальный номер абонента: <code>{this.state.id}</code>
                            </Typography>
                            <Typography variant="subtitle1" color="textSecondary">
                                Баланс: {this.state.balance}
                            </Typography>
                            <Typography variant="subtitle1" color="textSecondary">
                                Холд: {this.state.hold}
                            </Typography>
                            <Typography variant="subtitle1" color="textSecondary">
                                Статус: {this.state.status}
                            </Typography>
                            <div>
                                <Typography id="discrete-slider" gutterBottom>
                                    Снять со счета:
                                </Typography>
                                <Slider
                                    getAriaValueText={(v) => `${v}$`}
                                    aria-labelledby="discrete-slider"
                                    valueLabelDisplay="auto"
                                    step={10}
                                    marks
                                    min={0}
                                    max={500}
                                    defaultValue="100"
                                    onChangeCommitted={this.decreaseSliderHandler}
                                />
                                <Button variant="contained" color="secondary"
                                        onClick={this.decreaseHandler}>Подтвердить</Button>
                            </div>
                            <div>
                                <Typography id="discrete-slider" gutterBottom>
                                    Пополнить счет:
                                </Typography>
                                <Slider
                                    getAriaValueText={(v) => `${v}$`}
                                    aria-labelledby="discrete-slider"
                                    valueLabelDisplay="auto"
                                    step={10}
                                    marks
                                    min={0}
                                    max={500}
                                    defaultValue="100"
                                    onChangeCommitted={this.increaseSliderHandler}
                                />
                                <Button variant="contained" color="secondary"
                                        onClick={this.increaseHandler}>Подтвердить</Button>
                            </div>
                        </CardContent>
                    </div>
                </Card>
            </Grid>
        );
    }
}

AccountCard.propTypes = {
    post: PropTypes.object,
};