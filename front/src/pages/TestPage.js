import React, { Component } from 'react';
import { connect } from 'react-redux'

import LeagueRankingWidget from '../components/LeagueRanking';
import { SaleDisplay } from '../components/SaleDisplay'

class App extends Component {

	render() {
		const sale = {
            "id": 173,
            "rank": 1,
            "type": "PA",
            "player": {
                "id": 202,
                "url": "http://127.0.0.1:8000/game/home/stat/joueur/202/",
                "prenom": "Marcos Paulo Mesquita",
                "nom": "Lopes",
                "surnom": "Rony Lopes",
                "display_name": "Rony Lopes",
                "poste": "M",
                "club": {
                    "id": 20,
                    "nom": "Monaco"
                }
            },
            "author": {
                "id": 17,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/17",
                "name": "Hippoceros & Rhinoppotame"
            },
            "min_price": 0.1,
            "winner": {
                "id": 7,
                "url": "http://127.0.0.1:8000/game/league/1/ekyp/7",
                "name": "Damn ! United"
            },
            "amount": 30.0,
            "auctions": [
                {
                    "value": 0.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 4.8,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 5.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.5,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.6,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 6.7,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 7.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 7.2,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 8.1,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 21.2,
                    "is_valid": true,
                    "is_mine": true
                },
                {
                    "value": 22.0,
                    "is_valid": true,
                    "is_mine": false
                },
                {
                    "value": 30.0,
                    "is_valid": true,
                    "is_mine": false
                }
            ]
        };
		return (
			<div className="react-app-inner">
			<main>
			<SaleDisplay sale={ sale } />
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
	}
}

export const TestPage = App
