'use strict';

/****************************************************
 *      Обработка действий на странице "КОРЗИНА"    *
 * **************************************************/


$('input[name=quantity]').on('change', function(event){
    event.preventDefault();
    var productId = Number(event.target.id.replace('quantity_id_', ''))
        ,qty = Number(event.target.value)
        ,data = {"product_id" : productId, "quantity" : qty};
    if (productId)
        editCart(data);
    else console.warn('[!] Не передан ID товара.')
});

function editCart(data) {
    $.ajax({
        url : location.pathname,
        type : "POST",
        data : data,

        success : function(json) {
            $('.jsTotalCartQty').text(getTotalCartQty());
            $('#totalProductPrice'+json.product_id).text(json['total_price_product'].toFixed(2));
            $('.jsTotalCartPrice').text(getTotalCartPrice().toFixed(2));

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#ajaxError').html("<div class='alert-danger text-center'>Oops! Произошла непредвиденная ошибка. <br>Просим сообщить нам о ней! <br>" + errmsg +
                "<a href='#'>&times;</a></div>");
            // *console.warn(xhr.status + ": " + xhr.responseText);
        }
    });
};


var getTotalCartQty = function () {
    // общее кол-во всего в корзине
    var inputQty = $('input[name=quantity]')
        ,totalCartQty = 0
        ,i = 0;
    for(i; i < inputQty.length; i++){
        totalCartQty += Number(inputQty[i].value);
    }
    return totalCartQty;
};

var getTotalCartPrice = function () {
    // общая цена за все товары
    var jsTotalProductPrice = $('.jsTotalProductPrice')
        ,totalCartPrice = 0
        ,i = 0;
    for (i; i < jsTotalProductPrice.length; i++){
        totalCartPrice += (parseFloat(jsTotalProductPrice[i].innerText));
    }
    return totalCartPrice;
};

/*

/!**********************************************************************************
 * Создать элемент для оповещения
 *
 * @param data(json) - данные: ответа от сервера(!)
 * ********************************************************************************!/
var createPopup = function (data) {
    var msg = '<b>ТОВАР ДОБАВЛЕН!</b><br>' +
        '<span>' + data.name + ' - </span><b>'+data.quantity+' шт.</b><br>' +
        '<small class="text-muted">' + data.articul + '</small>';
    var div = document.createElement('div');
    div.className = 'msg_add_cart';
    div.innerHTML = msg;
    return div;
};


/!**********************************************************************************
 * Плавное удаление оповещения
 *
 * @param elem(object) - html элемент(!)
 * @param timeDelta(Number) - отрезок времени, через который элемент нужно удалить
 * ********************************************************************************!/
var deleteElement = function (elem, timeDelta) {
    timeDelta = timeDelta || 5000;
    setTimeout(function () { elem.slideUp(); }, timeDelta);
    setTimeout(function () { elem.remove(); }, timeDelta + 1000);
};
*/
