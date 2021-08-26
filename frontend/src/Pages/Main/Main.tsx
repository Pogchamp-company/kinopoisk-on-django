import Carousel from "react-material-ui-carousel";
import "./Main.scss"
import img_1 from "../../images/img_1.png"
import img_2 from "../../images/img_2.png"
import img_3 from "../../images/img_3.png"
import {Poster} from "../../Components/Poster/Poster";
import {NewsItem} from "../../Components/NewsItem/NewsItem";


export function MainPage() {
    return (
        <div className={"content"}>
            <div className="main-page-container">
                <Carousel navButtonsAlwaysVisible={true}
                          autoPlay={false}
                          className={"poster__carousel"}
                >
                    <Poster movie={{
                        name: 'Аватар: Легенда об Аанге', src: img_1,
                    }}/>
                    <Poster movie={{
                        name: 'Гравити Фолз', src: img_2,
                    }}/>
                    <Poster movie={{
                        name: 'Друзья', src: img_3,
                    }}/>
                </Carousel>
                <div className={"news__container"}>
                    <NewsItem/>
                    <NewsItem/>
                    <NewsItem/>
                </div>
            </div>
        </div>
    )
}