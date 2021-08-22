import { Button, Grid, Paper, Typography, makeStyles } from "@material-ui/core";
import Brightness4Icon from "@material-ui/icons/Brightness4";
import Brightness7Icon from "@material-ui/icons/Brightness7";
import React, { useEffect } from "react";

import { useThemeDispatch } from "../context/theme/context";
import { useThemeState } from "../context/theme";
import IconButton from "@material-ui/core/IconButton";
import { useDispatch } from "react-redux";
import { setSnackbar } from "../context/snackbar/snackbar";
import { Divider } from "@material-ui/core";

import AlertDialog from "../components/aboutModal";

const useStyles = makeStyles((theme) => ({
  formControl: {
    minWidth: 120,
    maxWidth: 300,
  },
  paper: {
    padding: theme.spacing(4),
    margin: "auto",
  },
  img: {
    width: "100%",
  },
  divider: {
    margin: theme.spacing(2),
    height: 4,
  },
  centerText: {
    textAlign: "center",
  },
}));

export default function Users() {
  const classes = useStyles();
  const { theme } = useThemeState();
  const dispatchTheme = useThemeDispatch();
  const _toggleTheme = () => dispatchTheme({ type: "TOGGLE_THEME" });
  const dispatch = useDispatch();

  const [fileExtensionSettings, setFileExtensionSettings] = React.useState({});
  const [fileDescription, setFileDescription] = React.useState("");
  const [uploadedFilename, setUploadedFilename] = React.useState("");

  const fileExtensionRegex = /\.[^.]+$/;

  useEffect(() => {
    try {
      getJSON("https://raw.githubusercontent.com/romh-acking/vgdatainspect/main/rcogfileexts.json", function (status, resp) {
        if (resp) {
          setFileExtensionSettings(resp);
        } else {
          dispatch(setSnackbar(true, "error", `Could not obtains file extension settings json. Received HTTP status code: ${status}`));
        }
      });
    } catch (err) {
      dispatch(setSnackbar(true, "error", `Could not obtains file extension settings json: ${err}`));
    }
    // eslint-disable-next-line
  }, []);

  const checkExtension = (event) => {
    setFileDescription("");

    let file = event.target.files[0];

    let filename = file.name;
    setUploadedFilename(filename);
    let extension = filename.match(fileExtensionRegex);

    if (extension) {
      if (fileExtensionSettings[extension]) {
        setFileDescription(fileExtensionSettings[extension]);
      } else {
        setFileDescription("Unknown file");
      }
    } else {
      dispatch(setSnackbar(true, "error", `File doesn't have extension: ${filename}`));
    }
  };

  function getJSON(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.responseType = "json";

    xhr.onload = function () {
      var status = xhr.status;

      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status);
      }
    };

    xhr.send();
  }

  return (
    <>
      <Paper className={classes.paper}>
        <Grid container justify="space-between" alignItems="flex-start">
          <Grid item>
            <Grid container direction="row" alignItems="center">
              <Grid item>
                <Typography variant="h4">&nbsp;&nbsp;VGDataInspect JS</Typography>
              </Grid>
            </Grid>
          </Grid>

          <Grid item>
            <Grid container spacing={4} alignItems="center">
              <Grid item>
                {fileExtensionSettings ? (
                  <>
                    <label htmlFor="upload-file">
                      <input style={{ display: "none" }} id="upload-file" type="file" onChange={checkExtension} />

                      <Button color="primary" variant="contained" component="span">
                        Check Extension
                      </Button>
                    </label>
                  </>
                ) : null}
              </Grid>

              <Grid item>
                <AlertDialog />
              </Grid>

              <Grid item>
                <IconButton onClick={_toggleTheme}>{theme === "light" ? <Brightness7Icon /> : <Brightness4Icon />}</IconButton>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
        {fileDescription ? (
          <Grid item>
            <Divider className={classes.divider} />

            <Typography className={classes.centerText}>
              Based on the extension,
              <br />"{uploadedFilename}"<br />
              is a(n):
              <br />
              <br />
            </Typography>

            {
              <Typography className={classes.centerText} variant="h5">
                {fileDescription}
              </Typography>
            }
          </Grid>
        ) : null}
      </Paper>

      <br />
    </>
  );
}
