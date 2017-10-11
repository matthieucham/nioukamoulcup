import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';
import { FieldPlayer } from '../components/Formation';


var CURRENT_CLUBS = [
    {
        "id": 1,
        "nom": "Toulouse",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 2,
        "nom": "Dijon",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 3,
        "nom": "Nancy",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 4,
        "nom": "Saint Etienne",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 5,
        "nom": "Guingamp",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 6,
        "nom": "Metz",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 7,
        "nom": "Lyon",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 8,
        "nom": "Nice",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 9,
        "nom": "Marseille",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 10,
        "nom": "Bastia",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 11,
        "nom": "Angers",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 12,
        "nom": "Montpellier",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 13,
        "nom": "Lorient",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 14,
        "nom": "Bordeaux",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 15,
        "nom": "Lille",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 16,
        "nom": "Nantes",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 17,
        "nom": "Paris SG",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 18,
        "nom": "Caen",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 19,
        "nom": "Rennes",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 20,
        "nom": "Monaco",
        "maillot_svg": "jersey-diag-half-white2",
        "maillot_color_bg": "#FF0000",
        "maillot_color1": "",
        "maillot_color2": ""
    }
];
var CLUB = {"id": 20, "nom": "Monaco", "maillot_svg": "jersey-diag-half-white2", "maillot_color_bg": "#ff0000", "maillot_color1": "#ffffff"};
var PLAYER = {"club": {"id": 20, "name": "Monaco"}, "score": 49.52535000000001, "player": {"id": 275, "name": "T. Lemar"}};

class App extends Component {
  render() {
    return (
      <FieldPlayer club={ CLUB } player={ PLAYER } />

    );
  }
}

export const TestPage = App
