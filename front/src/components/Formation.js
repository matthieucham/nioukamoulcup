import React, { Component } from "react";
import { Tabs, TabLink, TabContent } from "react-tabs-redux";

import { JerseyPlaceHolder } from "./FieldPlayer";
import ClubFieldPlayer from "../containers/ClubFieldPlayer";

const PlayersLine = ({ expected, players }) => {
  const fieldPlayers = players.map(pl => (
    <ClubFieldPlayer key={pl.player.id} player={pl} />
  ));
  const placeHolders = [];
  if (fieldPlayers.length < expected) {
    for (var i = 0; i < expected - fieldPlayers.length; i++) {
      placeHolders.push(<JerseyPlaceHolder key={"ph" + i} />);
    }
  }
  return (
    <div className={`compoLine`}>
      {fieldPlayers}
      {placeHolders}
    </div>
  );
};

export const Composition = ({ composition, formation, score }) => {
  const positionOrder = ["G", "D", "M", "A"];
  const lines = positionOrder.map(pos => (
    <PlayersLine
      key={pos}
      players={composition[pos].slice(0, formation[pos])}
      expected={formation[pos]}
    />
  ));
  return (
    <div className="composition">
      {lines}
      <h1>Total: {score}</h1>
    </div>
  );
};

export const CompoTabs = ({ latestScores }) => {
  const links = latestScores.map((lsc, index) => (
    <TabLink to={"ttab_" + index} key={"tablink_" + lsc["day"]["id"]}>
      {lsc["day"]["phase"]}{" "}
    </TabLink>
  ));

  const compositions = latestScores.map((lsc, index) => (
    <TabContent for={"ttab_" + index} key={lsc["day"]["id"]}>
      <Composition
        composition={lsc["composition"]}
        formation={lsc["formation"]}
        score={lsc["score"]}
      />
    </TabContent>
  ));
  return (
    <Tabs>
      {links}
      {compositions}
    </Tabs>
  );
};
