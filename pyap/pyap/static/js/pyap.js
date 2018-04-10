/**
 * визуальные дополнения к административной панели
 */
(function() {
    'use strict';

    // INIT FUNCTIONS --------

    /**
     * Определить и установить Красный шрифт если значение отричательное
     * @param: $input - JQ-element {input|select}
    * */
    var identifyMinisVal = function ($input) {
        var lenInp = $input.length
            ,i = 0;
        for (i; i < lenInp; i++) {
            if (Math.sign($input[i].value < 0)){
                $input[i].className += ' jsMinusVal';
            }
        }
    };


    /**
     * создаем новый элемент input и добавляем в него контент, ститли
     * * */
    var addDOMElement = function(formPost) {
        var newElem = document.createElement("input");
        newElem.type = 'submit';
        newElem.value = 'V';
        newElem.name = '_save';
        newElem.style.position = 'fixed';
        newElem.style.backgroundColor = '#4e7fda';
        newElem.style.top = '0';
        newElem.style.left = '2px';
        newElem.style.zIndex = '888';
        // добавляем только что созданый элемент в дерево DOM
        var nullElem = document.getElementById("org_div1");
        formPost.insertBefore(newElem, nullElem);
    };

    // -------- end INIT FUNCTIONS --------

    identifyMinisVal($('input'));
    identifyMinisVal($('select'));

    // подняться вверх сайта
    var SPEED_UP_DOWN = 300;
    $(function () {
        $(window).scroll(function () {
            if ($(this).scrollTop() != 0) { $('#toTop').fadeIn(); }
            else { $('#toTop').fadeOut(); }
        });
        $('#toTop').click(function () {
            $('body,html').animate({ scrollTop: 0 }, SPEED_UP_DOWN);
        });
    });
    // вниз
    $("#toBottom").click(function () {
        var elementClick = $(this).attr("href");
        var destination = $(elementClick).offset().top;
         $('html').animate({ scrollTop: destination }, SPEED_UP_DOWN);
        return false;
    });


    // // мини-кнопка `сохранить` (если есть на странице форма)
    // console.log(location.pathname.indexOf('admin'))
    // if (document.getElementsByTagName('form').length > 0)   {
    //     var formPost = null;
    //     for (var i = 0; i < document.getElementsByTagName('form').length; i++) {
    //         if (document.getElementsByTagName('form')[i].method === 'post') {
    //             formPost = document.getElementsByTagName('form')[i];
    //             console.log(formPost);
    //             break;
    //         }
    //     }
    //     addDOMElement(formPost)
    // }
    
})();