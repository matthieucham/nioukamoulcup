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
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "score": "993.217",
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
                "A": 2,
                "M": 5,
                "G": 1,
                "D": 3
            },
            "compo": {
                "A": [
                    {
                        "club": {
                            "name": "Nancy",
                            "id": 3
                        },
                        "score": "93.75",
                        "player": {
                            "name": "I. Dia",
                            "id": 306
                        }
                    },
                    {
                        "club": {
                            "name": "Lille",
                            "id": 15
                        },
                        "score": "77.75",
                        "player": {
                            "name": "Y. Benzia",
                            "id": 204
                        }
                    },
                    {
                        "club": {
                            "name": "Lyon",
                            "id": 7
                        },
                        "score": "35.83",
                        "player": {
                            "name": "R. Ghezzal",
                            "id": 383
                        }
                    }
                ],
                "M": [
                    {
                        "club": {
                            "name": "Bordeaux",
                            "id": 14
                        },
                        "score": "93.27",
                        "player": {
                            "name": "J. Toulalan",
                            "id": 187
                        }
                    },
                    {
                        "club": {
                            "name": "Marseille",
                            "id": 9
                        },
                        "score": "92.55",
                        "player": {
                            "name": "W. Vainqueur",
                            "id": 118
                        }
                    },
                    {
                        "club": {
                            "name": "Monaco",
                            "id": 20
                        },
                        "score": "82.97",
                        "player": {
                            "name": "T. Bakayoko",
                            "id": 272
                        }
                    },
                    {
                        "club": {
                            "name": "Caen",
                            "id": 18
                        },
                        "score": "76.58",
                        "player": {
                            "name": "J. Féret",
                            "id": 245
                        }
                    },
                    {
                        "club": {
                            "name": "Guingamp",
                            "id": 5
                        },
                        "score": "76.20",
                        "player": {
                            "name": "M. Diallo",
                            "id": 63
                        }
                    }
                ],
                "G": [
                    {
                        "club": {
                            "name": "Toulouse",
                            "id": 1
                        },
                        "score": "105.42",
                        "player": {
                            "name": "A. Lafont",
                            "id": 345
                        }
                    }
                ],
                "D": [
                    {
                        "club": {
                            "name": "Toulouse",
                            "id": 1
                        },
                        "score": "112.72",
                        "player": {
                            "name": "C. Jullien",
                            "id": 4
                        }
                    },
                    {
                        "club": {
                            "name": "Toulouse",
                            "id": 1
                        },
                        "score": "93.42",
                        "player": {
                            "name": "i. Diop",
                            "id": 346
                        }
                    },
                    {
                        "club": {
                            "name": "Nancy",
                            "id": 3
                        },
                        "score": "88.60",
                        "player": {
                            "name": "J. Cétout",
                            "id": 34
                        }
                    }
                ]
            }
        },
        {
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "score": "1942.637",
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
                "A": 2,
                "M": 5,
                "G": 1,
                "D": 3
            },
            "compo": {
                "A": [
                    {
                        "club": {
                            "name": "Nancy",
                            "id": 3
                        },
                        "score": "162.58",
                        "player": {
                            "name": "I. Dia",
                            "id": 306
                        }
                    },
                    {
                        "club": {
                            "name": "Lille",
                            "id": 15
                        },
                        "score": "138.42",
                        "player": {
                            "name": "Y. Benzia",
                            "id": 204
                        }
                    },
                    {
                        "club": {
                            "name": "Lyon",
                            "id": 7
                        },
                        "score": "124.91",
                        "player": {
                            "name": "R. Ghezzal",
                            "id": 383
                        }
                    }
                ],
                "M": [
                    {
                        "club": {
                            "name": "Monaco",
                            "id": 20
                        },
                        "score": "181.23",
                        "player": {
                            "name": "T. Bakayoko",
                            "id": 272
                        }
                    },
                    {
                        "club": {
                            "name": "Marseille",
                            "id": 9
                        },
                        "score": "179.48",
                        "player": {
                            "name": "W. Vainqueur",
                            "id": 118
                        }
                    },
                    {
                        "club": {
                            "name": "Caen",
                            "id": 18
                        },
                        "score": "174.68",
                        "player": {
                            "name": "J. Féret",
                            "id": 245
                        }
                    },
                    {
                        "club": {
                            "name": "Bordeaux",
                            "id": 14
                        },
                        "score": "165.00",
                        "player": {
                            "name": "J. Toulalan",
                            "id": 187
                        }
                    },
                    {
                        "club": {
                            "name": "Guingamp",
                            "id": 5
                        },
                        "score": "155.83",
                        "player": {
                            "name": "M. Diallo",
                            "id": 63
                        }
                    }
                ],
                "G": [
                    {
                        "club": {
                            "name": "Toulouse",
                            "id": 1
                        },
                        "score": "205.89",
                        "player": {
                            "name": "A. Lafont",
                            "id": 345
                        }
                    }
                ],
                "D": [
                    {
                        "club": {
                            "name": "Toulouse",
                            "id": 1
                        },
                        "score": "228.95",
                        "player": {
                            "name": "C. Jullien",
                            "id": 4
                        }
                    },
                    {
                        "club": {
                            "name": "Toulouse",
                            "id": 1
                        },
                        "score": "185.75",
                        "player": {
                            "name": "i. Diop",
                            "id": 346
                        }
                    },
                    {
                        "club": {
                            "name": "Nancy",
                            "id": 3
                        },
                        "score": "164.81",
                        "player": {
                            "name": "J. Cétout",
                            "id": 34
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
