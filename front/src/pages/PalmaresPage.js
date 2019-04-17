import React, { Component } from "react";

import { PhaseRankingsTab } from "../components/PhaseRankingsTab";
import { SigningsTable } from "../components/SigningsTable";
import { connect } from "react-redux";

const idle = () => {};

const mapStateToProps = state => {
  return {
    phases: state.data.palmares.initial.final_ranking,
    playersRanking: state.data.palmares.initial.players_ranking,
    onPlayersTab: idle,
    hyperlinks: false,
    title: `${state.data.palmares.initial.league_instance_name} : ${state.data.palmares.initial.league_instance_slogan}`
  };
};

const PhaseRankings = connect(mapStateToProps)(PhaseRankingsTab);

const mapStateToProps2 = state => {
  return {
    signings: state.data.palmares.initial.signings_history,
    height: 600,
    showTeam: true,
    hyperlinks: false,
  };
};

const Signings = connect(mapStateToProps2)(SigningsTable);

export const PalmaresPage = () => {
  return (
    <div className="react-app-inner">
      <main>
        <PhaseRankings />
		<h1 className="page-title">Historique des transferts</h1>
        <Signings />
      </main>
    </div>
  );
};
