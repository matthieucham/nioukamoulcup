import React, { Component } from 'react';
import { AutoSizer, Column, Table, SortDirection } from 'react-virtualized';
import Moment from 'moment';

function getNumber(theNumber)
{
    if(theNumber > 0){
        return "+" + theNumber;
    }else{
        return theNumber.toString();
    }
}

export const FinancesTable = ({ history, height }) => {
		Moment.locale('fr');

		return (<AutoSizer disableHeight>
			{({width}) => (
				<Table
				ref="Table"
				height={height}
				width={width}
				headerHeight={30}
				rowHeight={30}
				rowCount={history ? history.length : 0}
				rowGetter={({ index }) => history ? history[index] : null}>

				<Column	label="Date"
				dataKey="date"
				cellDataGetter={({rowData}) => Moment(rowData.date).format('DD/MM/YYYY') } 
				width={120}/>

				<Column	label="Montant"
				dataKey="amount"
				cellDataGetter={({rowData}) => getNumber(rowData.amount) }
				width={80} flexGrow={1}/>
				
				<Column	label="Total"
				dataKey="new_balance"
				cellDataGetter={({rowData}) => getNumber(rowData.new_balance) +' Ka'}
				width={80}/>

				<Column	label="Infos"
				dataKey="info"
				width={200} flexGrow={1}/>
				</Table>
				)}
			</AutoSizer>);
	}


