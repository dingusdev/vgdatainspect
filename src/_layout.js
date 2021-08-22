import {
  Box,
  Container,
  CssBaseline,
  ThemeProvider,
  createMuiTheme,
} from "@material-ui/core";

import bg from './assets/backgroundOpacity.png'
import React from "react";
import { useThemeState } from "./context/theme";

export const light = {
  palette: {
    type: "light"
  },

  overrides: {
    MuiCssBaseline: {
      "@global": {
        body: {
          backgroundImage: `url(${bg})`,
          backgroundImageOpacity: 0.6
        }
      }
    }
  }
};

export const dark = {
  palette: {
    type: "dark",
    primary: {
      main: '#7289da',
      paper: {
        main: '#7289da',
      }
    }
  },

  overrides: {
    MuiCssBaseline: {
      "@global": {
        body: {
          backgroundImage: `url(${bg})`,
          backgroundImageOpacity: 0.6
        }
      }
    }
  }
};

export default function Layout({ children }) {
  const { theme } = useThemeState();

  const lightTheme = createMuiTheme(light);
  const darkTheme = createMuiTheme(dark);

  return (
    <ThemeProvider theme={theme === "light" ? lightTheme : darkTheme}>
      <CssBaseline />
      <Container maxWidth="md">
        <Box marginTop={2}>{children}</Box>
      </Container>
    </ThemeProvider>
  );
}