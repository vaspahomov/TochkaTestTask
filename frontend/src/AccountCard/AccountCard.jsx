import React from 'react';
import PropTypes from 'prop-types';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';

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
        };
    }

    componentDidMount() {
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

    render() {
        return (
            <Grid item xs={12} md={6} style={{margin: "auto", width: "70%"}}>
                <CardActionArea component="a">
                    <Card>
                        <div>
                            <CardContent>
                                <Typography component="h2" variant="h5">
                                    {this.state.name}
                                </Typography>
                                <Typography variant="subtitle1" color="textSecondary">
                                    Уникальный номер абонента: {this.state.id}
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
                            </CardContent>
                        </div>
                    </Card>
                </CardActionArea>
            </Grid>
        );
    }
}

AccountCard.propTypes = {
    post: PropTypes.object,
};