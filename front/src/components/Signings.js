import 'rc-collapse/assets/index.css';
import React, { Component } from 'react';
import Moment from 'moment';
import Collapse, { Panel } from 'rc-collapse';

class SigningPanel extends Component{

	constructor(props) {
		super(props);
	}

	render() {
		const signing = this.props.signing
		const hasLeft = signing.hasOwnProperty('end') && signing.end
		const bonus = signing.attributes.score_factor && signing.attributes.score_factor > 1.0 ? ((signing.attributes.score_factor - 1.0) * 100).toFixed(0) : 0
		Moment.locale('fr');
		return (
			<dl>
			<dt>Montant</dt>
			<dd>{ signing.attributes.amount } Ka</dd>
			{ bonus > 0 && <dt>Bonus</dt>}
			{ bonus > 0 && <dd>+{ bonus }%</dd> }
			<dt>Arrivée</dt>
			<dd>{ Moment(signing.begin).format('DD/MM/YYYY HH:mm') }</dd>
			{ hasLeft && <dt>Départ</dt>}
			{ hasLeft && <dd>{ Moment(signing.end).format('DD/MM/YYYY HH:mm') }</dd> }
			<a className="navlink" href={ signing.player.url }>Fiche du joueur</a>
			</dl>
		);
	}
}

class PositionSignings extends Component {
	constructor(props) {
		super(props);

		this.state={
			'dico': {'G': 'Gardiens', 'D': 'Défenseurs', 'M': 'Milieux', 'A': 'Attaquants'}
		};
	}

	getSigningHeader(signing) {
		const club = signing.player.club ? signing.player.club.nom : 'Hors championnat';
		const player = signing.player.surnom.length ? signing.player.surnom : signing.player.prenom+' '+signing.player.nom;
		
		return player+' ('+club+')';
	}

	getClassName(signing) {
		const bonusClass = signing.attributes.score_factor && signing.attributes.score_factor > 1.0 ? 'bonus' : '';
		const currentClass = signing.hasOwnProperty('end') && signing.end ? 'past' : '';

		return `${bonusClass} ${currentClass}`;
	}

	render() {
		const pos = this.props.position;
		const signings = this.props.signings.filter( (s) => s.player.poste==pos).map( (s) => 
			<Panel key={s.player.id+'_'+s.player.begin} header={ this.getSigningHeader(s) } className={ this.getClassName(s) } showArrow={false}>
				<SigningPanel signing={s} />
			</Panel>);
		return (
			<div className="position-signings">
				<h2>{ this.state.dico[this.props.position] }</h2>
				<Collapse accordion={true}>
				{signings}
				</Collapse>
			</div>
		);
	}
}

export class TeamSignings extends Component {
	render() {
		return (
			<section>
				<h1>Effectif</h1>
				<PositionSignings signings={ this.props.signings } position="G" />
    			<PositionSignings signings={ this.props.signings } position="D" />
    			<PositionSignings signings={ this.props.signings } position="M" />
    			<PositionSignings signings={ this.props.signings } position="A" />
			</section>
		);
	}
}