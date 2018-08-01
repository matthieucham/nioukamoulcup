import React, { Component } from 'react';
import { connect } from 'react-redux'
import { SolvedMerkatoSession } from '../components/sales/MerkatoSession'

const mapStateToProps = state => {
	return {
		ranking: state.data.rankings.current,
	}
}

class App extends Component {

	
	render() {
		const SESSION = {
    "url": "http://127.0.0.1:8000/game/rest/merkatosessions/5",
    "number": 1,
    "closing": "2017-09-01T10:07:32+02:00",
    "solving": "2017-09-07T19:00:00+02:00",
    "is_solved": true,
    "attributes": {
        "score_factor": 1.05
    },
    "sales_count": 6,
    "releases_count": 0,
    "sales": [
        {
            "id": 6,
            "rank": 1,
            "type": "PA",
            "player": {
                "id": 667,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/667/",
                "prenom": "Neymar Júnior",
                "nom": "da Silva Santos",
                "surnom": "Neymar Jr",
                "display_name": "Neymar Jr",
                "poste": "A",
                "club": {
                    "id": 28,
                    "nom": "Brésil",
                    "maillot_svg": "jersey-plain2",
                    "maillot_color_bg": "#FFFFFF",
                    "maillot_color_stroke": ""
                }
            },
            "author": {
                "id": 12,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/12",
                "name": "Nation of Breizh"
            },
            "min_price": 22.2,
            "winner": {
                "id": 26,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/26",
                "name": "Cette année pas de connerie"
            },
            "amount": 95.2,
            "auctions": [
                {
                    "value": 25.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 31.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 33.3,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 34.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 35.3,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 35.9,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 37.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 42.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 42.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 42.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 42.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 43.6,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 45.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 45.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 46.0,
                    "is_valid": true,
                    "is_mine": true
                },
                {
                    "value": 47.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 51.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 69.9,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 95.2,
                    "is_valid": true,
                    "is_mine": false
                }
            ]
        },
        {
            "id": 8,
            "rank": 2,
            "type": "PA",
            "player": {
                "id": 372,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/372/",
                "prenom": "Loïc",
                "nom": "Perrin",
                "surnom": "",
                "display_name": "Loïc Perrin",
                "poste": "D",
                "club": {
                    "id": 4,
                    "nom": "Saint Etienne",
                    "maillot_svg": "jersey-plain2",
                    "maillot_color_bg": "#559E54",
                    "maillot_color_stroke": ""
                }
            },
            "author": {
                "id": 9,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/9",
                "name": "Liv, t'as l'heure ?"
            },
            "min_price": 0.1,
            "winner": {
                "id": 12,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/12",
                "name": "Nation of Breizh"
            },
            "amount": 28.0,
            "auctions": [
                {
                    "value": 4.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 5.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 8.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 10.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 12.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 14.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 14.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 15.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 15.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 16.4,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 17.3,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 17.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 21.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 22.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 28.0,
                    "is_valid": true,
                    "is_mine": true
                }
            ]
        },
        {
            "id": 9,
            "rank": 3,
            "type": "PA",
            "player": {
                "id": 112,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/112/",
                "prenom": "Hiroki",
                "nom": "Sakai",
                "surnom": "",
                "display_name": "Hiroki Sakai",
                "poste": "D",
                "club": {
                    "id": 34,
                    "nom": "Japon",
                    "maillot_svg": "jersey-plain2",
                    "maillot_color_bg": "#FFFFFF",
                    "maillot_color_stroke": ""
                }
            },
            "author": {
                "id": 26,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/26",
                "name": "Cette année pas de connerie"
            },
            "min_price": 0.1,
            "winner": {
                "id": 12,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/12",
                "name": "Nation of Breizh"
            },
            "amount": 11.0,
            "auctions": [
                {
                    "value": 2.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 3.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 3.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 5.4,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 8.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 8.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 10.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 11.0,
                    "is_valid": true,
                    "is_mine": true
                }
            ]
        },
        {
            "id": 10,
            "rank": 4,
            "type": "PA",
            "player": {
                "id": 701,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/701/",
                "prenom": "Youri",
                "nom": "Tielemans",
                "surnom": "",
                "display_name": "Youri Tielemans",
                "poste": "M",
                "club": {
                    "id": 29,
                    "nom": "Belgique",
                    "maillot_svg": "jersey-plain2",
                    "maillot_color_bg": "#FFFFFF",
                    "maillot_color_stroke": ""
                }
            },
            "author": {
                "id": 1,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/1",
                "name": "Ministry of Madness"
            },
            "min_price": 0.1,
            "winner": {
                "id": 1,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/1",
                "name": "Ministry of Madness"
            },
            "amount": 14.7,
            "auctions": [
                {
                    "value": 0.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 0.4,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 1.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 1.1,
                    "is_valid": true,
                    "is_mine": true
                },
                {
                    "value": 1.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 3.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.9,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 8.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 10.9,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 13.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 14.7,
                    "is_valid": true,
                    "is_mine": false
                }
            ]
        },
        {
            "id": 11,
            "rank": 5,
            "type": "PA",
            "player": {
                "id": 561,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/561/",
                "prenom": "Daniel Alves",
                "nom": "da Silva",
                "surnom": "Dani Alves",
                "display_name": "Dani Alves",
                "poste": "D",
                "club": {
                    "id": 17,
                    "nom": "Paris SG",
                    "maillot_svg": "jersey-stripe-center2",
                    "maillot_color_bg": "#004080",
                    "maillot_color_stroke": "#f20000"
                }
            },
            "author": {
                "id": 7,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/7",
                "name": "Damn ! United"
            },
            "min_price": 12.0,
            "winner": {
                "id": 11,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/11",
                "name": "Cramponakelamour"
            },
            "amount": 27.8,
            "auctions": [
                {
                    "value": 12.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 12.4,
                    "is_valid": true,
                    "is_mine": true
                },
                {
                    "value": 12.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 13.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 15.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 16.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 18.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 18.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 19.3,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 21.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 22.4,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 22.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 23.6,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 24.4,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 27.8,
                    "is_valid": true,
                    "is_mine": false
                }
            ]
        },
        {
            "id": 172,
            "rank": 6,
            "type": "PA",
            "player": {
                "id": 677,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/677/",
                "prenom": "Mariano",
                "nom": "Diaz",
                "surnom": "Mariano",
                "display_name": "Mariano",
                "poste": "A",
                "club": {
                    "id": 7,
                    "nom": "Lyon",
                    "maillot_svg": "jersey-stripe-h-bicolor2",
                    "maillot_color_bg": "#ff0000",
                    "maillot_color_stroke": "#0000ff"
                }
            },
            "author": {
                "id": 17,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/17",
                "name": "Hippoceros & Rhinoppotame"
            },
            "min_price": 10.0,
            "winner": {
                "id": 19,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/19",
                "name": "Remontée Grenat"
            },
            "amount": 42.0,
            "auctions": [
                {
                    "value": 10.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 17.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 18.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 19.0,
                    "is_valid": true,
                    "is_mine": true
                },
                {
                    "value": 21.3,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 23.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 24.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 26.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 26.9,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 30.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 42.0,
                    "is_valid": true,
                    "is_mine": false
                }
            ]
        }
    ],
    "releases": []
};

		return (
			<div className="react-app-inner">
			<main>
				<article id="home-main">
					<SolvedMerkatoSession session={SESSION} />
				</article>
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
	}
}

export const TestPage = connect(mapStateToProps)(App)
