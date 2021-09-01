import img_4 from "../../images/img_4.png";
import "./NewsItem.scss"
import {Link} from "react-router-dom"

export function NewsItem() {
    return (
        <Link className="news__item" to={"/movie"}>
            <img src={img_4} alt=""/>
            <div>
                <h2>Аквамен, клоны и могучие рейнджеры в трейлере пятого сезона «Рика и Морти»</h2>
                <p>В сети появился трейлер пятого сезона мультсериала «Рик и Морти»...</p>
            </div>
        </Link>
    )
}