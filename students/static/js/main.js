function initJournal() {
    let indicator = $('#ajax-progress-indicator');

    $('.day-box input[type="checkbox"]').click(function(event){
        let box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1': '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show();
            },
            'error': function(xhr, status, error){
                alert(error);
                indicator.hide();
            },
            'success': function(data, status, xhr) {
                indicator.hide();
            }
        });
    });
}

function initGroupSelector() {
    // look up select element with groups and attach our event handler
    // on field "change" event

    $('#group-selector select').change(function (event) {
        // get value of currently selected group option
        let group = $(this).val();

        if (group) {
            // set cookie with expiration date 1 year since now;
            // cookie creation function takes period in days
            Cookies.set('current_group', group, {'path': '/', 'expires': 365});
        } else {
            // otherwise we delete the cookie
            Cookies.remove('current_group', {'path': '/'});
        }
        // and reload a page
        location.reload(true);
        return true;
    });
}

$(document).ready(function () {
    initJournal();
    initGroupSelector();
});

