
export const TEAM_NEXT_RESULT='TEAM_NEXT_RESULT'
export const TEAM_PREVIOUS_RESULT='TEAM_PREVIOUS_RESULT'

export const teamNextResult = dayNumber => {
	return {
		type: TEAM_NEXT_RESULT,
		dayNumber
	}
}

export const teamPreviousResult = dayNumber => {
	return {
		type: TEAM_PREVIOUS_RESULT,
		dayNumber
	}
}