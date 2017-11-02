import React, { Component } from 'react';
import ReactSVG from 'react-svg';
import 'rc-tabs/assets/index.css';
import Tabs, { TabPane } from 'rc-tabs';
import TabContent from 'rc-tabs/lib/TabContent';
import InkTabBar from 'rc-tabs/lib/InkTabBar';
import Griddle, { plugins, RowDefinition, ColumnDefinition } from 'griddle-react';


class Jersey extends Component {

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


class JerseyPlaceHolder extends Component {

	render() {
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
}

class FieldPlayerDetails extends Component {
	render() {
		return (
			<div className="details">
			<h1>{ this.props.player.player.name }</h1>
			<p>{ this.props.player.score }</p>
			<p>{ this.props.club.nom }</p>
			</div>
		);
	}
}

class FieldPlayer extends Component {

	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="fieldPlayer">
			<Jersey club={this.props.club} />
			<div className="playerDetails">
			<h1>{ this.props.player.player.name }</h1>
			<p>{ this.props.player.score }</p>
			<p>{ this.props.club.nom }</p>
			</div>
			</div>
		);
	}

}

class PlayersLine extends Component {
	constructor(props) {
		super(props);
	}

	getClub(club) {
		var found = null;
		if (club) {
			found = this.props.clubsMap.get(+club.id);
		} 
		if (found) {
			return found;
		} else {
			return this.props.clubsMap.get(0); /* special Key for "no club" */
		}
	}

	render () {
		const fieldPlayers = this.props.players.map( (pl) => <FieldPlayer key={pl.player.id} player={pl} club={ this.getClub(pl.club) } />);
		const placeHolders = [];
		if (fieldPlayers.length < this.props.expected) {
			for(var i=0; i<(this.props.expected-fieldPlayers.length); i++) {
				placeHolders.push(<JerseyPlaceHolder key={'ph'+i} />)
			}
		}
		return (
			<div className={`compoLine`}>{fieldPlayers}{placeHolders}</div>
			);
	}
}

class Composition extends Component {
	constructor(props) {
		super(props);
		this.state = {clubsMap: new Map( props.clubs.map((cl) => [cl.id, cl]) )};
	}

	render() {
		const positionOrder = ['G', 'D', 'M', 'A'];
		const lines = positionOrder.map( (pos) => <PlayersLine key={pos} clubsMap={this.state.clubsMap} players={this.props.phaseResult['compo'][pos].slice(0, this.props.phaseResult['formation'][pos])} expected={ this.props.phaseResult['formation'][pos] }/>);
		return (<div className="composition">
				{ lines }
				<h1>Total: { this.props.phaseResult['score'] }</h1>
				</div>)
	}
}

class CompositionTable extends Component {

	constructor(props) {
		super(props);
		const compo = this.props.phaseResult['compo'];
		const positionOrder = ['G', 'D', 'M', 'A'];
		positionOrder.map( (pos) => compo[pos].map((pl) => pl.position=pos));
		
		const arrs = [compo['G'], compo['D'], compo['M'], compo['A']];
		this.state = {
      		data: [].concat(...arrs)
    	};
	}

	render() {
		const playerHrefComponent = ({value}) => <a href={`/game/home/stat/joueur/${value.get('id')}`}>{value.get('name')}</a>;
		const clubHrefComponent = ({value}) => <a href={`/game/home/stat/club/${value.get('id')}`}>{value.get('name')}</a>;
		return (
			<Griddle data={this.state.data} plugins={[plugins.LocalPlugin]}
				components={{Layout: ({ Table }) => <Table />}} pageProperties={{ pageSize: 14 }}>
				<RowDefinition>
					<ColumnDefinition id="player" title="Joueur" customComponent={ playerHrefComponent }/>
					<ColumnDefinition id="position" title="Poste" />
					<ColumnDefinition id="club" title="Club" customComponent={ clubHrefComponent }/>
					<ColumnDefinition id="score" title="Score" />
				</RowDefinition>
			</Griddle>
		);
	}
}

export class CompoTabs extends Component {
	render() {
		if (this.props.latestScores.length == 1) {
			return (<Composition clubs={this.props.clubs} phaseResult={ this.props.latestScores[0] } />);
		} else {
			const compositions = this.props.latestScores.map( (lsc) => 
				<TabPane tab={ lsc['day']['phase'] } key={ lsc['day']['id'] }>
					<Composition clubs={this.props.clubs} phaseResult={ lsc }/>
					<CompositionTable phaseResult={ lsc }/>
				</TabPane>);
			return (
				<Tabs
					renderTabBar={() => <InkTabBar/>}
          			renderTabContent={() => <TabContent/>}>
				{compositions}
				</Tabs>
			);
		}
	}
}