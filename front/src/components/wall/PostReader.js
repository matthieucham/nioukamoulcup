import React from "react";
import { format } from "date-fns";
import { PostWriter } from "./PostWriter";

class TextMessageFormatter extends React.Component {
  render() {
    let CAPTION_LENGTH_LIMIT = 30;
    let ANNOUNCE_LENGTH_LIMIT = 120;
    const { message, in_reply_to } = this.props;
    let classname = "wall-message-std";
    if (in_reply_to == null && message) {
      if (message.length < CAPTION_LENGTH_LIMIT) {
        classname = "wall-message-caption";
      } else if (message.length < ANNOUNCE_LENGTH_LIMIT) {
        classname = "wall-message-announce";
      }
    }
    return <div className={classname}>{message}</div>;
  }
}

class PictureMessageDisplayer extends React.Component {
  render() {
    const { pictureUrl } = this.props;
    return (
      <div className="wall-picture-container">
        {pictureUrl && <img src={pictureUrl} className="wall-picture-box" />}
      </div>
    );
  }
}

class HotlinkedTitle extends React.Component {
  render() {
    const { url, title } = this.props;
    if (title) {
      return (
        <a href={url} target="_blank">
          <TextMessageFormatter message={title} in_reply_to={null} />
        </a>
      );
    } else {
      const shortenedLink = url.length > 80 ? url.substring(80) + "..." : url;
      return (
        <a href={url} target="_blank">
          {shortenedLink}
        </a>
      );
    }
  }
}

class ResponseReader extends React.Component {
  render() {
    const { post } = this.props;
    const pdate = format(post.created_at, "DD/MM/YYYY HH:mm");
    return (
      <div className="wall-response">
        <div className="wall-response-header">
          <div className="wall-response-author">{post.author}</div>
          {/*<div className="wall-response-date">{pdate}</div>*/}
        </div>
        <div className="wall-response-content">
          <TextMessageFormatter
            message={post.message}
            in_reply_to={post.in_reply_to}
          />
        </div>
      </div>
    );
  }
}

export class PostReader extends React.Component {
  render() {
    const { post, sendDisabled, onSend } = this.props;
    const pdate = format(post.created_at, "DD/MM/YYYY HH:mm");
    const replies = post.replies.map((reply, index) => (
      <ResponseReader key={post.id + "_" + index} post={reply} />
    ));
    return (
      <div className="wall-post">
        <div className="wall-post-header">
          <div className="wall-post-author">{post.author}</div>
          <div className="wall-post-date">{pdate}</div>
        </div>
        <div className="wall-post-content">
          <div className="wall-post-message">
            <TextMessageFormatter
              message={post.message}
              in_reply_to={post.in_reply_to}
            />
          </div>
          <div className="wall-post-hotlinked">
            {post.hotlinked_picture && (
              <PictureMessageDisplayer pictureUrl={post.hotlinked_picture} />
            )}
            {post.hotlinked_title && (
              <HotlinkedTitle
                url={post.hotlinked_url}
                title={post.hotlinked_title}
              />
            )}
          </div>
        </div>
        <div className="wall-post-responses">
          {replies}
          <PostWriter
            replyTo={post.id}
            sendDisabled={sendDisabled}
            onSend={onSend}
          />
        </div>
      </div>
    );
  }
}
