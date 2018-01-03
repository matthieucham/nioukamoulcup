import React, { Component } from 'react';
import { AutoSizer, Column, Table, SortDirection } from 'react-virtualized';
import 'react-virtualized/styles.css'; // only needs to be imported once
import Griddle, { plugins, RowDefinition, ColumnDefinition } from 'griddle-react';
import { connect } from 'react-redux';


const rowDataSelector = (state, { griddleKey }) => {
  return state
    .get('data')
    .find(rowMap => rowMap.get('griddleKey') === griddleKey)
    .toJSON();
};

const enhancedWithRowData = connect((state, props) => {
  return {
    // rowData will be available into MyCustomComponent
    rowData: rowDataSelector(state, props)
  };
});

export class PlayersRankingTable extends Component {
	constructor(props) {
		super(props);
		
		this.state={
			players: props.players.sort(this._defaultSortBy('rank')),
			dico: {'G': 'Gardien', 'D': 'Défenseur', 'M': 'Milieu', 'A': 'Attaquant'},
		};

	}

	render() {
		const PlayerHrefComponent = ({ value, griddleKey, rowData }) => <a href={rowData.url}>{value}</a>;
		const PosteComponent = ({ value }) => <span className="poste">{ this.state.dico[value] }</span>
		return (
			<Griddle data={this.state.players} plugins={[plugins.LocalPlugin]}
				components={ {Layout: ({ Table, Pagination, Filter }) => <div><Filter /><Pagination /><Table /></div>} }
				pageProperties={{ pageSize: 20 }}>
				<RowDefinition>
					<ColumnDefinition id="rank" title="Rang" />
					<ColumnDefinition id="display_name" title="Joueur" customComponent={enhancedWithRowData(PlayerHrefComponent) }/>
					<ColumnDefinition id="poste" title="Poste" customComponent={ PosteComponent }/>
					<ColumnDefinition id="score" title="Score" />
				</RowDefinition>
			</Griddle>
		);
	}

	_sort({sortBy}) {
		const players = this._sortList({sortBy});

		this.setState({players});
	}

	_sortList({sortBy}) {
		let sortedList = this.state.players.sort(this._defaultSortBy(sortBy));
		return sortedList;
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




class PlayersRankingTable2 extends Component {

	constructor(props) {
		super(props);


		this.state={
			sortBy: 'rank',
			sortDirection: SortDirection.ASC,
			players: props.players.sort(this._defaultSortBy('rank')),
			dico: {'G': 'Gardien', 'D': 'Défenseur', 'M': 'Milieu', 'A': 'Attaquant'},
		};

		this._sort = this._sort.bind(this);
	}

	render() {
		const {
			players,
			sortBy,
			sortDirection,
			dico,
		} = this.state;

		return (
			<AutoSizer>
			{({width, height}) => (
				<Table
				ref="PlayersTable"
				height={height}
				width={width}
				headerHeight={30}
				rowHeight={30}
				rowCount={players.length}
				rowGetter={({ index }) => players[index]}

				sort={this._sort}
				sortBy={sortBy}
				sortDirection={sortDirection}>
				
				<Column	label="Rang"
				dataKey="rank"
				width={60}/>

				<Column	label="Joueur"
				dataKey="display_name"
				cellRenderer={({rowData}) => <a href={rowData['url']}>{rowData['display_name']}</a> } 
				width={100} flexGrow={1}
				disableSort/>

				<Column	label="Poste"
				dataKey="poste"
				cellDataGetter={({rowData}) => dico[rowData['poste']] }
				width={80}
				disableSort/>

				<Column	label="Score"
				dataKey="score"
				width={80}/>

				</Table>
				)}
			</AutoSizer>
			);
	}

	_sort({sortBy, sortDirection}) {
		const players = this._sortList({sortBy, sortDirection});

		this.setState({sortBy, sortDirection, players});
	}

	_sortList({sortBy, sortDirection}) {
		let sortedList = this.state.players.sort(this._defaultSortBy(sortBy));
		if (sortDirection === SortDirection.DESC)
			return sortedList.reverse();
		return sortedList;
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