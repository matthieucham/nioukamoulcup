import React, { Component } from "react";
import { TransitionSession } from "../components/sales/TransitionSession";
import { KeepOrFreeSignings } from "../components/sales/SigningCard";

const SIGNINGS = [
  {
    id: 847,
    player: {
      id: 225,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/225/",
      prenom: "Marcos",
      nom: "Correa",
      surnom: "Marquinhos",
      display_name: "Marquinhos",
      poste: "D",
      club: {
        id: 17,
        nom: "Paris SG",
        maillot_svg: "jersey-stripe-center2",
        maillot_color_bg: "#004080",
        maillot_color_stroke: "#f20000"
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-10-22T09:01:01.940518+02:00",
    end: null,
    attributes: {
      pick_order: 3,
      rank: 17,
      locked: true,
      score_factor: 1.0,
      type: "DRFT"
    }
  },
  {
    id: 866,
    player: {
      id: 151,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/151/",
      prenom: "Jonathan",
      nom: "Bamba",
      surnom: "",
      display_name: "Jonathan Bamba",
      poste: "A",
      club: {
        id: 15,
        nom: "Lille",
        maillot_svg: "jersey-shoulders2",
        maillot_color_bg: "#ffffff",
        maillot_color_stroke: "#ff0000"
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-10-24T20:01:02.199716+02:00",
    end: null,
    attributes: {
      amount: 36.2,
      type: "PA",
      release_amount: 18.1,
      locked: false,
      score_factor: 1.0
    }
  },
  {
    id: 890,
    player: {
      id: 56,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/56/",
      prenom: "Karl-Johann",
      nom: "Johnsson",
      surnom: "",
      display_name: "Karl-Johann Johnsson",
      poste: "G",
      club: {
        id: 5,
        nom: "Guingamp",
        maillot_svg: "jersey-shoulders2",
        maillot_color_bg: "#E60A18",
        maillot_color_stroke: "#000000"
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-10-28T20:01:01.918559+01:00",
    end: null,
    attributes: {
      amount: 13.7,
      type: "PA",
      release_amount: 6.9,
      locked: false,
      score_factor: 1.05
    }
  },
  {
    id: 933,
    player: {
      id: 801,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/801/",
      prenom: "Lebo",
      nom: "Mothiba",
      surnom: "",
      display_name: "Lebo Mothiba",
      poste: "A",
      club: {
        id: 23,
        nom: "Strasbourg",
        maillot_svg: "jersey-plain2",
        maillot_color_bg: "#0000a0",
        maillot_color_stroke: "#000000"
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-11-04T12:01:02.485641+01:00",
    end: null,
    attributes: {
      amount: 8.8,
      type: "PA",
      locked: false,
      score_factor: 1.05,
      release_amount: 4.4,
      ending: true
    }
  },
  {
    id: 912,
    player: {
      id: 81,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/81/",
      prenom: "Florent",
      nom: "Mollet",
      surnom: "",
      display_name: "Florent Mollet",
      poste: "M",
      club: {
        id: 12,
        nom: "Montpellier",
        maillot_svg: "jersey-shoulders2",
        maillot_color_bg: "#004080",
        maillot_color_stroke: "#ff8000"
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-10-31T20:01:01.807138+01:00",
    end: null,
    attributes: {
      amount: 23.1,
      type: "PA",
      release_amount: 11.6,
      locked: false,
      score_factor: 1.05
    }
  },
  {
    id: 929,
    player: {
      id: 526,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/526/",
      prenom: "Clément",
      nom: "Grenier",
      surnom: "",
      display_name: "Clément Grenier",
      poste: "M",
      club: {
        id: 19,
        nom: "Rennes",
        maillot_svg: "jersey-plain2",
        maillot_color_bg: "#d90000",
        maillot_color_stroke: "#000000"
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-11-03T20:01:02.753199+01:00",
    end: null,
    attributes: {
      amount: 10.3,
      type: "PA",
      release_amount: 5.2,
      locked: false,
      score_factor: 1.05
    }
  },
  {
    id: 935,
    player: {
      id: 802,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/802/",
      prenom: "Runar Alex",
      nom: "Runarsson",
      surnom: "",
      display_name: "Runar Alex Runarsson",
      poste: "G",
      club: {
        id: 2,
        nom: "Dijon",
        maillot_svg: "jersey-plain2",
        maillot_color_bg: "#B71520",
        maillot_color_stroke: ""
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-11-05T12:01:02.829327+01:00",
    end: null,
    attributes: {
      amount: 0.1,
      type: "PA",
      release_amount: 0.1,
      locked: false,
      score_factor: 1.05
    }
  },
  {
    id: 934,
    player: {
      id: 701,
      url: "http://127.0.0.1:8000/game/home/stat/joueur/701/",
      prenom: "Youri",
      nom: "Tielemans",
      surnom: "",
      display_name: "Youri Tielemans",
      poste: "M",
      club: {
        id: 20,
        nom: "Monaco",
        maillot_svg: "jersey-diag-half-white2",
        maillot_color_bg: "#FF0000",
        maillot_color_stroke: ""
      }
    },
    team: {
      id: 42,
      url: "http://127.0.0.1:8000/game/league/2/ekyp/42",
      name: "Chamystador"
    },
    begin: "2018-11-04T12:01:02.502253+01:00",
    end: null,
    attributes: {
      amount: 4.9,
      type: "PA",
      locked: false,
      score_factor: 1.05,
      release_amount: 2.5,
      ending: true
    }
  }
];

const TRANSITION_SESSION = {
  closing: "2019-03-22T17:03:21+01:00",
  is_solved: false,
  attributes: {
    default_formation: {
      M: 4,
      D: 4,
      A: 2,
      G: 1
    },
    formations: [
      {
        M: 3,
        D: 5,
        A: 2,
        G: 1
      },
      {
        M: 4,
        D: 4,
        A: 2,
        G: 1
      },
      {
        M: 3,
        D: 4,
        A: 3,
        G: 1
      },
      {
        M: 5,
        D: 3,
        A: 2,
        G: 1
      },
      {
        M: 4,
        D: 3,
        A: 3,
        G: 1
      }
    ],
    to_keep: 5
  },
  my_choice: null
};

const MERKATO = 10;

export class TestPage extends Component {
  render() {
    return (
      <div className="react-app-inner">
        <main>
          <article id="home-main">
            <TransitionSession
              merkato={MERKATO}
              signings={SIGNINGS}
              transition={TRANSITION_SESSION}
            />
          </article>
        </main>
        <aside className="hg__right" />
      </div>
    );
  }
}
