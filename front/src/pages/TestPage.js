import React, { Component } from "react";
import { DraftSessionResult } from "../components/sales/DraftSession";
import { SigningCard } from "../components/sales/SigningCard";

const SIGNING = {
  "id": 847,
  "player": {
      "id": 225,
      "url": "http://127.0.0.1:8000/game/home/stat/joueur/225/",
      "prenom": "Marcos",
      "nom": "Correa",
      "surnom": "Marquinhos",
      "display_name": "Marquinhos",
      "poste": "D",
      "club": {
          "id": 17,
          "nom": "Paris SG",
          "maillot_svg": "jersey-stripe-center2",
          "maillot_color_bg": "#004080",
          "maillot_color_stroke": "#f20000"
      }
  },
  "team": {
      "id": 42,
      "url": "http://127.0.0.1:8000/game/league/2/ekyp/42",
      "name": "Chamystador"
  },
  "begin": "2018-10-22T09:01:01.940518+02:00",
  "end": null,
  "attributes": {
      "rank": 17,
      "score_factor": 1.0,
      "locked": true,
      "type": "DRFT",
      "pick_order": 3
  }
}

const DRAFT = {
  number: 1,
  closing: "2018-10-08T19:33:32+02:00",
  is_solved: true,
  attributes: null,
  draftsessionrank_set: [
    {
      rank: 3,
      team: {
        id: 4,
        url: "http://127.0.0.1:8000/game/league/1/ekyp/4",
        name: "MFI"
      },
      signing: {
        id: 4,
        player: {
          id: 94,
          url: "http://127.0.0.1:8000/game/home/stat/joueur/94/",
          prenom: "Paulo Henrique",
          nom: "Chagas de Lima",
          surnom: "Ganso",
          display_name: "Ganso",
          poste: "M",
          club: {
            id: 7,
            nom: "Amiens",
            maillot_svg: "jersey-plain2",
            maillot_color_bg: "#FFFFFF",
            maillot_color_stroke: ""
          }
        },
        team: {
          id: 4,
          url: "http://127.0.0.1:8000/game/league/1/ekyp/4",
          name: "MFI"
        },
        begin: "2018-10-10T13:10:23.278441+02:00",
        end: null,
        attributes: {
          score_factor: 1.0,
          rank: 3,
          pick_order: 1,
          type: "DRFT"
        }
      }
    },
    {
      rank: 4,
      team: {
        id: 4,
        url: "http://127.0.0.1:8000/game/league/1/ekyp/4",
        name: "MFI"
      },
      signing: {
        id: 4,
        player: {
          id: 94,
          url: "http://127.0.0.1:8000/game/home/stat/joueur/94/",
          prenom: "Paulo Henrique",
          nom: "Chagas de Lima",
          surnom: "Ganso",
          display_name: "Kyllian Mizango Pouyt",
          poste: "M",
          club: {
            id: 7,
            nom: "Amiens",
            maillot_svg: "jersey-plain2",
            maillot_color_bg: "#FFFFFF",
            maillot_color_stroke: ""
          }
        },
        team: {
          id: 4,
          url: "http://127.0.0.1:8000/game/league/1/ekyp/4",
          name: "MFI"
        },
        begin: "2018-10-10T13:10:23.278441+02:00",
        end: null,
        attributes: {
          score_factor: 1.0,
          rank: 3,
          pick_order: 1,
          type: "DRFT"
        }
      }
    }
  ]
};

export class TestPage extends Component {
  render() {
    return (
      <div className="react-app-inner">
        <main>
          <article id="home-main">
            <SigningCard signing={SIGNING} />
          </article>
        </main>
        <aside className="hg__right" />
      </div>
    );
  }
}

