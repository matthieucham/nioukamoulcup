import React, { Component } from "react";
import ReactSVG from "react-svg";
import PropTypes from "prop-types";

export const Jersey = ({ club, jerseysize, displayName }) => {
  const svgPath =
    "/static/svg/" + (club ? club.maillot_svg : "jersey-noclub2") + ".svg";
  const colFill = club ? club.maillot_color_bg : "#000";
  const colStroke = club ? club.maillot_color_stroke : "#000";
  return (
    <div className="jersey">
      <ReactSVG
        path={svgPath}
        style={{
          width: jerseysize,
          height: jerseysize,
          fill: colFill,
          stroke: colStroke
        }}
      />
      {displayName && (
        <div className="clubName-container">
          <span className="clubName">{club ? club.nom : "-"}</span>
        </div>
      )}
    </div>
  );
};

Jersey.defaultProps = {
  jerseysize: 64,
  displayName: true
};

export const Position = ({ poste }) => {
  const dico = { G: "Gardien", D: "Défenseur", M: "Milieu", A: "Attaquant" };
  return <p>{dico[poste]}</p>;
};

export const JerseyPlaceHolder = () => {
  const svgPath = "/static/svg/jersey-placeholder2.svg";
  return (
    <div className="jersey">
      <ReactSVG path={svgPath} style={{ width: 64, height: 64 }} />
    </div>
  );
};

const FieldPlayerDetails = ({ player, club }) => {
  const bonus = (player.score_factor - 1.0).toFixed(2) * 100;
  var bonusDisplay = "";
  if (bonus > 0) {
    bonusDisplay = <span className="bonus">{bonus + "%"}</span>;
  }
  return (
    <div className="playerDetails">
      <h1>{player.player.name}</h1>
      <p>
        {player.score}
        {bonusDisplay}
      </p>
    </div>
  );
};

export const FieldPlayer = ({ player, club }) => (
  <div className="fieldPlayer">
    <Jersey club={club} />
    <FieldPlayerDetails player={player} club={club} />
  </div>
);
