import React from "react";
import TextareaAutosize from "react-autosize-textarea";
import Button from "@material-ui/core/Button";

export class PostWriter extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      value:
        props.editedPost == null
          ? ""
          : props.editedPost.message +
            (props.editedPost.hotlinked_url
              ? " " + props.editedPost.hotlinked_url
              : ""),
      replyTo: props.replyTo
    };

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
    this.props.onSend(this.state.value, this.state.replyTo);
  }

  render() {
    const { replyTo, editedPost, sendDisabled, onSend } = this.props;
    const minRows = replyTo == null ? 5 : 1;
    const maxRows = replyTo == null ? 30 : 5;
    //const maxHeight = replyTo == null ? 300 : 100;
    const placeholder = replyTo == null ? "Exprimez-vous" : "Un commentaire ?";
    return (
      <div className="wall-post-writer">
        <TextareaAutosize
          //style={{ maxHeight: {maxHeight}, boxSizing: "border-box" }}
          rows={minRows}
          maxRows={maxRows}
          placeholder={placeholder}
          value={this.state.value}
          onChange={e => this.setState({ value: e.target.value })}
        />
        {!sendDisabled && (
          <Button color="primary" variant="outlined" onClick={this.handleClick}>
            Envoyer
          </Button>
        )}
        {sendDisabled && (
          <Button color="primary" variant="outlined" disabled>
            Envoi en cours...
          </Button>
        )}
      </div>
    );
  }
}
