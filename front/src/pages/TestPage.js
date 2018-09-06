import React, { Component } from "react";
import { connect } from "react-redux";
import PlayerPicker from "../components/sales/PlayerPicker";

const mapStateToProps = state => {
  return {
    ranking: state.data.rankings.current
  };
};

export class TestPage extends Component {
  render() {
    return (
      <div className="react-app-inner">
        <main>
          <article id="home-main">
            <PlayerPicker />
            
          </article>
        </main>
        <aside className="hg__right" />
      </div>
    );
  }
}

/* export const TestPage = connect(mapStateToProps)(App) */
