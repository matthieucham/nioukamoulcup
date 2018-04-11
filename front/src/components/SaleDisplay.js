import React, { Component } from 'react';
import TextLoop from './TextLoop';
import ReactRevealText from 'react-reveal-text'
import { Jersey, Position } from './FieldPlayer'


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
			<div onClick={ this.handleClick }>
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
			panel: 'PRESENTATION'
		}

		this.handleClick = this.handleClick.bind(this)
	}

	handleClick() {
		if (this.state.panel == 'PRESENTATION') {
			this.setState({ panel: 'PLAY' })
		}
	}

	render() {
		return (
			<div className="saleDisplay">
				{ this.state.panel == 'PLAY' && 
					<AnimatedOffersValue offers={ this.props.sale.auctions } winner={ this.props.sale.winner.name } bestOffer={ this.props.sale.amount } difference={ 8.0 } /> }
				{ this.state.panel == 'PRESENTATION' && 
					<SalePresentation sale={this.props.sale} onClick={ this.handleClick }/> }
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


