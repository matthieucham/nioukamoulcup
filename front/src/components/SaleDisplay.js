import React, { Component } from 'react';
import TextLoop from './TextLoop';
import ReactRevealText from 'react-reveal-text'


export class AnimatedOffersValue extends Component {

	constructor(props) {
		super(props);

		this.state = {
			showWinner: false
		}
	}

	render() {
		const vals = this.props.offers.map( o => o.value );
		return (
			<div>
				<TextLoop 
					springConfig={{ stiffness: 180, damping: 8 }} 
					speed={ 1000 }
					stopLoop={ true }
					children={ vals }
					onLoopCompleted={ () => this.setState({'showWinner': true}) }>
				</TextLoop> Ka
				<ReactRevealText show={ this.state.showWinner }>
				The Gipsy Queens
				</ReactRevealText>
			</div>
		);
	}
}
