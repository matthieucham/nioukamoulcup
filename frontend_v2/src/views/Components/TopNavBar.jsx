import { Component } from 'react';
import { Anchor, Box, Button, Heading, ResponsiveContext } from 'grommet';
import { Header } from 'grommet-controls';
import { Home, Info, Menu, User } from 'grommet-icons';

const TopMenu = () => (
  <ResponsiveContext.Consumer>
    {size => (
      <Box>
        {size !== 'small' ? (
          <Box direction="row" justify="end">
            <Anchor href="#" icon={<Home />} />
            <Anchor href="#" icon={<Info />} />
            <Anchor href="#" icon={<User />} />
          </Box>
        ) : (
          <Button icon={<Menu />} />
        )}
      </Box>
    )}
  </ResponsiveContext.Consumer>
);

class TopNavBar extends Component {
  state = {};

  render() {
    return (
      <Box>
        <Header position="sticky" elevation={0}>
          <Heading level="3" margin="none">
            Kamoulcup
          </Heading>
          <TopMenu />
        </Header>
      </Box>
    );
  }
}

export default TopNavBar;
