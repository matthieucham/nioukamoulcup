import React from 'react';
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
  CardActions,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

import WideBand from '../../Components/WideBand';
import cover from '../../../static/img/cover.png';

const useStyles = makeStyles({
  card: {
    maxWidth: 345,
  },
  media: {
    height: 140,
  },
  actions: {
    marginLeft: 'auto',
  },
});

export default function LeaguesBand() {
  function PreferredLeague() {
    const classes = useStyles();
    return (
      <Card className={classes.card}>
        <CardMedia image={cover} title="KDF" className={classes.media} />
        <CardContent>
          <Typography gutterBottom variant="h5">
            KDF
          </Typography>
          <Typography variant="body2" color="textSecondary" component="p">
            Saison 2019-2020
          </Typography>
        </CardContent>
        <CardActions disableSpacing>
          <Button size="small" className={classes.actions}>Choisir une autre ligue</Button>
        </CardActions>
      </Card>
    );
  }

  return (
    <WideBand>
      <PreferredLeague />
    </WideBand>
  );
}
