import { schema } from "normalizr";

const playerSchema = new schema.Entity("players");
const clubSchema = new schema.Entity("clubs");
const signingSchema = new schema.Entity("signings", { player: playerSchema });

export const Schemas = {
  PLAYER: playerSchema,
  PLAYER_ARRAY: [playerSchema],
  CLUB: clubSchema,
  CLUB_ARRAY: [clubSchema],
  SIGNING: signingSchema,
  SIGNING_ARRAY: [signingSchema]
};
