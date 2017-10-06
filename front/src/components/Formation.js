import React, { Component } from 'react'
import ReactSVG from 'react-svg'


class Jersey extends Component {

	render() {
		const svgPath = 'svg/'+this.props.club.maillot_svg+'.svg';
		/*const svgStyle = {
			bg: {
				fill: this.props.club.maillot_color_bg
			},
			color1: {
				fill: this.props.club.maillot_color1
			},
			color2: {
				fill: this.props.club.maillot_color2
			},
		}*/
		return (
			<ReactSVG
    			path={ svgPath }
    			/*style={ svgStyle }*/
  			/>
		);
	}
}

export default Jersey