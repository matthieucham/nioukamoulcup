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
			<AutoSizer>
			{({width, height}) => (
				<Table
				ref="Table"
				height={height}
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
				cellDataGetter={({rowData}) => rowData['previous_rank'] ? rowData['rank']-rowData['previous_rank'] : ' - '}
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

				<Column	label="Notes manquantes"
				dataKey="missing_notes"
				width={60}/>

				<Column	label="Score"
				dataKey="score"
				width={80}/>

				<Column	label=""
				dataKey="previous_score"
				cellDataGetter={({rowData}) => rowData['score']-rowData['previous_score']}
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
		let sortedList = this.state.teams.sort(this._defaultSortBy(sortBy));
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