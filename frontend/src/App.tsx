import React from 'react';
import './App.scss';
import {createTheme, ThemeProvider} from "@material-ui/core";

import {Header} from "./Components/Header/Header";
import {blue, orange} from "@material-ui/core/colors";
import {MainPage} from "./Pages/Main/Main";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import {MoviePage} from "./Pages/Movie/Movie";
import "./base.scss"

function App() {
    const theme = createTheme({
        palette: {
            type: 'dark',
            primary: {
                main: orange[500],
            },
            secondary: {
                main: blue[500],
            },
        },
    });
    console.log("ssdadsd")

    return (
        <ThemeProvider theme={theme}>
            <BrowserRouter basename={"/react"}>
                <Header/>
                <Switch>
                    {/*<MainPage/>*/}
                    <Route exact path={"/"} component={MainPage}/>
                    <Route exact path={"/movie"} component={MoviePage}/>
                </Switch>
            </BrowserRouter>
        </ThemeProvider>
    );
}

export default App;
