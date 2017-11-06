import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';
import { CompoTabs } from '../components/Formation';
import { TeamSignings, AggregationPanel } from '../components/Signings';
import { TeamCover, TeamHeader } from '../components/TeamDesc';

var CURRENT_CLUBS = [
    {
        "id": 0,
        "nom": "Hors L1",
        "maillot_svg": "jersey-noclub2",
    },
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
                        "club": null,
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
                        "club": null,
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

var SIGNINGS = [
        {
            "player": {
                "id": 245,
                "prenom": "Julien",
                "nom": "Féret",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 18,
                    "nom": "Caen"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2016-10-13T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 15.0
            }
        },
        {
            "player": {
                "id": 345,
                "prenom": "Alban",
                "nom": "Lafont",
                "surnom": "",
                "poste": "G",
                "club": {
                    "id": 1,
                    "nom": "Toulouse"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2016-09-06T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.05,
                "amount": 26.1
            }
        },
        {
            "player": {
                "id": 4,
                "prenom": "Christopher",
                "nom": "Jullien",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 1,
                    "nom": "Toulouse"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2016-09-22T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.05,
                "amount": 23.9
            }
        },
        {
            "player": {
                "id": 63,
                "prenom": "Mustapha",
                "nom": "Diallo",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 5,
                    "nom": "Guingamp"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2016-09-29T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 3.3
            }
        },
        {
            "player": {
                "id": 346,
                "prenom": "issa",
                "nom": "Diop",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 1,
                    "nom": "Toulouse"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2016-10-10T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 15.5
            }
        },
        {
            "player": {
                "id": 204,
                "prenom": "Yassine",
                "nom": "Benzia",
                "surnom": "",
                "poste": "A",
                "club": {
                    "id": 15,
                    "nom": "Lille"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-02-12T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 4.1
            }
        },
        {
            "player": {
                "id": 34,
                "prenom": "Julien",
                "nom": "Cétout",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 3,
                    "nom": "Nancy"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-03-06T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 5.9
            }
        },
        {
            "player": {
                "id": 272,
                "prenom": "Tiémoué",
                "nom": "Bakayoko",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 20,
                    "nom": "Monaco"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-02-16T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 36.1
            }
        },
        {
            "player": {
                "id": 187,
                "prenom": "Jérémy",
                "nom": "Toulalan",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 14,
                    "nom": "Bordeaux"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-02-21T23:00:00Z",
            "end": "2017-03-09T11:00:00Z",
            "attributes": {
                "score_factor": 1.0,
                "amount": 18.1
            }
        },
        {
            "player": {
                "id": 118,
                "prenom": "William",
                "nom": "Vainqueur",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 9,
                    "nom": "Marseille"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-02-21T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 24.7
            }
        },
        {
            "player": {
                "id": 383,
                "prenom": "Rachid",
                "nom": "Ghezzal",
                "surnom": "",
                "poste": "A",
                "club": {
                    "id": 7,
                    "nom": "Lyon"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-03-05T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 0.1
            }
        },
        {
            "player": {
                "id": 306,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/259/",
                "prenom": "Issiar",
                "nom": "Dia",
                "surnom": "",
                "poste": "A",
                "club": {
                    "id": 3,
                    "nom": "Nancy"
                }
            },
            "team": {
                "id": 9,
                "name": "Liv, t'as l'heure ?"
            },
            "begin": "2017-03-12T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0,
                "amount": 7.2
            }
        }
    ];
var AGG = {
        "total_pa": 18,
        "total_releases": 2,
        "total_signings": 11,
        "current_signings": 11
    };

var FULL_PAGE = {
    "name": "Le ZOO NAZI du FLAN FRAPPE",
    "managers": [
        {
            "user": "zozo"
        },
        {
            "user": "Fier Panpan"
        },
        {
            "user": "Olaf"
        }
    ],
    "permissions": {
        "write": false,
        "read": true
    },
    "account_balance": null,
    "signings_aggregation": {
        "total_pa": 0,
        "total_releases": 0,
        "total_signings": 12,
        "current_signings": 12
    },
    "signings": [
        {
            "player": {
                "id": 276,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/276/",
                "prenom": "Djibril",
                "nom": "Sidibé",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 20,
                    "nom": "Monaco"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2016-09-15T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.05
            }
        },
        {
            "player": {
                "id": 196,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/196/",
                "prenom": "Sébastien",
                "nom": "Corchia",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 15,
                    "nom": "Lille"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2016-09-18T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.05
            }
        },
        {
            "player": {
                "id": 88,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/88/",
                "prenom": "Maxime",
                "nom": "Gonalons",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 7,
                    "nom": "Lyon"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2016-09-20T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.05
            }
        },
        {
            "player": {
                "id": 232,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/232/",
                "prenom": "Edinson",
                "nom": "Cavani",
                "surnom": "",
                "poste": "A",
                "club": {
                    "id": 17,
                    "nom": "Paris SG"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2016-09-03T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 106,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/106/",
                "prenom": "Younes",
                "nom": "Belhanda",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 8,
                    "nom": "Nice"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2016-10-04T22:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 281,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/281/",
                "prenom": "Benjamin",
                "nom": "Mendy",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 20,
                    "nom": "Monaco"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-02-07T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 163,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/163/",
                "prenom": "Steve",
                "nom": "Mounié",
                "surnom": "",
                "poste": "A",
                "club": {
                    "id": 12,
                    "nom": "Montpellier"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-02-07T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 396,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/396/",
                "prenom": "Fouad",
                "nom": "Chafik",
                "surnom": "",
                "poste": "D",
                "club": {
                    "id": 2,
                    "nom": "Dijon"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-02-27T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 131,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/131/",
                "prenom": "Yannick",
                "nom": "Cahuzac",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 10,
                    "nom": "Bastia"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-02-28T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 216,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/216/",
                "prenom": "Valentin",
                "nom": "Rongier",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 16,
                    "nom": "Nantes"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-02-28T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 353,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/353/",
                "prenom": "Mathieu",
                "nom": "Michel",
                "surnom": "",
                "poste": "G",
                "club": {
                    "id": 11,
                    "nom": "Angers"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-03-01T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        },
        {
            "player": {
                "id": 373,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/373/",
                "prenom": "Ole",
                "nom": "Selnaes",
                "surnom": "",
                "poste": "M",
                "club": {
                    "id": 4,
                    "nom": "Saint Etienne"
                }
            },
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "begin": "2017-03-16T23:00:00Z",
            "end": null,
            "attributes": {
                "score_factor": 1.0
            }
        }
    ],
    "latest_scores": [
        {
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "score": "1013.363",
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
                "M": 4,
                "A": 2,
                "D": 4,
                "G": 1
            },
            "compo": {
                "M": [
                    {
                        "club": {
                            "name": "Nantes",
                            "id": 16
                        },
                        "score": 96.1,
                        "player": {
                            "name": "V. Rongier",
                            "id": 216
                        }
                    },
                    {
                        "club": {
                            "name": "Lyon",
                            "id": 7
                        },
                        "score": 83.95,
                        "player": {
                            "name": "M. Gonalons",
                            "id": 88
                        }
                    },
                    {
                        "club": {
                            "name": "Nice",
                            "id": 8
                        },
                        "score": 78.23,
                        "player": {
                            "name": "Y. Belhanda",
                            "id": 106
                        }
                    },
                    {
                        "club": {
                            "name": "Bastia",
                            "id": 10
                        },
                        "score": 65.45,
                        "player": {
                            "name": "Y. Cahuzac",
                            "id": 131
                        }
                    },
                    {
                        "club": {
                            "name": "Saint Etienne",
                            "id": 4
                        },
                        "score": 60.37,
                        "player": {
                            "name": "O. Selnaes",
                            "id": 373
                        }
                    }
                ],
                "A": [
                    {
                        "club": {
                            "name": "Paris SG",
                            "id": 17
                        },
                        "score": 149.5,
                        "player": {
                            "name": "E. Cavani",
                            "id": 232
                        }
                    },
                    {
                        "club": {
                            "name": "Montpellier",
                            "id": 12
                        },
                        "score": 102.33,
                        "player": {
                            "name": "S. Mounié",
                            "id": 163
                        }
                    }
                ],
                "D": [
                    {
                        "club": {
                            "name": "Monaco",
                            "id": 20
                        },
                        "score": 114.68,
                        "player": {
                            "name": "B. Mendy",
                            "id": 281
                        }
                    },
                    {
                        "club": {
                            "name": "Lille",
                            "id": 15
                        },
                        "score": 102.67,
                        "player": {
                            "name": "S. Corchia",
                            "id": 196
                        }
                    },
                    {
                        "club": {
                            "name": "Monaco",
                            "id": 20
                        },
                        "score": 95.39,
                        "player": {
                            "name": "D. Sidibé",
                            "id": 276
                        }
                    },
                    {
                        "club": {
                            "name": "Dijon",
                            "id": 2
                        },
                        "score": 60.9,
                        "player": {
                            "name": "F. Chafik",
                            "id": 396
                        }
                    }
                ],
                "G": [
                    {
                        "club": {
                            "name": "Angers",
                            "id": 11
                        },
                        "score": 64.15,
                        "player": {
                            "name": "M. Michel",
                            "id": 353
                        }
                    }
                ]
            }
        },
        {
            "team": {
                "id": 2,
                "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                "name": "Le ZOO NAZI du FLAN FRAPPE"
            },
            "score": "2082.132",
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
                "M": 4,
                "A": 2,
                "D": 4,
                "G": 1
            },
            "compo": {
                "M": [
                    {
                        "club": {
                            "name": "Nice",
                            "id": 8
                        },
                        "score": 181.84,
                        "player": {
                            "name": "Y. Belhanda",
                            "id": 106
                        }
                    },
                    {
                        "club": {
                            "name": "Lyon",
                            "id": 7
                        },
                        "score": 181.63,
                        "player": {
                            "name": "M. Gonalons",
                            "id": 88
                        }
                    },
                    {
                        "club": {
                            "name": "Nantes",
                            "id": 16
                        },
                        "score": 160.22,
                        "player": {
                            "name": "V. Rongier",
                            "id": 216
                        }
                    },
                    {
                        "club": {
                            "name": "Bastia",
                            "id": 10
                        },
                        "score": 150.55,
                        "player": {
                            "name": "Y. Cahuzac",
                            "id": 131
                        }
                    },
                    {
                        "club": {
                            "name": "Saint Etienne",
                            "id": 4
                        },
                        "score": 133.4,
                        "player": {
                            "name": "O. Selnaes",
                            "id": 373
                        }
                    }
                ],
                "A": [
                    {
                        "club": {
                            "name": "Paris SG",
                            "id": 17
                        },
                        "score": 284.17,
                        "player": {
                            "name": "E. Cavani",
                            "id": 232
                        }
                    },
                    {
                        "club": {
                            "name": "Montpellier",
                            "id": 12
                        },
                        "score": 202.5,
                        "player": {
                            "name": "S. Mounié",
                            "id": 163
                        }
                    }
                ],
                "D": [
                    {
                        "club": {
                            "name": "Monaco",
                            "id": 20
                        },
                        "score": 217.61,
                        "player": {
                            "name": "D. Sidibé",
                            "id": 276
                        }
                    },
                    {
                        "club": {
                            "name": "Lille",
                            "id": 15
                        },
                        "score": 206.87,
                        "player": {
                            "name": "S. Corchia",
                            "id": 196
                        }
                    },
                    {
                        "club": {
                            "name": "Monaco",
                            "id": 20
                        },
                        "score": 188.62,
                        "player": {
                            "name": "B. Mendy",
                            "id": 281
                        }
                    },
                    {
                        "club": {
                            "name": "Dijon",
                            "id": 2
                        },
                        "score": 160.49,
                        "player": {
                            "name": "F. Chafik",
                            "id": 396
                        }
                    }
                ],
                "G": [
                    {
                        "club": {
                            "name": "Angers",
                            "id": 11
                        },
                        "score": 147.65,
                        "player": {
                            "name": "M. Michel",
                            "id": 353
                        }
                    }
                ]
            }
        }
    ]
}

class App extends Component {
  render() {
    return (
    	<div className="react-app-inner">
    		<main>
    		<TeamHeader team={ FULL_PAGE } />
    		<CompoTabs clubs={ CURRENT_CLUBS } latestScores={ FULL_PAGE.latest_scores } />
    		</main>
    		<aside className="hg__right">
                <TeamCover name="El Brutal Principe " coverUrl={ 'http://2.bp.blogspot.com/_vtZDyEhVbnw/SSoFfKwR-gI/AAAAAAAACHs/4p_3iAYKikY/s400/Francescoli.php' }/>
    			<TeamSignings signings={ FULL_PAGE.signings } />
    		</aside>
    	</div>

    );
  }
}

export const TestPage = App
