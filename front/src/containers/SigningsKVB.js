import { connect } from 'react-redux'
import KeyValueBox from '../components/KeyValueBox'
import { fetchSignings } from '../actions'

const mapDispatchToProps = dispatch => {
  return {
    onKVBClick: () => {
      dispatch(fetchSignings(3)) /* todo pass team */
    }
  }
}

export const SigningsKVB = connect(null, mapDispatchToProps)(KeyValueBox);