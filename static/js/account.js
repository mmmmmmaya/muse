function changeDetails(evt){
    checkFieldMissing('name');
    checkFieldMissing('email');

    showAlerts(evt);
}

$('#update-account-form').submit(changeDetails);


function changePassword(evt) {

    checkFieldMissing('old-password');
    checkFieldMissing('password');
    checkPasswordsMatch();

    showAlerts(evt);
}

$('#update-password-form').submit(changePassword);
