$('.carousel').carousel({
    interval: 5000,
    wrap: true
});

$(document).ready(function () {
    $('body').on('click', '.button_more', function () {

        var button = $(this);

        console.log("Кнопка 'Больше фильмов' робит")
        document.getElementById("1").id = 2;
        //------------- контейнер для вставки статей
        var container = $('.container-more');

        //------------- ссылка на бэкэнд для запроса "Больше статей"
        var postLink = '/';

        if (!button.hasClass('working')) {
            button.addClass('working');

            //------------- атрибуты для передачи на бэкэнд
            var data = {};
            data.action = 'more';

            //------------- ajax-запрос
            $.ajax({
                url: postLink,
                type: 'POST',
                dataType: 'json',
                data: data,
                success: function (data) {
                },
                error: function (data) {
                    button.removeClass('working');
                }
            }).done(function (data) {
                //---------------- результаты с бэкэнда
                //---------------- data.html - массив статей для вставки
                //---------------- data.last - нужна ли кнопка Больше
                container.append(data.html);
                if (data.last) {
                    button.removeClass('working');
                } else {
                    button.remove();
                }
            });
        }
    });
});

var buttons = document.getElementsByClassName('button_more'),
    forEach = Array.prototype.forEach;

forEach.call(buttons, function (b) {
    b.addEventListener('click', addElement);
});

function addElement(e) {
    var addDiv = document.createElement('div'),
        mValue = Math.max(this.clientWidth, this.clientHeight),
        rect = this.getBoundingClientRect(),
        sDiv = addDiv.style,
        px = 'px';

    sDiv.width = sDiv.height = mValue + px
    sDiv.left = e.clientX - rect.left - (mValue / 2) + px
    sDiv.top = e.clientY - rect.top - (mValue / 2) + px


    addDiv.classList.add("pulse");
    this.appendChild(addDiv)
}

function autocomplete(inp, url) {
    /*the autocomplete function takes two arguments,
    the text field element and an array of possible autocompleted values:*/
    let currentFocus;
    /*execute a function when someone writes in the text field:*/
    $(inp).on("input", function (e) {
        let result_container
        const val = this.value;
        /*close any already open lists of autocompleted values*/
        closeAllLists();
        if (!val) {
            return false;
        }
        currentFocus = -1;
        /*create a DIV element that will contain the items (values):*/

        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json"}
        };
        fetch(`${url}?query=${val}`, requestOptions).then((response) => response.json())
            .then((data) => {
                console.log(data)
                result_container = $('.autocomplete-items')
                if (!result_container.length) {
                    result_container = $("<div/>", {
                        id: this.id + "autocomplete-list",
                        "class": "autocomplete-items"
                    })
                    $(this).parent().append(result_container)
                }
                let result_temp = '';
                if (data.movies.length) {
                    result_temp += `<h3>Фильмы и сериалы</h3>
                                    ${data.movies.map(
                        movie => `<div><a href="/movie/${movie.id}" class="result" style="text-decoration: none"><h5>${movie.title}</h5></a></div>`).join('')}
                                    `
                }
                if (data.persons.length) {
                    result_temp += `<h3>Персоны</h3>
                                     ${data.persons.map(
                        person => `<a href="/person/${person.id}" class="result" style="text-decoration: none"><h5>${person.ru_fullname ? person.ru_fullname : person.fullname}</h5></a>`).join('')}
                                    `
                }
                result_container.html(result_temp);
                result_container.show()
            }).catch((error) => console.log(error))
    });
    /*execute a function presses a key on the keyboard:*/
    $(inp).on("keydown", function (e) {
        let x = document.getElementById(this.id + "autocomplete-list");
        if (x) x = x.getElementsByTagName("div");
        if (e.keyCode === 40) {
            /*If the arrow DOWN key is pressed,
            increase the currentFocus variable:*/
            currentFocus++;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode === 38) { //up
            /*If the arrow UP key is pressed,
            decrease the currentFocus variable:*/
            currentFocus--;
            /*and and make the current item more visible:*/
            addActive(x);
        } else if (e.keyCode === 13) {
            /*If the ENTER key is pressed, prevent the form from being submitted,*/
            e.preventDefault();
            if (currentFocus > -1) {
                /*and simulate a click on the "active" item:*/
                if (x) {
                    history.pushState({}, "", $(x[currentFocus]).find('a').attr("href"))
                    location.reload()
                }
            }
        }
    });

    function addActive(x) {
        /*a function to classify an item as "active":*/
        if (!x) return false;
        /*start by removing the "active" class on all items:*/
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        /*add class "autocomplete-active":*/
        x[currentFocus].classList.add("autocomplete-active");
    }

    function removeActive(x) {
        /*a function to remove the "active" class from all autocomplete items:*/
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove("autocomplete-active");
        }
    }

    function closeAllLists(elmnt) {
        $('.autocomplete-items').hide()
    }

    /*execute a function when someone clicks in the document:*/
    document.addEventListener("click", function (e) {
        if (!$(e.target).hasClass("movie-search")) {
            closeAllLists(e.target);
        }
    })

    $(inp).on("click", function (e) {
        $('.autocomplete-items').show()
    })
    ;
}

try {
    autocomplete(document.getElementsByClassName("movie-search")[0], urlForSearch)
} catch {
}

/*скролер*/
var hidWidth;
var scrollBarWidths = 40;

var widthOfList = function () {
    var itemsWidth = 0;
    $('.list a').each(function () {
        var itemWidth = $(this).outerWidth();
        itemsWidth += itemWidth;
    });
    return itemsWidth;
};

var widthOfHidden = function () {
    var ww = 0 - $('.wrapper').outerWidth();
    var hw = (($('.wrapper').outerWidth()) - widthOfList() - getLeftPosi()) - scrollBarWidths;
    var rp = $(document).width() - ($('.nav-item.nav-link').last().offset().left + $('.nav-item.nav-link').last().outerWidth());

    if (ww > hw) {
        //return ww;
        return (rp > ww ? rp : ww);
    } else {
        //return hw;
        return (rp > hw ? rp : hw);
    }
};

var getLeftPosi = function () {

    var ww = 0 - $('.wrapper').outerWidth();
    try {
        var lp = $('.list').position().left;
        if (ww > lp) {
            return ww;
        } else {
            return lp;
        }
    } catch (e) {
        console.log("Сережа, тестировать не учили?!")
    }

};

var reAdjust = function () {

    // check right pos of last nav item
    try {
        var rp = $(document).width() - ($('.nav-item.nav-link').last().offset().left + $('.nav-item.nav-link').last().outerWidth());
        if (($('.wrapper').outerWidth()) < widthOfList() && (rp < 0)) {
            $('.scroller-right').show().css('display', 'flex');
        } else {
            $('.scroller-right').hide();
        }
        if (getLeftPosi() < 0) {
            $('.scroller-left').show().css('display', 'flex');
        } else {
            $('.item').animate({left: "-=" + getLeftPosi() + "px"}, 'slow');
            $('.scroller-left').hide();
        }
    } catch (e) {
        console.log("Сережа долбоеб");
    }
}

reAdjust();

$(window).on('resize', function (e) {
    reAdjust();
});

$('.scroller-right').click(function () {

    $('.scroller-left').fadeIn('slow');
    $('.scroller-right').fadeOut('slow');

    $('.list').animate({left: "+=" + widthOfHidden() + "px"}, 'slow', function () {
        reAdjust();
    });
});

$('.scroller-left').click(function () {

    $('.scroller-right').fadeIn('slow');
    $('.scroller-left').fadeOut('slow');

    $('.list').animate({left: "-=" + getLeftPosi() + "px"}, 'slow', function () {
        reAdjust();
    });
})

$(document).ready(function () {

    if (!$('*').is('.form-panel')) {
        console.log('лицей вечен');
        return;
    }

    var panelOne = $('.form-panel.two').height(),
        panelTwo = $('.form-panel.two')[0].scrollHeight;

    $('.form-panel.two').not('.form-panel.two.active').on('click', function (e) {
        e.preventDefault();

        $('.form-toggle').addClass('visible');
        $('.form-panel.one').addClass('hidden');
        $('.form-panel.two').addClass('active');
        $('.form').animate({
            'height': panelTwo
        }, 200);
    });

    $('.form-toggle').on('click', function (e) {
        e.preventDefault();
        $(this).removeClass('visible');
        $('.form-panel.one').removeClass('hidden');
        $('.form-panel.two').removeClass('active');
        $('.form').animate({
            'height': panelOne
        }, 200);
    });
});