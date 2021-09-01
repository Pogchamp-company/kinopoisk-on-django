import "./Movie.scss"
import img_1 from "../../images/img_1.png"
import img_5 from "../../images/img_5.png"
import {Link} from "react-router-dom"

interface RolePersonsListParams {
    roleName: string;
}

function RolePersonsList({roleName}: RolePersonsListParams) {
    return (
        <>
            <h3>{roleName}</h3>
            <div className={"movie-page-info__persons"}>
                {
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0].map(person => {
                        return (
                            <div className="person-card">
                                <img src={img_5} alt=""/>
                                <div className={"person-card__description"}>
                                    <p className={"person-card__name"}>Джанкарло Вольпе</p>
                                    <p className={"person-card__role"}>Джанкарло Вольпе</p>
                                </div>
                            </div>
                        )
                    })
                }
            </div>
        </>
    )
}

export function MoviePage() {
    return (
        <div className={"content"}>
            <div className="movie-page-container">
                <div className={"movie-poster__container"}>
                    <h1>Аватар: Легенда об Аанге</h1>
                    <img src={img_1} alt={"Poster"}/>

                </div>

                <div className="movie-page__info">
                    <div className={"movie-page__main-info"}>
                        <h3>Avatar: The Last Airbender</h3>
                        <div><h5>Год:</h5><p>2004</p></div>
                        <div><h5>Жанр:</h5><p>фэнтези, боевик, мультфильм, приключения, семейный</p></div>
                        <div><h5>Категория:</h5><p>Сериал</p></div>
                        <div><h5>Слоган:</h5><p>The Avatar Returns</p></div>
                        <div><h5>Бюджет:</h5><p>$5000000</p></div>
                        <div><h5>Премьера Мир: </h5><p> 21 февраля 2005 г.</p></div>
                        <div><h5>Премьера РФ: </h5><p> -</p></div>
                        <div><h5>Время: </h5><p>0:22:00</p></div>
                    </div>
                    <div className={"movie-page__roles"}>
                        {
                            ['Режиссеры', 'Продюсер', 'Сценарист'].map(value => <RolePersonsList roleName={value}/>)
                        }
                    </div>
                </div>
            </div>
        </div>
    )
}