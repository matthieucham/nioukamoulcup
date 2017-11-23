import React, { Component } from 'react';
import ReactSVG from 'react-svg';

const Jersey = ({ club }) => {

	const svgPath = '/static/svg/'+(club ? club.maillot_svg : 'jersey-noclub2')+'.svg';
	const colFill = club ? club.maillot_color_bg : '#000';
	const colStroke = club ? club.maillot_color1 : '#000';
	return (
		<div className="jersey">
		<ReactSVG
		path={ svgPath }
		style={{ width:64, height:64, fill:colFill, stroke:colStroke }}
		/>
		</div>
		);
}


export const JerseyPlaceHolder = () => {

	const svgPath = '/static/svg/jersey-placeholder2.svg';
	return (
		<div className="jersey">
		<ReactSVG
		path={ svgPath }
		style={{ width:64, height:64 }}
		/>
		</div>
		);
}

const FieldPlayerDetails = ({player, club}) => <div className="playerDetails"><h1>{ player.player.name }</h1><p>{ player.score }</p><p>{ club ? club.nom : '-' }</p></div>;


export const FieldPlayer = ({ player, club }) => <div className="fieldPlayer"><Jersey club={club} /><FieldPlayerDetails player={ player } club={ club } /></div>;