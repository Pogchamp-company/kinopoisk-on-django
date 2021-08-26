import React from 'react';
import './App.scss';
import {createTheme, ThemeProvider} from "@material-ui/core";

import {Header} from "./Components/Header/Header";
import {blue, orange} from "@material-ui/core/colors";
import {MainPage} from "./Pages/Main/Main";

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

    return (
        <ThemeProvider theme={theme}>
            <Header/>
            <MainPage/>
        </ThemeProvider>
    );
}

export default App;
