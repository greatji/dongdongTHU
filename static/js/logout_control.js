$(document).ready(function () {
    $.ajax({
        type: 'POST',
        url: base_url + 'api/logout',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({}),
        dataType: 'json',
        success: function (data) {
            location.href = '/index.html';
        }
    })
})