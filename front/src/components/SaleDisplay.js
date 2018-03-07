import React, { Component } from 'react';
import TextLoop from './TextLoop';


export class AnimatedOffersValue extends Component {

	constructor(props) {
		super(props);


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
					onLoopCompleted={ () => console.log('Terminé')}>
				</TextLoop> Ka
			</div>
		);
	}
}
