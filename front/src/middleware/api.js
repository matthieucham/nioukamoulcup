import { schema } from 'normalizr';

const playerSchema = new schema.Entity('players');
const clubSchema = new schema.Entity('clubs');

export const Schemas = {
	PLAYER: playerSchema,
	PLAYER_ARRAY: [ playerSchema ],
	CLUB: clubSchema,
	CLUB_ARRAY: [ clubSchema ]
}