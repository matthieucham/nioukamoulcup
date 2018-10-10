import React, { Component } from "react";
import { connect } from "react-redux";
import { DraftSessionResult } from "../components/sales/DraftSession";

const mapStateToProps = state => {
  return {
    draftsession: state.data.draftsession.initial
  };
};

const Page = ({ draftsession }) => {
  return (
    <div className="react-app-inner">
      <main>
        <article id="home-main">
          <DraftSessionResult draftSession={draftsession} />
        </article>
      </main>
    </div>
  );
};

export const DraftResultsPage = connect(mapStateToProps)(Page);
