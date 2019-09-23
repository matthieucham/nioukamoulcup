import React from "react";
import { PostReader } from "../components/wall/PostReader";
import { connect } from "react-redux";
import { fetchMorePosts, sendPost } from "../actions";
import { PostWriter } from "../components/wall/PostWriter";
import Cookies from "js-cookie";

class FetchMoreLink extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { nextUrl, onFetchMore } = this.props;
    return (
      <a
        href="#"
        onClick={() => {
          return onFetchMore(nextUrl);
        }}
      >
        Plus...
      </a>
    );
  }
}

class NewMessageForm extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { sendDisabled, onPostMessage } = this.props;
    return <PostWriter sendDisabled={sendDisabled} onSend={onPostMessage} />;
  }
}

class MessagesList extends React.Component {
  render() {
    const { posts, sendDisabled, onPostMessage } = this.props;
    const postsReaders = posts.map(p => (
      <PostReader
        post={p}
        key={p.id}
        sendDisabled={sendDisabled}
        onSend={onPostMessage}
      />
    ));
    return <div className="wall-group-posts">{postsReaders}</div>;
  }
}

export class WallGroup extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      csrftoken: Cookies.get("csrftoken")
    };
  }

  render() {
    const { posts, next, isFetching } = this.props;

    const ConnectedMessagesList = connect(
      state => ({ posts: posts, sendDisabled: isFetching }),
      dispatch => {
        return {
          onPostMessage: (content, replyTo) =>
            dispatch(sendPost(content, replyTo, this.state.csrftoken))
        };
      }
    )(MessagesList);

    const ConnectedFetchMore = connect(
      state => ({ nextUrl: next }),
      dispatch => {
        return {
          onFetchMore: nu => dispatch(fetchMorePosts(nu))
        };
      }
    )(FetchMoreLink);

    const ConnectedNewPostForm = connect(
      state => ({ sendDisabled: isFetching }),
      dispatch => {
        return {
          onPostMessage: (content, replyTo) =>
            dispatch(sendPost(content, replyTo, this.state.csrftoken))
        };
      }
    )(NewMessageForm);

    return (
      <div>
        {<ConnectedNewPostForm />}
        {<ConnectedMessagesList />}
        {next && <ConnectedFetchMore />}
      </div>
    );
  }
}
