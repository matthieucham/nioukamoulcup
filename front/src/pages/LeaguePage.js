import React, { Component } from 'react';

import { LeagueRankings } from '../containers/LeagueRankings'
import { LeagueTeamInfos } from '../containers/LeagueTeamInfos'

export const LeaguePage = () => {

		return (
			<div className="react-app-inner">
			<main>
				<LeagueRankings />
			</main>
			<aside className="hg__right">
				<LeagueTeamInfos />
			</aside>
			</div>

			);
}

