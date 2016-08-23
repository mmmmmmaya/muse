'use strict';

function songRenamed(evt) {
    evt.preventDefault();
    $('#save-message-div').html('Saving ...');

    var data = $(evt.originalEvent.target).serialize();

    $.post("/rename", data, function (data) {
        updateMsgDivStatus(data.status);

        var dataIdSelector = '[data-id*="' + data.id + '"]';

        $('.renameForm').find(dataIdSelector)
                        .attr('value', data.title);
    });
}

$('.renameForm').submit(songRenamed);


function songDeleted(evt) {
    $('#save-message-div').html('Deleting ...');

    var id = $(evt.originalEvent.target).data('id');
    var params = {"id": id};

    $.post("/delete", params, function (data) {
        updateMsgDivStatus(data.status);
        var selector = '[data-id*="' + data.id + '"]';
        $(selector).remove();
    });
}

$('.delete').click(songDeleted);
