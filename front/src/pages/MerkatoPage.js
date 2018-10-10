import React, { Component } from "react";
import { connect } from "react-redux";
import { CurrentMerkatoBid } from "../components/sales/CurrentSales";
import { CurrentMerkatoDraftSession } from "../components/sales/CurrentDraft";

const mapStateToProps = state => {
  return {
    merkatos: state.data.merkatos.initial
  };
};

const Page = ({ merkatos }) => {
  const merkatosComp = merkatos.map((element, index) => {
    if (element.mode == "BID") {
      return <CurrentMerkatoBid merkato={element} key={`merkato_${index}`} />;
    } else {
      const drafts = element.draft_sessions.map(sess => (
        <CurrentMerkatoDraftSession draftSession={sess} />
      ));
      return <div>{drafts}</div>;
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
