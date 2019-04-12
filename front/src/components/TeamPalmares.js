import React from "react";

const Trophy = ({ rank, level, type }) => {
  let size = "";
  let picto = "";
  let color = "";
  if (rank == 1 && level == 1) {
    size = "fa-2x";
  }
  if (type == "FULLSEASON") {
    picto = "fa-star";
  }
  if (type == "HALFSEASON") {
    picto = "fa-star-half-o";
  }
  if (rank == 1) {
    color = "Orange";
  }
  if (rank == 2) {
    color = "Gray";
  }
  if (rank == 3) {
    color = "Sienna";
  }
  return <i className={`fa ${picto} ${size}`} style={{ color: color }} />;
};

export const TeamPalmares = ({ palmaresLines }) => {
  const lines = palmaresLines.map(pl => (
    <li>
      <Trophy rank={pl.rank} level={pl.level} type={pl.phase_type} />
      {pl.phase_name}: {pl.rank}
    </li>
  ));
  return (
    <div>
      <h1>Palmarès</h1>
      <ul>{lines}</ul>
    </div>
  );
};
