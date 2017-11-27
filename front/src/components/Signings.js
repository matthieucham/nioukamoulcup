import React, { Component } from 'react';
import Moment from 'moment';
import {Card, CardHeader, CardActions, CardText} from 'material-ui/Card';
import Subheader from 'material-ui/Subheader';
import Avatar from 'material-ui/Avatar';
import FlatButton from 'material-ui/FlatButton';

import KeyValueBox from './KeyValueBox'


const SigningPanel = ({ signing }) => {

	const hasLeft = signing.hasOwnProperty('end') && signing.end;
	const bonus = signing.attributes.score_factor && signing.attributes.score_factor > 1.0 ? ((signing.attributes.score_factor - 1.0) * 100).toFixed(0)+'%': null;
	const amount = signing.attributes.amount + ' Ka';
	Moment.locale('fr');
	return (
		<div>
		<KeyValueBox label="Prix d'achat" value={ amount } />
		{ bonus && <KeyValueBox label="Bonification" value={ bonus }/>}
		<KeyValueBox label="Arrivée" value={ Moment(signing.begin).format('DD/MM/YYYY') } />
		{ hasLeft && <KeyValueBox label="Départ" value={ Moment(signing.end).format('DD/MM/YYYY') } />}
		<CardActions>
      		<FlatButton label="Fiche" href={ signing.player.url } />
      		<FlatButton label="Revendre" href={ signing.player.url } primary={true} />
    	</CardActions>
		</div>
		);
}

const PositionSignings = ({signings, position}) => {

	const panels = signings.filter( (s) => s.player.poste==position).map( (s) => {
		const showBonus = s.attributes.score_factor && s.attributes.score_factor > 1.0;
		const textDeco = s.hasOwnProperty('end') && s.end ? 'line-through': 'none';
		return (
			<Card key={s.player.id+'_'+s.begin}>
			
				<CardHeader title={s.player.surnom.length ? s.player.surnom : s.player.prenom+' '+s.player.nom}
							subtitle={s.player.club ? s.player.club.nom : '-'}
							actAsExpander={true} showExpandableButton={true}
							titleStyle={ {textDecoration: textDeco} }>
						<div>
						{showBonus && <Avatar size={24}>B</Avatar>}
						</div>
				</CardHeader>

			<CardText expandable={true} style={ {paddingTop: 0, paddingBottom: 0} } actAsExpander={false} >
			<SigningPanel signing={s} />
			</CardText>
			</Card>)});
	return (
		<div className="position-signings">
			<Subheader>{ {'G': 'Gardiens', 'D': 'Défenseurs', 'M': 'Milieux', 'A': 'Attaquants'}[position] }</Subheader>
			{panels}
		</div>
		);
}

export const TeamSignings = ({signings}) => 
<section>
<h1>Effectif</h1>
<PositionSignings signings={ signings } position="G" />
<PositionSignings signings={ signings } position="D" />
<PositionSignings signings={ signings } position="M" />
<PositionSignings signings={ signings } position="A" />
</section>;