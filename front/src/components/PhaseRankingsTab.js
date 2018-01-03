import React, { Component } from 'react';
import { Tabs, TabLink, TabContent } from 'react-tabs-redux'
import { TeamRankingTable } from './TeamRankingTable'


export const ByDivisionRanking = ({ divisions }) => {
	const divs = divisions.map( (dv) =>
		<section key={ 'rankingdiv_'+dv['id'] } style={{ height: '100%' }}>
			<h1>{ dv['name'] }</h1>
			<TeamRankingTable teams={ dv['ranking'] } />
		</section>	
	)  
	return (
			divs
		);
}

export const PhaseRankingsTab = ( { phases } ) => {
	const links = phases.map( (ph) => 
		<TabLink to={ 'ttab'+ph['id'] } key={ 'tablink_'+ph['id'] }>{ ph['name'] } </TabLink>);

	const rankings = phases.map( (ph) => 
		<TabContent for={ 'ttab'+ph['id'] } key={ 'tabcontent_'+ph['id'] }>
			<ByDivisionRanking divisions={ ph['current_ranking']['ranking_ekyps'] }/>
		</TabContent>);
	return (
		<Tabs style={{ height: '100%' }}>
		{links}
		{rankings}
		</Tabs>
		);
}