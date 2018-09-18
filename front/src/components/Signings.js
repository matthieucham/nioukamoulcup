import "rc-collapse/assets/index.css";
import React, { Component } from "react";
import { format } from "date-fns";
import Collapse, { Panel } from "rc-collapse";
import KeyValueBox from "./KeyValueBox";

const SigningPanel = ({ signing }) => {
  const hasLeft = signing.hasOwnProperty("end") && signing.end;
  const bonus =
    signing.attributes.score_factor && signing.attributes.score_factor > 1.0
      ? ((signing.attributes.score_factor - 1.0) * 100).toFixed(0) + "%"
      : null;
  const amount = signing.attributes.amount + " Ka";
  return (
    <div>
      <KeyValueBox label="Prix d'achat" value={amount} />
      {bonus && <KeyValueBox label="Bonification" value={bonus} />}
      <KeyValueBox
        label="Arrivée"
        value={format(signing.begin, "DD/MM/YYYY")}
      />
      {hasLeft && (
        <KeyValueBox label="Départ" value={format(signing.end, "DD/MM/YYYY")} />
      )}
      <a className="navlink" href={signing.player.url}>
        Fiche du joueur
      </a>
    </div>
  );
};

function getSigningHeader(signing) {
  const club = signing.player.club
    ? signing.player.club.nom
    : "Hors championnat";
  const player = signing.player.surnom.length
    ? signing.player.surnom
    : signing.player.prenom + " " + signing.player.nom;

  return (
    <span>
      <span className="playerName">{player}</span>
      <span className="clubName">{club}</span>
    </span>
  );
}

function getClassName(signing) {
  const bonusClass =
    signing.attributes.score_factor && signing.attributes.score_factor > 1.0
      ? "bonus"
      : "";
  const currentClass =
    signing.hasOwnProperty("end") && signing.end ? "past" : "";

  return `${bonusClass} ${currentClass}`;
}

const PositionSignings = ({ signings, position }) => {
  const panels = signings.filter(s => s.player.poste == position).map(s => (
    <Panel
      key={s.player.id + "_" + s.begin}
      header={getSigningHeader(s)}
      headerClass={getClassName(s)}
      showArrow
    >
      <SigningPanel signing={s} />
    </Panel>
  ));
  return (
    <div className="position-signings">
      <h3>
        {
          { G: "Gardiens", D: "Défenseurs", M: "Milieux", A: "Attaquants" }[
            position
          ]
        }
      </h3>
      <Collapse accordion={true}>{panels}</Collapse>
    </div>
  );
};

export const TeamSignings = ({ signings }) => (
  <section>
    <h1>Effectif</h1>
    <PositionSignings signings={signings} position="G" />
    <PositionSignings signings={signings} position="D" />
    <PositionSignings signings={signings} position="M" />
    <PositionSignings signings={signings} position="A" />
  </section>
);
