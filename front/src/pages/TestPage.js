import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';
import { CompoTabs } from '../components/Formation';


var CURRENT_CLUBS = [
    {
        "id": 1,
        "nom": "Toulouse",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#6E4CA9",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 2,
        "nom": "Dijon",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#B71520",
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
        "maillot_color_bg": "#559E54",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 5,
        "nom": "Guingamp",
        "maillot_svg": "jersey-shoulders2",
        "maillot_color_bg": "#E60A18",
        "maillot_color1": "#000000",
        "maillot_color2": ""
    },
    {
        "id": 6,
        "nom": "Metz",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#940023",
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
        "maillot_svg": "jersey-stripes-v2",
        "maillot_color_bg": "#000000",
        "maillot_color1": "#FF0000",
        "maillot_color2": ""
    },
    {
        "id": 9,
        "nom": "Marseille",
        "maillot_svg": "jersey-shoulders2",
        "maillot_color_bg": "#FFFFFF",
        "maillot_color1": "#70CCF0",
        "maillot_color2": ""
    },
    {
        "id": 10,
        "nom": "Bastia",
        "maillot_svg": "jersey-plain2",
        "maillot_color_bg": "#1258DC",
        "maillot_color1": "",
        "maillot_color2": ""
    },
    {
        "id": 11,
        "nom": "Angers",
        "maillot_svg": "jersey-stripes-v2",
        "maillot_color_bg": "#000000",
        "maillot_color1": "#FFFFFF",
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
        "maillot_svg": "jersey-scap2",
        "maillot_color_bg": "#0B29C1",
        "maillot_color1": "#FFFFFF",
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
var LATEST_SCORES = [
        {
            "team": {
                "id": 3,
                "name": "Béjon14"
            },
            "score": "1027.163",
            "day": {
                "id": 57,
                "number": 38,
                "journee": {
                    "id": 1,
                    "numero": 38,
                    "debut": "2017-05-20T19:00:00Z",
                    "fin": "2017-05-20T19:00:00Z"
                },
                "phase_id": 2,
                "phase": "Clausura 2017"
            },
            "formation": {
                "G": 1,
                "M": 4,
                "A": 2,
                "D": 4
            },
            "compo": {
                "G": [
                    {
                        "player": {
                            "id": 414,
                            "name": "T. Didillon"
                        },
                        "score": 86.0,
                        "club": {
                            "id": 6,
                            "name": "Metz"
                        }
                    }
                ],
                "M": [
                    {
                        "player": {
                            "id": 105,
                            "name": "J. Seri"
                        },
                        "score": 98.18300000000002,
                        "club": {
                            "id": 8,
                            "name": "Nice"
                        }
                    },
                    {
                        "player": {
                            "id": 334,
                            "name": "S. Marveaux"
                        },
                        "score": 91.833,
                        "club": {
                            "id": 13,
                            "name": "Lorient"
                        }
                    },
                    {
                        "player": {
                            "id": 62,
                            "name": "E. Didot"
                        },
                        "score": 85.29799999999999,
                        "club": {
                            "id": 5,
                            "name": "Guingamp"
                        }
                    },
                    {
                        "player": {
                            "id": 201,
                            "name": "I. Amadou"
                        },
                        "score": 84.433,
                        "club": {
                            "id": 15,
                            "name": "Lille"
                        }
                    }
                ],
                "A": [
                    {
                        "player": {
                            "id": 93,
                            "name": "A. Lacazette"
                        },
                        "score": 128.833,
                        "club": {
                            "id": 7,
                            "name": "Lyon"
                        }
                    },
                    {
                        "player": {
                            "id": 247,
                            "name": "R. Rodelin"
                        },
                        "score": 86.25,
                        "club": {
                            "id": 18,
                            "name": "Caen"
                        }
                    }
                ],
                "D": [
                    {
                        "player": {
                            "id": 268,
                            "name": "Jemerson"
                        },
                        "score": 114.8175,
                        "club": {
                            "id": 20,
                            "name": "Monaco"
                        }
                    },
                    {
                        "player": {
                            "id": 112,
                            "name": "H. Sakai"
                        },
                        "score": 94.6,
                        "club": {
                            "id": 9,
                            "name": "Marseille"
                        }
                    },
                    {
                        "player": {
                            "id": 143,
                            "name": "V. Manceau"
                        },
                        "score": 87.58300000000001,
                        "club": {
                            "id": 11,
                            "name": "Angers"
                        }
                    },
                    {
                        "player": {
                            "id": 386,
                            "name": "E. Mammana"
                        },
                        "score": 69.333,
                        "club": {
                            "id": 7,
                            "name": "Lyon"
                        }
                    }
                ]
            }
        },
        {
            "team": {
                "id": 3,
                "name": "Béjon14"
            },
            "score": "2076.266",
            "day": {
                "id": 37,
                "number": 38,
                "journee": {
                    "id": 1,
                    "numero": 38,
                    "debut": "2017-05-20T19:00:00Z",
                    "fin": "2017-05-20T19:00:00Z"
                },
                "phase_id": 1,
                "phase": "Saison 2016-17"
            },
            "formation": {
                "G": 1,
                "M": 4,
                "A": 2,
                "D": 4
            },
            "compo": {
                "G": [
                    {
                        "player": {
                            "id": 414,
                            "name": "T. Didillon"
                        },
                        "score": 181.96800000000007,
                        "club": {
                            "id": 6,
                            "name": "Metz"
                        }
                    }
                ],
                "M": [
                    {
                        "player": {
                            "id": 105,
                            "name": "J. Seri"
                        },
                        "score": 222.93199999999993,
                        "club": {
                            "id": 8,
                            "name": "Nice"
                        }
                    },
                    {
                        "player": {
                            "id": 334,
                            "name": "S. Marveaux"
                        },
                        "score": 163.783,
                        "club": {
                            "id": 13,
                            "name": "Lorient"
                        }
                    },
                    {
                        "player": {
                            "id": 201,
                            "name": "I. Amadou"
                        },
                        "score": 161.552,
                        "club": {
                            "id": 15,
                            "name": "Lille"
                        }
                    },
                    {
                        "player": {
                            "id": 62,
                            "name": "E. Didot"
                        },
                        "score": 152.148,
                        "club": {
                            "id": 5,
                            "name": "Guingamp"
                        }
                    }
                ],
                "A": [
                    {
                        "player": {
                            "id": 93,
                            "name": "A. Lacazette"
                        },
                        "score": 251.584,
                        "club": {
                            "id": 7,
                            "name": "Lyon"
                        }
                    },
                    {
                        "player": {
                            "id": 247,
                            "name": "R. Rodelin"
                        },
                        "score": 183.919,
                        "club": {
                            "id": 18,
                            "name": "Caen"
                        }
                    }
                ],
                "D": [
                    {
                        "player": {
                            "id": 268,
                            "name": "Jemerson"
                        },
                        "score": 226.01250000000002,
                        "club": {
                            "id": 20,
                            "name": "Monaco"
                        }
                    },
                    {
                        "player": {
                            "id": 112,
                            "name": "H. Sakai"
                        },
                        "score": 199.20199999999997,
                        "club": {
                            "id": 9,
                            "name": "Marseille"
                        }
                    },
                    {
                        "player": {
                            "id": 33,
                            "name": "T. Badila"
                        },
                        "score": 168.116,
                        "club": {
                            "id": 3,
                            "name": "Nancy"
                        }
                    },
                    {
                        "player": {
                            "id": 143,
                            "name": "V. Manceau"
                        },
                        "score": 165.05,
                        "club": {
                            "id": 11,
                            "name": "Angers"
                        }
                    }
                ]
            }
        }
    ];


class App extends Component {
  render() {
    return (
    	<CompoTabs clubs={ CURRENT_CLUBS } latestScores={ LATEST_SCORES } />
    );
  }
}

export const TestPage = App
