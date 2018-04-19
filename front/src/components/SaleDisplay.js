import React, { Component } from 'react';
import TextLoop from './TextLoop';
import ReactRevealText from 'react-reveal-text'
import { Jersey, Position } from './FieldPlayer'
/*import { FlexyFlipCard } from 'flexy-flipcards';*/
/*import Flipcard from '@kennethormandy/react-flipcard'*/

// Import minimal required styles however you’d like
/*import '@kennethormandy/react-flipcard/dist/Flipcard.css'*/
import { FlipCard } from 'react-flop-card';


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
			winner: this.props.winner,
		}
	}

	_cleanOffers(offers) {
		return offers.map(o => o.value).sort(function(a, b){return a - b});
	}



	render() {
		const vals = this.state.auctions.map(a => a.toFixed(1) + ' Ka');
		return (
			<div>
				{ !this.state.showWinner &&
					<TextLoop 
						springConfig={{ stiffness: 180, damping: 8 }} 
						speed={ this.props.speed }
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


export class SalePresentation extends Component {
	constructor(props) {
		super(props)

		this.handleClick = this.handleClick.bind(this)
	}

	handleClick(e) {
    	e.preventDefault();
    	if (this.props.onClick) { this.props.onClick(); }
  	}

	render() {
		const isPA = this.props.sale.type == "PA";
		const isMV = this.props.sale.type == "MV";
		return (
			<div className="salePresentation" onClick={ this.handleClick }>
				<p>{ this.props.sale.author.name }</p>
				<div className="playerDesc">
					<Jersey club={ this.props.sale.player.club } height="32" width="32" />
					<div>
					<h1>{this.props.sale.player.display_name}</h1>
					<Position poste={this.props.sale.player.poste}/>
					</div>
				</div>
				<h1>
					{ isPA && <PASaleMarker /> }
					{ isMV && <MVSaleMarker /> }
					{this.props.sale.min_price} Ka
				</h1>
			</div>
			)
	}
}


export class SaleDisplay extends Component {

	constructor(props) {
		super(props)

		this.state = {
			isFlipped: false,
			offersSpeed: 0
		}

		this.showBack = this.showBack.bind(this)
		this.showFront = this.showFront.bind(this)
	}

	showBack() {
		this.setState({
			isFlipped: true,
			offersSpeed: 600
		});
	}

  	showFront() {
  		this.setState({
  			isFlipped: false
  		});
  	}

	render() {
		const front = (<SalePresentation sale={this.props.sale} onClick={ this.showBack }/>);
		const back = (<AnimatedOffersValue 
							offers={ this.props.sale.auctions } 
							winner={ this.props.sale.winner.name } 
							bestOffer={ this.props.sale.amount } 
							difference={ 8.0 }
							speed={ this.state.offersSpeed }
					 	/>);
		return (
			<div>
			<div className="saleDisplay">
				<FlipCard flipped={this.state.isFlipped} frontChild={front} backChild={back} width="240" height="180">
				</FlipCard>
			</div>
			</div>
			)
	}
}


const SaleMarker = ({ text, cl }) => 
	<span className={ `salemarker ${cl}` }>{ text }</span>


const PASaleMarker = () =>
	<SaleMarker text="PA" cl="salemarker-pa"/>

const MVSaleMarker = () =>
	<SaleMarker text="MV" cl="salemarker-mv"/>


