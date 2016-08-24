describe('Tests register page functionality', function() {
    afterEach(function() {
        $('#field-name').val('');
        $('#field-email').val('');
        $('#field-password').val('');
        $('#field-confirm-password').val('');

        alerts = [];
    });

    it('should check that two password fields match', function () {
        $('#field-password').val('test');
        $('#field-confirm-password').val('test');

        checkPasswordsMatch();

        expect(alerts.length).toBe(0);
    });

    it('should alert if two password fields do not match', function () {
        $('#field-password').val('test');
        $('#field-confirm-password').val('test1');

        checkPasswordsMatch();

        expect(alerts.length).toBe(1);
    });

    it('should check if all required fields are filled', function() {
        $('#field-name').val('test');
        $('#field-email').val('test@test.com');
        $('#field-password').val('test');

        checkFieldMissing('name');
        checkFieldMissing('email');
        checkFieldMissing('password');

        expect(alerts.length).toBe(0);
    });

    it('should alert if not all required fields are filled', function() {
        checkFieldMissing('name');
        checkFieldMissing('email');
        checkFieldMissing('password');

        expect(alerts.length).toBe(3);
    });

});