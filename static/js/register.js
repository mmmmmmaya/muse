var alerts = [];

function checkPasswordsMatch() {
    var first_pw = $('#field-password').val();
    var second_pw = $('#field-confirm-password').val();

    if (!(first_pw === second_pw)) {
        alerts.push('Passwords do not match.\n');
    }
}

function checkFieldMissing(fieldName) {
    var id = '#field-' + fieldName;
    var fieldValue = $(id).val();

    if (!(fieldValue && (typeof fieldValue === 'string'))) {
        var message = 'Must fill in ' + fieldName + '.\n';
        alerts.push(message);
    }
}

function formSubmitted(evt){

    checkPasswordsMatch();
    checkFieldMissing('name');
    checkFieldMissing('email');
    checkFieldMissing('password');

    if (alerts.length > 0) {
        evt.preventDefault();
        alert(alerts);
        alerts = [];
    }
}

$('#registration-form').submit(formSubmitted);
