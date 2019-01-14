import React from "react";
import Card from "@material-ui/core/Card";
import CardHeader from "@material-ui/core/CardHeader";
import CardContent from "@material-ui/core/CardContent";
import { Jersey } from "../FieldPlayer";


const SigningCardHeader = ({ signing }) => (
    <CardHeader
      title={<a href={signing.player.url}>{signing.player.display_name}</a>}
      subheader={
        signing.player.poste + ", " + (signing.player.club ? signing.player.club.nom : "?")
      }
      avatar={<Jersey club={ signing.player.club }/>}
    />
  );

export class SigningCard extends React.Component {
    constructor(props) {
      super(props);
    }
  
    render() {
      const { signing } = this.props;
      return (
        <Card>
          <SigningCardHeader signing={signing} />
        </Card>
      );
    }
  }