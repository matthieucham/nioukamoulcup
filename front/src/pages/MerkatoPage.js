import React, { Component } from "react";
import { connect } from "react-redux";
import { CurrentMerkatoBid } from "../components/sales/CurrentSales";
import { CurrentMerkatoDraftSession } from "../components/sales/CurrentDraft";
import { TransitionSession } from "../components/sales/TransitionSession";

const mapStateToProps = state => {
  return {
    merkatos: state.data.merkatos.initial,
    team: state.data.team.initial
  };
};

const Page = ({ merkatos, team }) => {
  const merkatosComp = merkatos.map((element, index) => {
    if (element.mode == "BID") {
      return <CurrentMerkatoBid merkato={element} key={`merkato_${index}`} />;
    }
    if (element.mode == "DRFT") {
      const drafts = element.draft_sessions.map(sess => (
        <CurrentMerkatoDraftSession draftSession={sess} />
      ));
      return <div>{drafts}</div>;
    }
    if (element.mode == "TRS") {
      const transitions = element.transition_sessions.map(sess => (
        <TransitionSession merkato={element.id} transition={sess} signings={team.signings} />
      ));
      return <div>{transitions}</div>;
    }
  });
  return (
    <div className="react-app-inner">
      <main>
        <article id="home-main">{merkatosComp}</article>
      </main>
    </div>
  );
};

export const MerkatoPage = connect(mapStateToProps)(Page);
