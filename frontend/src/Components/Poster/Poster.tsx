import React from "react";
import {Button} from "@material-ui/core";
import "./Poster.scss"

// @ts-ignore
export function Poster(props) {
    return (
        <div className={"poster__container"}>
            <div className={'poster__description'}>
                <h2>{props.movie.name}</h2>

                <Button className="CheckButton" variant="contained">
                    Смотреть
                </Button>
            </div>
            <img className={"poster__image"} src={props.movie.src} alt=""/>
        </div>
    )
}