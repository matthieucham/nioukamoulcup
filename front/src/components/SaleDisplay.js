import React, { Component } from 'react';
import TextLoop from './TextLoop';
import ReactRevealText from 'react-reveal-text'


export class AnimatedOffersValue extends Component {

	constructor(props) {
		super(props);

		let offers = this._cleanOffers(props.offers)
		let best = props.bestOffer.toFixed(1)+' Ka'
		let difference = 'écart ' + props.difference.toFixed(1)+' Ka'
		this.state = {
			showWinner: false,
			auctions: offers,
			best: best,
			difference: difference,
			winner: this.props.winner
		}
	}

	_cleanOffers(offers) {
		return offers.map(o => o.value).sort(function(a, b){return a - b});
	}

	render() {
		const vals = this.state.auctions;
		return (
			<div>
				{ !this.state.showWinner &&
					<TextLoop 
						springConfig={{ stiffness: 180, damping: 8 }} 
						speed={ 1000 }
						stopLoop={ true }
						children={ vals }
						onLoopCompleted={ () => this.setState({'showWinner': true}) }>
					</TextLoop>
				}
				<ReactRevealText show={ this.state.showWinner }>
					{ this.state.best }
				</ReactRevealText>
				<ReactRevealText show={ this.state.showWinner }>
					{ this.state.winner }
				</ReactRevealText>
				<ReactRevealText show={ this.state.showWinner }>
					{ this.state.difference }
				</ReactRevealText>
				
			</div>
		);
	}
}


export class SaleDisplay extends Component {

	constructor(props) {
		super(props)
	}

	render() {
		return (
			<div className="saleDisplay">
				<AnimatedOffersValue offers={ this.props.sale.auctions } winner={ this.props.sale.winner.name } bestOffer={ this.props.sale.amount } difference={ 8.0 } />
			</div>
			)
	}
}