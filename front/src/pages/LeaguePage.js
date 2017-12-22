import React, { Component } from 'react';

import { TeamRankingTable } from '../components/TeamRankingTable'

export const LeaguePage = () => {

		const TEAMS = [
                            {
                                "team": {
                                    "id": 1,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/1/",
                                    "name": "Ministry of Madness"
                                },
                                "score": 2114.998,
                                "previous_score": 2084.871,
                                "is_complete": true,
                                "rank": 1,
                                "previous_rank": 1,
                                "missing_notes": 14
                            },
                            {
                                "team": {
                                    "id": 2,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/2/",
                                    "name": "Le ZOO NAZI du FLAN FRAPPE"
                                },
                                "score": 2082.132,
                                "previous_score": 2064.289,
                                "is_complete": true,
                                "rank": 2,
                                "previous_rank": 2,
                                "missing_notes": 6
                            },
                            {
                                "team": {
                                    "id": 3,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/3/",
                                    "name": "Béjon14"
                                },
                                "score": 2076.266,
                                "previous_score": 2031.049,
                                "is_complete": true,
                                "rank": 3,
                                "previous_rank": 3,
                                "missing_notes": 2
                            },
                            {
                                "team": {
                                    "id": 4,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/4/",
                                    "name": "Ventre mou"
                                },
                                "score": 2023.949,
                                "previous_score": 1996.361,
                                "is_complete": true,
                                "rank": 4,
                                "previous_rank": 4,
                                "missing_notes": 5
                            },
                            {
                                "team": {
                                    "id": 5,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/5/",
                                    "name": "El Brutal Principe"
                                },
                                "score": 1997.051,
                                "previous_score": 1977.123,
                                "is_complete": true,
                                "rank": 5,
                                "previous_rank": 5,
                                "missing_notes": 4
                            },
                            {
                                "team": {
                                    "id": 7,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/7/",
                                    "name": "Damn ! United"
                                },
                                "score": 1988.194,
                                "previous_score": 1956.393,
                                "is_complete": true,
                                "rank": 6,
                                "previous_rank": 6,
                                "missing_notes": 5
                            },
                            {
                                "team": {
                                    "id": 6,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/6/",
                                    "name": "Pan Bagnat FC"
                                },
                                "score": 1974.277,
                                "previous_score": 1946.554,
                                "is_complete": true,
                                "rank": 7,
                                "previous_rank": 8,
                                "missing_notes": 9
                            },
                            {
                                "team": {
                                    "id": 8,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/8/",
                                    "name": "Lulu Society"
                                },
                                "score": 1969.805,
                                "previous_score": 1951.396,
                                "is_complete": true,
                                "rank": 8,
                                "previous_rank": 7,
                                "missing_notes": 14
                            },
                            {
                                "team": {
                                    "id": 9,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/9/",
                                    "name": "Liv, t'as l'heure ?"
                                },
                                "score": 1942.637,
                                "previous_score": 1909.252,
                                "is_complete": true,
                                "rank": 9,
                                "previous_rank": 10,
                                "missing_notes": 6
                            },
                            {
                                "team": {
                                    "id": 11,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/11/",
                                    "name": "Cramponakelamour"
                                },
                                "score": 1932.754,
                                "previous_score": 1928.236,
                                "is_complete": true,
                                "rank": 10,
                                "previous_rank": 9,
                                "missing_notes": 7
                            },
                            {
                                "team": {
                                    "id": 10,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/10/",
                                    "name": "Chamystador"
                                },
                                "score": 1926.743,
                                "previous_score": 1908.961,
                                "is_complete": true,
                                "rank": 11,
                                "previous_rank": 11,
                                "missing_notes": 19
                            },
                            {
                                "team": {
                                    "id": 13,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/13/",
                                    "name": "The Dashing Otter"
                                },
                                "score": 1925.94,
                                "previous_score": 1908.77,
                                "is_complete": true,
                                "rank": 12,
                                "previous_rank": 12,
                                "missing_notes": 16
                            },
                            {
                                "team": {
                                    "id": 12,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/12/",
                                    "name": "Nation of Breizh"
                                },
                                "score": 1907.082,
                                "previous_score": 1879.406,
                                "is_complete": true,
                                "rank": 13,
                                "previous_rank": 13,
                                "missing_notes": 19
                            },
                            {
                                "team": {
                                    "id": 14,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/14/",
                                    "name": "Willy Wahbi Vinci"
                                },
                                "score": 1876.012,
                                "previous_score": 1849.945,
                                "is_complete": true,
                                "rank": 14,
                                "previous_rank": 14,
                                "missing_notes": 15
                            },
                            {
                                "team": {
                                    "id": 15,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/15/",
                                    "name": "The Gipsy Queens"
                                },
                                "score": 1868.266,
                                "previous_score": 1845.566,
                                "is_complete": true,
                                "rank": 15,
                                "previous_rank": 15,
                                "missing_notes": 19
                            },
                            {
                                "team": {
                                    "id": 16,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/16/",
                                    "name": "Boistou"
                                },
                                "score": 1860.852,
                                "previous_score": 1831.595,
                                "is_complete": true,
                                "rank": 16,
                                "previous_rank": 16,
                                "missing_notes": 30
                            },
                            {
                                "team": {
                                    "id": 17,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/17/",
                                    "name": "Hippoceros & Rhinoppotame"
                                },
                                "score": 1787.327,
                                "previous_score": 1774.561,
                                "is_complete": true,
                                "rank": 17,
                                "previous_rank": 17,
                                "missing_notes": 33
                            },
                            {
                                "team": {
                                    "id": 18,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/18/",
                                    "name": "Party Malin"
                                },
                                "score": 1743.826,
                                "previous_score": 1709.208,
                                "is_complete": true,
                                "rank": 18,
                                "previous_rank": 18,
                                "missing_notes": 21
                            },
                            {
                                "team": {
                                    "id": 19,
                                    "url": "http://127.0.0.1:8000/game/league/ekyp/19/",
                                    "name": "Remontée Grenat"
                                },
                                "score": 1704.239,
                                "previous_score": 1677.31,
                                "is_complete": true,
                                "rank": 19,
                                "previous_rank": 19,
                                "missing_notes": 37
                            }
                        ];
		return (
			<div className="react-app-inner">
			<main>
				<TeamRankingTable teams={ TEAMS } />
			</main>
			<aside className="hg__right">
			
			</aside>
			</div>

			);
}

