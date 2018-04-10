/**
 * визуальные дополнения к административной панели
 */
(function() {
    'use strict';
    // красный шрифт если цифра в input минусовая
    var $inpNumber = $('input[type="number"]');
    var lenInpNumber = $inpNumber.length;
    var i = 0;
    for (i; i < lenInpNumber; i++) {
        if (Math.sign($inpNumber[i].value < 0)){
            $inpNumber[i].className += ' jsMinusVal';
        }
    }

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

    // мини-кнопка `сохранить` (если есть на странице форма)
    if (document.getElementsByTagName('form').length > 0) {
        var formPost = null;
        for (var i=0; i < document.getElementsByTagName('form').length; i++) {
            if (document.getElementsByTagName('form')[i].method === 'post') {
                formPost = document.getElementsByTagName('form')[i];
                console.log(formPost);
                break;
            }
        }
        addDOMElement(formPost)
    } 

})();


function addDOMElement(formPost) {
    // создаем новый элемент div
    // и добавляем в него немного контента
    var newElem = document.createElement("input");
    newElem.type = 'submit';
    newElem.value = 'V';
    newElem.name = '_save';
    newElem.style.position = 'fixed';
    newElem.style.backgroundColor = '#4e7fda';
    newElem.style.top = '0';
    newElem.style.left = '2px';
    // добавляем только что созданый элемент в дерево DOM
    var nullElem = document.getElementById("org_div1");
    formPost.insertBefore(newElem, nullElem);
}  

