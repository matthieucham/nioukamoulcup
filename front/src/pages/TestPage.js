import React, { Component } from "react";
import { connect } from "react-redux";
import {
  SortableContainer,
  SortableElement,
  arrayMove
} from "react-sortable-hoc";
import PlayerPicker from "../components/sales/PlayerPicker";
import { OpenMerkatoSession } from "../components/sales/CurrentSales";

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

export class TestPage extends Component {
  render() {
    return (
      <div className="react-app-inner">
        <main>
          <article id="home-main">
            <OpenMerkatoSession
              session={{
                url: "http://127.0.0.1:8001/game/rest/merkatosessions/220",
                number: 50,
                closing: "2018-09-27T22:00:00+02:00",
                solving: "2018-09-29T22:00:00+02:00",
                is_solved: false,
                attributes: {
                  score_factor: 1.04
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
                    min_price: 0.1
                  }
                ]
              }}
            />
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
