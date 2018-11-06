import React, { Component } from "react";
import { format } from "date-fns";
import { connect } from "react-redux";
import { fetchTeamScores } from "../actions";

const JB = ({ team, journee, onPreviousClick, onNextClick }) => {
  if (journee == null) {
    return (
      <div>
        <h1>Pas encore de journée</h1>
      </div>
    );
  }
  const previousClassName =
    journee && journee.is_first ? "navbutton disabled" : "navbutton";
  const nextClassName =
    journee && journee.is_current ? "navbutton disabled" : "navbutton";
  const journeeTitle = journee.is_current
    ? "En cours"
    : `Journée ${journee.numero} du ${format(
        journee.debut,
        "DD/MM/YYYY"
      )} au ${format(journee.fin, "DD/MM/YYYY")}`;
  return (
    <div>
      <h1>
        <a
          href="#"
          className={previousClassName}
          onClick={() => onPreviousClick()}
        >
          <i className="fa fa-chevron-left" />
        </a>
        &nbsp;
        {journeeTitle}
        &nbsp;
        <a href="#" className={nextClassName} onClick={() => onNextClick()}>
          <i className="fa fa-chevron-right" />
        </a>
      </h1>
    </div>
  );
};

const mapDispatchToProps = (dispatch, ownProps) => {
  if (ownProps.journee == null) {
    return {
      onPreviousClick: () => null,
      onNextClick: () => null
    };
  } else {
    const previousnum = ownProps.journee.is_first
      ? ownProps.journee.numero
      : ownProps.journee.is_current
        ? ownProps.journee.numero
        : ownProps.journee.numero - 1;
    const nextnum = ownProps.journee.is_last
      ? 0
      : ownProps.journee.is_current
        ? 0
        : ownProps.journee.numero + 1;

    return {
      onPreviousClick: () =>
        dispatch(fetchTeamScores(ownProps.team.initial.id, previousnum)),
      onNextClick: () =>
        dispatch(fetchTeamScores(ownProps.team.initial.id, nextnum))
    };
  }
};

export const JourneeBrowser = connect(
  null,
  mapDispatchToProps
)(JB);
