import React, { Component } from 'react';
import { AutoSizer, Column, Table, SortDirection } from 'react-virtualized';
import 'react-virtualized/styles.css'; // only needs to be imported once
import { connect } from 'react-redux';

class PositionFilter extends Component {

	constructor(props) {
		super(props)
	}

	render() {
		return(
			<select onChange={this.props.handleChange} value={this.props.value}>
			<option default value="">{this.props.label}</option>
			<option value="G">Gardiens</option>
			<option value="D">Défenseurs</option>
			<option value="M">Milieux</option>
			<option value="A">Attaquants</option>
			</select>
		);
	}
}


export class PlayersRankingTable extends Component {

	constructor(props) {
		super(props);


		this.state={
			phases: props.phases,
			filterPosition: props.filterPosition,
			sortBy: 'scores.'+props.phases[0]['id'],
			sortDirection: SortDirection.DESC,
			players: props.players.sort(this._sortByScore('scores.'+props.phases[0]['id'])).reverse(),
			dico: {'G': 'Gardien', 'D': 'Défenseur', 'M': 'Milieu', 'A': 'Attaquant'},
		};

		this._sort = this._sort.bind(this);
		this._filter = this._filter.bind(this);
	}

	render() {
		const {
			phases,
			players,
			sortBy,
			sortDirection,
			dico,
		} = this.state;

		var scoresCol = phases.map((ph) => <Column key={ 'col.scores.'+ph['id'] } label={ ph['name'] }
													dataKey={ 'scores.'+ph['id'] }
													cellDataGetter={({dataKey, rowData}) => rowData['scores'][dataKey.substring(7)] }
													width={ 80 } />);
		return (
			<AutoSizer disableHeight>
			{({width}) => (
				<Table
				ref="PlayersTable"
				height={this.props.height}
				width={width}
				headerHeight={30}
				rowHeight={30}
				rowCount={players.length}
				rowGetter={({ index }) => players[index]}

				sort={this._sort}
				sortBy={sortBy}
				sortDirection={sortDirection}>

				<Column label="Rang"
				cellDataGetter={({rowData}) => rowData.index}
				dataKey="index"
				width={60}/>

				<Column	label="Joueur"
				dataKey="display_name"
				cellRenderer={({rowData}) => <a href={rowData['url']}>{rowData['display_name']}</a> } 
				width={100} flexGrow={1}
				disableSort/>

				<Column	label="Poste"
				dataKey="poste"
				cellDataGetter={({rowData}) => dico[rowData['poste']] }
				width={140}
				disableSort
				headerRenderer={ ({ label }) => <PositionFilter label={label} handleChange={ ( event ) => {this.setState({ filterPosition: event.target.value }); this._filter()} }/> }
				/>

				{ scoresCol }

				</Table>
				)}
			</AutoSizer>
			);
	}

	_filter() {
		this.state.players.filter( pl => this.state.filterPosition.length>0 ? pl['poste'] == this.state.filterPosition : true )
	}

	_sort({sortBy, sortDirection}) {
		const players = this._sortList({sortBy, sortDirection});

		this.setState({sortBy, sortDirection, players});
	}

	_sortList({sortBy, sortDirection}) {
		let sortedList = this.state.players.sort(sortBy =='poste' ? this._sortByPoste() : ( sortBy.startsWith('scores.') ? this._sortByScore(sortBy) : this._defaultSortBy(sortBy) ) );
		if (sortDirection === SortDirection.DESC)
			return sortedList.reverse();
		return sortedList;
	}


	_sortByPoste() {
		var ordering = {}, // map for efficient lookup of sortIndex
		sortOrder = ['G','D','M', 'A'];
		for (var i=0; i<sortOrder.length; i++)
			ordering[sortOrder[i]] = i;
		return function(a, b){
			return (ordering[a.poste] - ordering[b.poste]);
		};
	}

	_sortByScore(sortByKey) {
		const phId = sortByKey.substring(7)
		return function(a, b){
			if (a['scores'][phId] < b['scores'][phId])
				return -1 ;
			if (a['scores'][phId] > b['scores'][phId])
				return 1;
			 return 0; //default return value (no sorting)
		};
	}


   	_defaultSortBy(sortByKey) {
   		return function(a, b){
			if (a[sortByKey] < b[sortByKey]) //sort string ascending
				return -1 ;
			if (a[sortByKey] > b[sortByKey])
				return 1;
			 return 0; //default return value (no sorting)
		};
	}
}