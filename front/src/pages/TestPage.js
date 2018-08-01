import React, { Component } from 'react';
import { connect } from 'react-redux'
import { SaleCard } from '../components/sales/SaleCard'

const mapStateToProps = state => {
	return {
		ranking: state.data.rankings.current,
	}
}

class App extends Component {

	
	render() {
		const SALE = {
            "id": 163,
            "rank": 1,
            "type": "PA",
            "player": {
                "id": 149,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/149/",
                "prenom": "Karl",
                "nom": "Toko Ekambi",
                "surnom": "",
                "display_name": "Karl Toko Ekambi",
                "poste": "A",
                "club": {
                    "id": 11,
                    "nom": "Angers",
                    "maillot_svg": "jersey-stripes-v2",
                    "maillot_color_bg": "#000000",
                    "maillot_color_stroke": "#FFFFFF"
                }
            },
            "author": {
                "id": 15,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/15",
                "name": "The Gipsy Queens"
            },
            "min_price": 0.1,
            "winner": {
                "id": 15,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/15",
                "name": "The Gipsy Queens"
            },
            "amount": 8.0,
            "auctions": [
                {
                    "value": 5.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.1,
                    "is_valid": false,
                    "is_mine": false
                },
                {
                    "value": 8.0,
                    "is_valid": true,
                    "is_mine": false
                }
            ]
        }
          ;

		return (
			<div className="react-app-inner">
			<main>
				<div id="salesList">
				<SaleCard sale={ SALE }/>
				
				</div>
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
	}
}

export const TestPage = connect(mapStateToProps)(App)
