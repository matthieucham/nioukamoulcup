import React, { Component } from 'react'
import ReactSVG from 'react-svg'


export class Jersey extends Component {

	render() {
		const svgPath = '/static/svg/'+this.props.club.maillot_svg+'.svg';
		return (
			<div className="jersey">
			<ReactSVG
			path={ svgPath }
			style={{ width:64, height:64, fill:this.props.club.maillot_color_bg, stroke:this.props.club.maillot_color1 }}
			/>
			</div>
			);
	}
}

export class FieldPlayer extends Component {

	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="fieldPlayer">
			<Jersey club={this.props.club} />
			<h1>{ this.props.player.player.name }</h1>
			<div className="details">
			<h1>{ this.props.player.player.name }</h1>
			<p>{ this.props.player.score }</p>
			<p>{ this.props.club.nom }</p>
			</div>
			</div>
			);
	}


}

/* https://stackoverflow.com/questions/29913387/show-hide-components-in-reactjs */