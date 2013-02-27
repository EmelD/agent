function is_array(input) {
    return typeof(input) == 'object' && (input instanceof Array);
}
$(function () {
    $("#selall").click(function  () {
        if  (!$("#selall").is(":checked")){
            $(".table-mytasks-check").removeAttr("checked");
        }
        else{
            $(".table-mytasks-check").attr("checked","checked");
        }

    });
});

function form_send(form_id, url, output_id, button_id, clear, prefix) {
    var options = {
        url: url,
        type: 'post',
        dataType: 'json',
        beforeSubmit: function () {
            $(output_id).removeClass('alert alert-success alert-error').addClass('alert alert-warning');
            $(output_id).html('Пожалуйста подождите...');
            //$(button_id).button('loading');
        },
        success: function (json) {
            $(output_id).empty().removeClass('alert alert-warning');
            $(button_id).button('reset');
            if (json.status && clear !== undefined) {
                if (is_array(clear)) {
                    if (clear[0] === '__all') {
                        $(form_id + ' input').val('');
                        $(form_id + ' textarea').val('');
                    } else {
                        $.each(clear, function (index, value) {
                            $(value).val('');
                        });
                    }
                }
            }
            if (json.messages) {
                if (json.status) {
                    $(output_id).addClass('alert alert-success');
                } else {
                    $(output_id).addClass('alert alert-error');
                }
                $.each(json.messages, function (i, message) {
                    $(output_id).append(message + '<br>');
                });
            }
            if (json.errors) {
                django_errors(form_id, json.errors, prefix);
            }
            if (json.callback) {
                callbacks[json.callback.name](json.callback.params);
            }
            if (json.redirect) {
                $(location).attr('href', json.redirect);
            }
        }
    };
    $(form_id).ajaxSubmit(options);
}

function django_errors(form_id, errors, prefix) {
    if (prefix == undefined) {
        prefix = '';
    }
    $(form_id + ' .help-error').remove();
    $(form_id + ' .control-group').removeClass('error');
    $.each(errors, function (key, value) {
        $('#cg_' + prefix + key).addClass('error');
        $('#id_' + prefix + key).after('<span class="help-block help-error" id="help-block-' + prefix + key + '"></span>');
        $.each(value, function (index, message) {
            $('#help-block-' + prefix + key).append(message + ' ');
        });
    });
}

var callbacks = {
    'add_html' : function add_html(params,result){$(params).html(result)}
};

function expand(div) {
    if ($(div).is(':visible')) {
        $(div).hide();
    } else {
        $(div).show();
    }
}

function cclick(click_div, div){
    if (click_div){
        expand(click_div);
    }
    if ($(div).hasClass('active')){
        $(div).removeClass('active');
    } else {
        $(div).addClass('active');
    }
}

function reset_form(form){
    $(form)[0].reset();
}

function show_opinion(div){
    if ($(div).hasClass('opinions-i opinion-open')){
        $(div).removeClass('opinions-i opinion-open');
        $(div).addClass('opinions-i opinion-hide');
    } else {
        $(div).removeClass('opinions-i opinion-hide');
        $(div).addClass('opinions-i opinion-open');
    }
}

function select_file(file,text){
    $(file).click();
    $(file).change(function(){
        $(this).parent().find('.photo-box-change').find('input').val($(this).val());
        $(text).text($(this).val());
    });
}

function clear_file(file,text){
    $(file).attr('value','');
    $(text).text('Файл не выбран');
}

function shov_beznal(div_hide, div_show, radio, radio2){
    $(div_hide).removeClass('display');
    $(div_hide).addClass('non_display');
    $(div_show).removeClass('non_display');
    $(div_show).addClass('display');
    $(radio).attr('checked', 'checked');
    $(radio2).attr('checked', 'checked');
}

function calculate_commission(div,block){
    val = $(div).val();
    res_comission = val/20;
    res = val-res_comission;
    $(block).text('Коммисия системы 5% (' + res_comission + 'руб.), Вам будет перечислено ' + res + ' руб.')
}

function clear_radio(radio){
    $(radio).find('input').each(function() {
    	 $(this).attr('checked', false);
    });
}

function show_message(id){
    ajax(id,'/message')
}

function select_purses(purse,div){
    ajax('system='+purse+'&csrfmiddlewaretoken='+getCookie('csrftoken'),'/purses');
}

function ajax(data,url){
    $.ajax({
        type: "POST",
        url: url,
        data: data,
        dataType: 'json',
        success: function (json) {
            if (json.errors) {
                alert(json.errors);
            }
            if (json.callback) {
                callbacks[json.callback.name](json.callback.params,json.result);
            }
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function show_hide_block(show, hide){
    if (show.length > 0){
        var i = 0;
        for(i; i < show.length; i++){
            $(show[i]).addClass('display');
            $(show[i]).removeClass('non_display');
        }
    }
    if (hide.length > 0){
        var i = 0;
        for(i; i < hide.length; i++){
            $(hide[i]).removeClass('display');
            $(hide[i]).addClass('non_display');
        }
    }
}

function make_active(block_non_active, block_active){
    if(block_non_active){
        $(block_non_active).removeClass('active');
    }
    if(block_active){
        $(block_active).addClass('active');
    }
}