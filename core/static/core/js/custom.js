// jQuery Script

$(function () {
    console.log('Info: jQuery & Document loaded');

    // CSRF Config
    let csrftoken = Cookies.get('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    console.log('Info: CSRF Config done');

    $('button.btn-save').on('click', function (event) {
        console.log('Info: Save button clicked');
        let btn_id = $(this).attr("id");
        let substitute_id = $('#substitute_'+btn_id);
        event.preventDefault();
        $.ajax({
            url: '/product/save/',
            data: {
                'substitute': substitute_id.val()
            },
            dataType: 'json',
            success: function(data){
                if (data.success) {
                    alert(data['message'])
                }
                else {
                    alert(data['message'])
                }
            }
        })
    });
});