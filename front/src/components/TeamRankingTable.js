import React, { Component } from 'react';
import { AutoSizer, Column, Table, SortDirection } from 'react-virtualized';
import 'react-virtualized/styles.css'; // only needs to be imported once

export class TeamRankingTable extends Component {

	constructor(props) {
		super(props);


		this.state={
			sortBy: 'rank',
			sortDirection: SortDirection.ASC,
			teams: props.teams.sort(this._defaultSortBy('rank')),
		};

		this._sort = this._sort.bind(this);
	}

	render() {
		const {
			teams,
			sortBy,
			sortDirection,
		} = this.state;

		return (
			<AutoSizer disableHeight>
			{({width}) => (
				<Table
				ref="Table"
				height={ this.props.height }
				width={width}
				headerHeight={30}
				rowHeight={30}
				rowCount={teams.length}
				rowGetter={({ index }) => teams[index]}

				sort={this._sort}
				sortBy={sortBy}
				sortDirection={sortDirection}>
				
				<Column	label="Rang"
				dataKey="rank"
				width={60}/>

				<Column	label=""
				dataKey="previous_rank"
				cellRenderer={({rowData}) => { 
						if (rowData['previous_rank']) {
							let prog = rowData['rank']-rowData['previous_rank']
							if (prog == 0)
								return <span className="prog-eq"><i className="fa fa-minus"></i></span>;
							if (prog < 0) {
								return <span className="prog-up"><i className="fa fa-arrow-up"></i> {Math.abs(prog)}</span>;
							}
							if (prog > 0)
								return <span className="prog-down"><i className="fa fa-arrow-down"></i> {prog}</span>;
						} else return '';
					}
				}
				width={40}
				disableSort/>

				<Column	label=""
				dataKey="is_complete"
				cellRenderer={({rowData}) => rowData['is_complete'] ? <i className="fa fa-check-circle-o"></i> : <i className="fa fa-circle-o"></i> } 
				width={20}
				disableSort/>

				<Column	label="Nom"
				dataKey="team.name"
				cellRenderer={({rowData}) => <a href={rowData['team']['url']}>{rowData['team']['name']}</a> } 
				width={100} flexGrow={1}
				disableSort/>

				<Column	label="Notes"
				dataKey="missing_notes"
				cellDataGetter={({rowData}) => rowData['missing_notes'] == 0 ? '' : '-'+rowData['missing_notes']}
				width={80}/>

				<Column	label="Score"
				dataKey="score"
				width={80}/>

				<Column	label="Prog."
				dataKey="previous_score"
				cellDataGetter={({rowData}) => '+'+(rowData['score']-rowData['previous_score']).toFixed(1)}
				width={80}/>

				</Table>
				)}
			</AutoSizer>
			);
	}

	_sort({sortBy, sortDirection}) {
		const teams = this._sortList({sortBy, sortDirection});

		this.setState({sortBy, sortDirection, teams});
	}

	_sortList({sortBy, sortDirection}) {
		let sortedList = this.state.teams.sort(sortBy=='previous_score' ? this._sortByProg() : this._defaultSortBy(sortBy));
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

	_sortByProg() {
   		return function(a, b){
			if (a['score']-a['previous_score'] < b['score']-b['previous_score']) //sort string ascending
				return -1 ;
			if (a['score']-a['previous_score'] > b['score']-b['previous_score'])
				return 1;
			 return 0; //default return value (no sorting)
		};
	}
}