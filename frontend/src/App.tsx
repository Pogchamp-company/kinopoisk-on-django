import React from 'react';
import './App.scss';
import {
    AppBar,
    Button,
    createTheme,
    IconButton,
    InputAdornment,
    InputBase,
    TextField, ThemeProvider,
    Toolbar,
    Typography
} from "@material-ui/core";

import SearchIcon from '@material-ui/icons/Search';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import StorageIcon from '@material-ui/icons/Storage';
import AccountBoxIcon from '@material-ui/icons/AccountBox';
import MovieIcon from '@material-ui/icons/Movie';
import image from './orig.png';
import image_small from './icon.png';

function App() {
    const theme = createTheme({
        palette: {
            type: 'dark',
        },
    });

    return (
        <ThemeProvider theme={theme}>
            <div className="App">

                <header className={"nav-container"}>
                    <div className={"nav-icons-container"}>
                        <img className={"nav__image big"} src={image} alt={"Logo"}/>
                        <MovieIcon className={"nav__image small"} fontSize={"large"}/>
                    </div>
                    <TextField className={"search-input"}
                               placeholder="Поиск"
                               InputProps={{
                                   startAdornment: (
                                       <InputAdornment position="start">
                                           <SearchIcon/>
                                       </InputAdornment>
                                   ),
                               }}
                               variant={"outlined"}
                               style={{width: '50ch'}}
                    />
                    <div className={"nav-icons-container"}>
                        <StorageIcon fontSize={"large"}/>
                        <AccountBoxIcon fontSize={"large"}/>
                        <ExitToAppIcon fontSize={"large"}/>
                    </div>
                </header>
            </div>
        </ThemeProvider>
    );
}

export default App;
