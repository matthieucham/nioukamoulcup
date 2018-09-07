import React, { Component } from "react";
import { connect } from "react-redux";
import {
  SortableContainer,
  SortableElement,
  arrayMove
} from "react-sortable-hoc";
import PlayerPicker from "../components/sales/PlayerPicker";

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
          <SortableList items={[<PlayerPicker key="pp1" />, <PlayerPicker key="pp2" />]} />
          </article>
        </main>
        <aside className="hg__right" />
      </div>
    );
  }
}

/* export const TestPage = connect(mapStateToProps)(App) */
