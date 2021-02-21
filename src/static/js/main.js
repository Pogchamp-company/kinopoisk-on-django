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

        if (!button.hasClass('working')){
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
                success: function(data) {
                },
                error: function(data){
                    button.removeClass('working');
                }
            }).done(function(data){
                    //---------------- результаты с бэкэнда
                    //---------------- data.html - массив статей для вставки
                    //---------------- data.last - нужна ли кнопка Больше
                    container.append(data.html);
                    if (data.last){
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
