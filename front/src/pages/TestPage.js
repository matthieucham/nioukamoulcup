import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';
import Jersey from '../components/Formation';


var PLAYER = {"club": {"id": 20, "name": "Monaco"}, "score": 49.52535000000001, "player": {"id": 275, "name": "T. Lemar"}};
var CLUB = {"id": 20, "nom": "Monaco", "maillot_svg": "jersey-diag-half", "maillot_color_bg": "#ffffff", "maillot_color1": "#ff0000", "maillot_color2": "#000000"};

class App extends Component {
  render() {
    return (
      <Jersey club={ CLUB }/>
    );
  }
}

export const TestPage = App
