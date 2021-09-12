// import image from "../../images/orig.png";
import React from "react";
import MovieIcon from "@material-ui/icons/Movie";
import {InputAdornment, TextField} from "@material-ui/core";
import SearchIcon from "@material-ui/icons/Search";
import StorageIcon from "@material-ui/icons/Storage";
import AccountBoxIcon from "@material-ui/icons/AccountBox";
import ExitToAppIcon from "@material-ui/icons/ExitToApp";
import "./Header.scss"
import {Link} from "react-router-dom";

export function Header() {
    return (
        <header className={"nav-container"}>
            <Link to={"/"} className={"nav-icons-container"}>
                <img className={"nav__image big"} src={"/static/img/orig.png"} alt={"Logo"}/>
                <MovieIcon className={"nav__image small"} fontSize={"large"}/>
            </Link>
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
    )
}