import React from 'react';
import StarIcon from '@material-ui/icons/Star';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import "./Stars.scss"

type StarsProps = {
    starsCount: number;
    currentCount: number;
    setCount: (count: any) => void;
}
export function Stars(props: StarsProps) {
    return <div className={"stars__container"}>
        {
            Array.from({length: props.starsCount}, (v, k) => k + 1).map(value => {
                if (value <= props.currentCount) return <StarIcon onClick={() => props.setCount(value)}/>
                return <StarBorderIcon onClick={() => props.setCount(value)}/>
            })
        }
    </div>
}