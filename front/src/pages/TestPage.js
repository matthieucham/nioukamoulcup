import React, { Component } from 'react';
import LeagueRankingWidget from '../components/LeagueRanking';
import { CompoTabs } from '../components/Formation';
import { TeamSignings, AggregationPanel } from '../components/Signings';
import { TeamCover, TeamHeader } from '../components/TeamDesc';
import { PlayersTable } from '../components/PlayersTable';

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
	"name": "Party Malin",
	"managers": [
	{
		"user": "Gilliatt"
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
		"total_signings": 13,
		"current_signings": 13
	},
	"signings": [
	{
		"player": {
			"id": 205,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/205/",
			"prenom": "Ederzito",
			"nom": "Macedo Lopes",
			"surnom": "Eder",
			"poste": "A",
			"club": {
				"id": 15,
				"nom": "Lille"
			},
			"perfs_agg": {
				"LEADER": 12,
				"GOAL": 5,
				"PENALSTOP": 0,
				"PENALTY": 1,
				"PASS": 4,
				"OFFENSIVE": 0,
				"NOTES_COUNT": 30,
				"CLEANSHEET": 8,
				"HALFCLEANSHEET": 1,
				"HALFPASS": 1,
				"HALFOFFENSIVE": 3,
				"NOTES_AVG": 4.656,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-03-02T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 142,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/142/",
			"prenom": "Ismaël",
			"nom": "Traoré",
			"surnom": "",
			"poste": "D",
			"club": {
				"id": 11,
				"nom": "Angers"
			},
			"perfs_agg": {
				"LEADER": 5,
				"GOAL": 1,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 1,
				"OFFENSIVE": 2,
				"NOTES_COUNT": 32,
				"CLEANSHEET": 6,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 1,
				"NOTES_AVG": 5.0,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2016-09-20T22:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.05
		}
	},
	{
		"player": {
			"id": 260,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/260/",
			"prenom": "Benjamin",
			"nom": "André",
			"surnom": "",
			"poste": "M",
			"club": {
				"id": 19,
				"nom": "Rennes"
			},
			"perfs_agg": {
				"LEADER": 9,
				"GOAL": 0,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 3,
				"OFFENSIVE": 0,
				"NOTES_COUNT": 36,
				"CLEANSHEET": 12,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 1,
				"NOTES_AVG": 5.366,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2016-09-08T22:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.05
		}
	},
	{
		"player": {
			"id": 3,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/3/",
			"prenom": "Steeve",
			"nom": "Yago",
			"surnom": "",
			"poste": "D",
			"club": {
				"id": 1,
				"nom": "Toulouse"
			},
			"perfs_agg": {
				"LEADER": 8,
				"GOAL": 0,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 0,
				"OFFENSIVE": 2,
				"NOTES_COUNT": 22,
				"CLEANSHEET": 6,
				"HALFCLEANSHEET": 1,
				"HALFPASS": 1,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.731,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2016-09-27T22:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 133,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/133/",
			"prenom": "Enzo",
			"nom": "Crivelli",
			"surnom": "",
			"poste": "A",
			"club": {
				"id": 10,
				"nom": "Bastia"
			},
			"perfs_agg": {
				"LEADER": 9,
				"GOAL": 10,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 1,
				"OFFENSIVE": 1,
				"NOTES_COUNT": 23,
				"CLEANSHEET": 7,
				"HALFCLEANSHEET": 1,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.993,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2016-10-18T22:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 434,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/434/",
			"prenom": "Wylan",
			"nom": "Cyprien",
			"surnom": "",
			"poste": "M",
			"club": {
				"id": 8,
				"nom": "Nice"
			},
			"perfs_agg": {
				"LEADER": 12,
				"GOAL": 8,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 3,
				"OFFENSIVE": 5,
				"NOTES_COUNT": 28,
				"CLEANSHEET": 12,
				"HALFCLEANSHEET": 2,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 1,
				"NOTES_AVG": 5.878,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2016-10-06T22:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 328,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/328/",
			"prenom": "Mapou",
			"nom": "Yangambiwa",
			"surnom": "",
			"poste": "D",
			"club": {
				"id": 7,
				"nom": "Lyon"
			},
			"perfs_agg": {
				"LEADER": 4,
				"GOAL": 0,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 0,
				"OFFENSIVE": 6,
				"NOTES_COUNT": 23,
				"CLEANSHEET": 9,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.801,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-02-07T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 223,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/223/",
			"prenom": "Kevin",
			"nom": "Trapp",
			"surnom": "",
			"poste": "G",
			"club": {
				"id": 17,
				"nom": "Paris SG"
			},
			"perfs_agg": {
				"LEADER": 16,
				"GOAL": 0,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 0,
				"OFFENSIVE": 9,
				"NOTES_COUNT": 24,
				"CLEANSHEET": 15,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 5.66,
				"3STOPS": 5
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-02-09T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 350,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/350/",
			"prenom": "Issiaga",
			"nom": "Sylla",
			"surnom": "",
			"poste": "D",
			"club": {
				"id": 1,
				"nom": "Toulouse"
			},
			"perfs_agg": {
				"LEADER": 3,
				"GOAL": 1,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 1,
				"OFFENSIVE": 3,
				"NOTES_COUNT": 21,
				"CLEANSHEET": 5,
				"HALFCLEANSHEET": 2,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.814,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-03-01T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 10,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/10/",
			"prenom": "Jimmy",
			"nom": "Durmaz",
			"surnom": "",
			"poste": "M",
			"club": {
				"id": 1,
				"nom": "Toulouse"
			},
			"perfs_agg": {
				"LEADER": 5,
				"GOAL": 2,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 1,
				"OFFENSIVE": 2,
				"NOTES_COUNT": 22,
				"CLEANSHEET": 4,
				"HALFCLEANSHEET": 2,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.852,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-03-05T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 362,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/362/",
			"prenom": "Ivan",
			"nom": "Balliu",
			"surnom": "",
			"poste": "D",
			"club": {
				"id": 6,
				"nom": "Metz"
			},
			"perfs_agg": {
				"LEADER": 6,
				"GOAL": 0,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 5,
				"OFFENSIVE": 1,
				"NOTES_COUNT": 26,
				"CLEANSHEET": 6,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.869,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-03-12T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 78,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/78/",
			"prenom": "Opa",
			"nom": "Nguette",
			"surnom": "",
			"poste": "A",
			"club": {
				"id": 6,
				"nom": "Metz"
			},
			"perfs_agg": {
				"LEADER": 5,
				"GOAL": 2,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 2,
				"OFFENSIVE": 1,
				"NOTES_COUNT": 30,
				"CLEANSHEET": 7,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 1,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 4.867,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"begin": "2017-03-13T23:00:00Z",
		"end": null,
		"attributes": {
			"score_factor": 1.0
		}
	},
	{
		"player": {
			"id": 304,
			"url": "http://127.0.0.1:8000/game/home/stat/joueur/304/",
			"prenom": "Alou",
			"nom": "Diarra",
			"surnom": "",
			"poste": "M",
			"club": {
				"id": 3,
				"nom": "Nancy"
			},
			"perfs_agg": {
				"LEADER": 8,
				"GOAL": 2,
				"PENALSTOP": 0,
				"PENALTY": 0,
				"PASS": 0,
				"OFFENSIVE": 0,
				"NOTES_COUNT": 16,
				"CLEANSHEET": 7,
				"HALFCLEANSHEET": 0,
				"HALFPASS": 0,
				"HALFOFFENSIVE": 0,
				"NOTES_AVG": 5.167,
				"3STOPS": 0
			}
		},
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
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
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"score": "773.242",
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
			"D": 5,
			"A": 2,
			"M": 3
		},
		"compo": {
			"G": [
			{
				"player": {
					"name": "K. Trapp",
					"id": 223
				},
				"club": {
					"name": "Paris SG",
					"id": 17
				},
				"score": 115.6
			}
			],
			"D": [
			{
				"player": {
					"name": "I. Balliu",
					"id": 362
				},
				"club": {
					"name": "Metz",
					"id": 6
				},
				"score": 94.2
			},
			{
				"player": {
					"name": "I. Traoré",
					"id": 142
				},
				"club": {
					"name": "Angers",
					"id": 11
				},
				"score": 93.41
			},
			{
				"player": {
					"name": "M. Yangambiwa",
					"id": 328
				},
				"club": {
					"name": "Lyon",
					"id": 7
				},
				"score": 55.93
			},
			{
				"player": {
					"name": "S. Yago",
					"id": 3
				},
				"club": {
					"name": "Toulouse",
					"id": 1
				},
				"score": 37.6
			},
			{
				"player": {
					"name": "I. Sylla",
					"id": 350
				},
				"club": {
					"name": "Toulouse",
					"id": 1
				},
				"score": 25.53
			}
			],
			"A": [
			{
				"player": {
					"name": "Eder",
					"id": 205
				},
				"club": {
					"name": "Lille",
					"id": 15
				},
				"score": 73.92
			},
			{
				"player": {
					"name": "O. Nguette",
					"id": 78
				},
				"club": {
					"name": "Metz",
					"id": 6
				},
				"score": 71.5
			},
			{
				"player": {
					"name": "E. Crivelli",
					"id": 133
				},
				"club": {
					"name": "Bastia",
					"id": 10
				},
				"score": 57.92
			}
			],
			"M": [
			{
				"player": {
					"name": "B. André",
					"id": 260
				},
				"club": {
					"name": "Rennes",
					"id": 19
				},
				"score": 83.89
			},
			{
				"player": {
					"name": "W. Cyprien",
					"id": 434
				},
				"club": {
					"name": "Nice",
					"id": 8
				},
				"score": 72.62
			},
			{
				"player": {
					"name": "J. Durmaz",
					"id": 10
				},
				"club": {
					"name": "Toulouse",
					"id": 1
				},
				"score": 49.03
			},
			{
				"player": {
					"name": "A. Diarra",
					"id": 304
				},
				"club": {
					"name": "Nancy",
					"id": 3
				},
				"score": 48.4
			}
			]
		}
	},
	{
		"team": {
			"id": 18,
			"url": "http://127.0.0.1:8000/game/league/ekyp/18/",
			"name": "Party Malin"
		},
		"score": "1743.826",
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
			"D": 5,
			"A": 2,
			"M": 3
		},
		"compo": {
			"G": [
			{
				"player": {
					"name": "K. Trapp",
					"id": 223
				},
				"club": {
					"name": "Paris SG",
					"id": 17
				},
				"score": 191.33
			}
			],
			"D": [
			{
				"player": {
					"name": "I. Traoré",
					"id": 142
				},
				"club": {
					"name": "Angers",
					"id": 11
				},
				"score": 168.7
			},
			{
				"player": {
					"name": "I. Balliu",
					"id": 362
				},
				"club": {
					"name": "Metz",
					"id": 6
				},
				"score": 158.78
			},
			{
				"player": {
					"name": "M. Yangambiwa",
					"id": 328
				},
				"club": {
					"name": "Lyon",
					"id": 7
				},
				"score": 139.72
			},
			{
				"player": {
					"name": "I. Sylla",
					"id": 350
				},
				"club": {
					"name": "Toulouse",
					"id": 1
				},
				"score": 134.69
			},
			{
				"player": {
					"name": "S. Yago",
					"id": 3
				},
				"club": {
					"name": "Toulouse",
					"id": 1
				},
				"score": 130.94
			}
			],
			"A": [
			{
				"player": {
					"name": "Eder",
					"id": 205
				},
				"club": {
					"name": "Lille",
					"id": 15
				},
				"score": 152.67
			},
			{
				"player": {
					"name": "E. Crivelli",
					"id": 133
				},
				"club": {
					"name": "Bastia",
					"id": 10
				},
				"score": 147.84
			},
			{
				"player": {
					"name": "O. Nguette",
					"id": 78
				},
				"club": {
					"name": "Metz",
					"id": 6
				},
				"score": 143.84
			}
			],
			"M": [
			{
				"player": {
					"name": "W. Cyprien",
					"id": 434
				},
				"club": {
					"name": "Nice",
					"id": 8
				},
				"score": 208.31
			},
			{
				"player": {
					"name": "B. André",
					"id": 260
				},
				"club": {
					"name": "Rennes",
					"id": 19
				},
				"score": 179.3
			},
			{
				"player": {
					"name": "J. Durmaz",
					"id": 10
				},
				"club": {
					"name": "Toulouse",
					"id": 1
				},
				"score": 131.55
			},
			{
				"player": {
					"name": "A. Diarra",
					"id": 304
				},
				"club": {
					"name": "Nancy",
					"id": 3
				},
				"score": 103.47
			}
			]
		}
	}
	]
};

class App extends Component {
	render() {
		return (
			<div className="react-app-inner">
			<main>
			<TeamHeader team={ FULL_PAGE } />
			<CompoTabs clubs={ CURRENT_CLUBS } latestScores={ FULL_PAGE.latest_scores } />
			<PlayersTable players={ FULL_PAGE.signings.map((s) => s.player ) } height={ 500 }/>
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
