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
var PLAYER = {"club": {"id": 20, "name": "Monaco"}, "score": 49.53, "player": {"id": 275, "name": "T. Lemar"}};
var COMPOSITION = {
                "M": [
                    {
                        "player": {
                            "id": 186,
                            "name": "V. Vada"
                        },
                        "score": 105.6,
                        "club": {
                            "id": 14,
                            "name": "Bordeaux"
                        }
                    },
                    {
                        "player": {
                            "id": 233,
                            "name": "A. Di Maria"
                        },
                        "score": 98.566,
                        "club": {
                            "id": 17,
                            "name": "Paris SG"
                        }
                    },
                    {
                        "player": {
                            "id": 250,
                            "name": "V. Bessat"
                        },
                        "score": 86.59899999999999,
                        "club": {
                            "id": 18,
                            "name": "Caen"
                        }
                    },
                    {
                        "player": {
                            "id": 368,
                            "name": "P. Capelle"
                        },
                        "score": 62.831999999999994,
                        "club": {
                            "id": 11,
                            "name": "Angers"
                        }
                    }
                ],
                "D": [
                    {
                        "player": {
                            "id": 141,
                            "name": "R. Thomas"
                        },
                        "score": 92.384,
                        "club": {
                            "id": 11,
                            "name": "Angers"
                        }
                    },
                    {
                        "player": {
                            "id": 113,
                            "name": "R. Fanni"
                        },
                        "score": 90.2,
                        "club": {
                            "id": 9,
                            "name": "Marseille"
                        }
                    },
                    {
                        "player": {
                            "id": 87,
                            "name": "J. Morel"
                        },
                        "score": 83.852,
                        "club": {
                            "id": 7,
                            "name": "Lyon"
                        }
                    },
                    {
                        "player": {
                            "id": 169,
                            "name": "M. Peybernes"
                        },
                        "score": 79.96600000000001,
                        "club": {
                            "id": 13,
                            "name": "Lorient"
                        }
                    }
                ],
                "G": [
                    {
                        "player": {
                            "id": 124,
                            "name": "J. Leca"
                        },
                        "score": 97.96395000000003,
                        "club": {
                            "id": 10,
                            "name": "Bastia"
                        }
                    }
                ],
                "A": [
                    {
                        "player": {
                            "id": 120,
                            "name": "B. Gomis"
                        },
                        "score": 115.41075000000002,
                        "club": {
                            "id": 9,
                            "name": "Marseille"
                        }
                    },
                    {
                        "player": {
                            "id": 357,
                            "name": "M. Balotelli"
                        },
                        "score": 92.05035,
                        "club": {
                            "id": 8,
                            "name": "Nice"
                        }
                    }
                ]
            };
var FORMATION = {"M": 4,"D": 4,"G": 1,"A": 2}

class App extends Component {
  render() {
    return (
      <FieldPlayer club={ CLUB } player={ PLAYER } />

    );
  }
}

export const TestPage = App
