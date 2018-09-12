import React, { Component } from "react";
import { connect } from "react-redux";
import {
  SortableContainer,
  SortableElement,
  arrayMove
} from "react-sortable-hoc";
import PlayerPicker from "../components/sales/PlayerPicker";
import {
  OpenBidMerkatoSession,
  CurrentMerkatoBid
} from "../components/sales/CurrentSales";

/* const mapStateToProps = state => {
  return {
    ranking: state.data.rankings.current
  };
}; */

const SortableItem = SortableElement(({ value }) => <li>{value}</li>);

const SortableList = SortableContainer(({ items }) => {
  return (
    <ul>
      {items.map((value, index) => (
        <SortableItem key={`item-${index}`} index={index} value={value} />
      ))}
    </ul>
  );
});

const MERKATO = {
  begin: "2018-09-03T06:00:00+02:00",
  end: "2018-10-12T18:00:00+02:00",
  mode: "BID",
  configuration: {
    sales_per_session: 10,
    pa_number: 1,
    mv_tax_rate: 0.1,
    roster_size_max: 9,
    session_duration: 48,
    closing_times: ["12:00", "20:00"],
    mv_number: 1,
    re_tax_rate: 0.5,
    init_balance: 100
  },
  league_instance: 6,
  sessions: [
    {
      url: "http://127.0.0.1:8001/game/rest/merkatosessions/220",
      number: 50,
      closing: "2018-09-27T22:00:00+02:00",
      solving: "2018-09-29T22:00:00+02:00",
      is_solved: false,
      attributes: {
        score_factor: 1.0
      },
      sales_count: 1,
      releases_count: 0,
      sales: [
        {
          id: 189,
          rank: 1,
          type: "PA",
          player: {
            id: 341,
            url: "http://127.0.0.1:8001/game/home/stat/joueur/341/",
            prenom: "Vitorino",
            nom: "Hilton",
            surnom: "",
            display_name: "Vitorino Hilton",
            poste: "D",
            club: {
              id: 12,
              nom: "Montpellier",
              maillot_svg: "jersey-shoulders2",
              maillot_color_bg: "#004080",
              maillot_color_stroke: "#ff8000"
            }
          },
          author: {
            id: 7,
            url: "http://127.0.0.1:8001/game/league/1/ekyp/7",
            name: "Damn ! United"
          },
          min_price: 0.1,
          my_auction: null
        }
      ]
    }
  ],
  permissions: {
    next_session: {
      url: "http://127.0.0.1:8001/game/rest/merkatosessions/190",
      number: 20,
      closing: "2018-09-12T22:00:00+02:00",
      solving: "2018-09-14T22:00:00+02:00",
      is_solved: false,
      attributes: {
        score_factor: 1.0
      },
      sales_count: 0,
      releases_count: 0
    },
    auctions: {
      can: false,
      reason: "NOT_ENOUGH_PA"
    },
    pa: {
      can: true,
      reason: "ROSTER_FULL"
    },
    mv: {
      can: true,
      reason: null
    }
  }
};

export class TestPage extends Component {
  render() {
    return (
      <div className="react-app-inner">
        <main>
          <article id="home-main">
            <CurrentMerkatoBid merkato={MERKATO} />
            {/* <SortableList
              items={[<PlayerPicker key="pp1" />, <PlayerPicker key="pp2" />]}
            /> */}
          </article>
        </main>
        <aside className="hg__right" />
      </div>
    );
  }
}

/* export const TestPage = connect(mapStateToProps)(App) */
