import React, { Component } from 'react';
import { Tabs, TabLink, TabContent } from 'react-tabs-redux'
import { TeamRankingTable } from './TeamRankingTable'
import { PlayersRankingTable } from './PlayersRankingTable'


const RankingHeader = ( { phase }) => 
	<h1>Après la journée {phase.current_ranking.number} / {phase.journee_last}</h1>


export const ByDivisionRanking = ({ divisions }) => {
	const divs = divisions.map( (dv) =>
		<div key={ 'rankingdiv_'+dv['id'] }>
			<h2 className="division-title">{ dv['name'] }</h2>
			<TeamRankingTable teams={ dv['ranking'] } height={ 650 } />
		</div>	
	)  
	return (
			divs
		);
}

export const PhaseRankingsTab = ( { phases } ) => {
	
	const links = phases.map( (ph) => {
		const roundIndex = ph.current_ranking.number - ph.journee_first + 1
		const roundTotal = ph.journee_last - ph.journee_first + 1

		return <TabLink to={ 'ttab'+ph['id'] } key={ 'tablink_'+ph['id'] }>{ ph['name'] } {roundIndex}/{roundTotal}</TabLink>});
	links.push(<TabLink to={ 'ttab_players' } key={ 'tablink_players'}>Joueurs</TabLink>)

	const rankings = phases.map( (ph) => 
		<TabContent for={ 'ttab'+ph['id'] } key={ 'tabcontent_'+ph['id'] }>
			<ByDivisionRanking divisions={ ph['current_ranking']['ranking_ekyps'] }/>
			<h1>Joueurs</h1>
			<PlayersRankingTable players={ ph['current_ranking']['ranking_players']['ranking'] } />
		</TabContent>);
	return (
		<section>
			<h1 className="page-title">Classements après la journée {phases[0].current_ranking.number}</h1>
			<Tabs>
			{links}
			{rankings}
			</Tabs>
		</section>
		);
}