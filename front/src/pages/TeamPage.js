import React, { Component } from "react";
import { connect } from "react-redux";
import { TeamDetails } from "../components/TeamDetails";
import { TeamPalmares } from "../components/TeamPalmares";
import { TeamCover } from "../containers/TeamDesc";

const mapStateToProps = state => {
  return {
    team: state.data.team.initial,
    palmares: state.data.team.palmares
  };
};

const Page = ({ team, palmares }) => {
  return (
    <div className="react-app-inner">
      <main>
        <TeamDetails team={team} />
      </main>
      <aside className="hg__right">
        <TeamCover team={team} />
        <TeamPalmares palmaresLines={palmares} />
      </aside>
    </div>
  );
};

export const TeamPage = connect(mapStateToProps)(Page);
