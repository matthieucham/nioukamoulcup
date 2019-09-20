import React from "react";
import TextareaAutosize from "react-autosize-textarea";
import Button from "@material-ui/core/Button";
import CSRFToken from "../csrftoken";
import { LEAGUE_ID } from "../../build";



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
              : "")
    };

    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();
  }

  render() {

    const { replyTo, editedPost } = this.props;
    const minRows = replyTo == null ? 3 : 1;
    const maxRows = replyTo == null ? 30 : 5;
    //const maxHeight = replyTo == null ? 300 : 100;
    const placeholder = replyTo == null ? "Exprimez-vous" : "Réponse";
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
        <Button color="primary" onClick={this.handleClick}>
          Envoyer
        </Button>
      </div>
    );
  }
}
