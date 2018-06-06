"use strict";

/**************************************************
 * Обработка нажатия кнопки "ДОБАВИТЬ В КОРЗИНУ" *
 * ************************************************/

// обработка событий
// сменить выбранную позицию товара
$('input[name=product_item]').on('change', function () {
    $('#productId').val($(this).val());
});


$('body').on('click', '.jsAddToCart', function(event){
    event.preventDefault();
    var data, url, productId;
    // добавить товар с каталога
    if ($(this).data('isCatalog')){
        data = {
            'product_id': $(this).data('productId'),
            'quantity': 1
        };
        url = '/cart/add/';
    }
    // добавить товар с карточки товара
    else {
        productId = $('#productId').val();
        if (productId === ''){
            alert('Не выбран вариант товара');
            return false;
        }

        data = {
            'product_id': productId,
            'quantity': $('#quantity').val()
        };
        url = location.pathname;
    }

    addCart(data, url);
});

function addCart(data, url) {
    $.ajax({
        url : url,
        type : "POST",
        data: data,

        success : function(json) {
            // Оповестить о результате добавлении товара
            var div = createPopup(json);
            var link_del = document.createElement('a');
            link_del.innerText = 'x';
            link_del.className = 'del_popup';

            div.appendChild(link_del);
            $('body').append(div);
            // преждевременное удаление
            $(link_del).click(function () {
                deleteElement($(div), 100);
            });
            deleteElement($(div));

            // Изменить общие данные корзины в шапке сайта
            var oldTotalCartQty = Number($('.jsTotalCartQty').text());
            var oldTotalCartPrice = parseFloat($('.jsTotalCartPrice').text());
            $('.jsTotalCartQty').text(oldTotalCartQty + json.quantity);
            $('.jsTotalCartPrice').text(oldTotalCartPrice + (json.price * json.quantity));

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            var logError = xhr.status + ':' + xhr.responseText.slice(0, 100) + '...';
            $('#ajaxError').html("<div class='alert-danger text-center'>Oops! Что то пошло не так :(" +
                "<br>Если ошибка повториться, пожалуйста, сообщите нам о ней!<br><code>"+logError+"</code></div>");
        }
    });
};


/**********************************************************************************
 * Создать элемент для оповещения
 *
 * @param data(json) - данные: ответа от сервера(!)
 * ********************************************************************************/
var createPopup = function (data) {
    var msg = '<b>ТОВАР ДОБАВЛЕН!</b><br>' +
        '<span>' + data.name + ' - </span><b>'+data.quantity+' шт.</b><br>' +
        '<small class="text-muted">' + data.articul + '</small>';
    var div = document.createElement('div');
    div.className = 'msg_add_cart';
    div.innerHTML = msg;
    return div;
};


/**********************************************************************************
 * Плавное удаление оповещения
 *
 * @param elem(object) - html элемент(!)
 * @param timeDelta(Number) - отрезок времени, через который элемент нужно удалить
 * ********************************************************************************/
var deleteElement = function (elem, timeDelta) {
    timeDelta = timeDelta || 3000;
    setTimeout(function () { elem.slideUp(); }, timeDelta);
    setTimeout(function () { elem.remove(); }, timeDelta + 1000);
};
