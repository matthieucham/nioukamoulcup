import React, { Component } from 'react';
import Moment from 'moment';

class SigningPanel extends Component{

	constructor(props) {
		super(props);

		this.state={
      		'dico': {'G': 'Gardien', 'D': 'Défenseur', 'M': 'Milieu', 'A': 'Attaquant'}
    	};
	}

	render() {
		Moment.locale('fr');
		return (<dl><dt>Date d'arrivée</dt><dd>{ Moment(this.props.begin).format('DD/MM/YYYY HH:mm') }</dd></dl>);
	}
}