describe('Tests recording functionality', function() {

    it('should turn recording on and off', function () {
        var recording = appIsRecording;
        toggleRecording();
        expect(recording).not.toBe(appIsRecording);
    });

    it('should send recordings to the server and clear recordingArray', function(done) {
        var recordingArray = [{'timestamp': 123,
                               'key': 'a',
                               'theme': 1}];

        sendSongToServer();

        expect(recordingArray.length).toBe(0);
        done();
    });

    it('should update status message div', function() {
        var msg = $('#save-message-div');

        updateMsgDivStatus('test status');

        expect(msg.html).not.toBe('');
        expect(msg.html).toBe('test status');
    });

    it('should clear the status message div', function() {
        var msg = $('#save-message-div');
        updateMsgDivStatus('test status');

        clearMsgDiv();

        expect(msg.html).toBe('');
        expect(msg.html).not.toBe('test status');
    });

    it('should know what is a letter', function() {
        var notLetter = ']';
        var letter = 'a';

        var shouldBeFalse = isLetter(notLetter);
        var shouldBeTrue = isLetter(letter);

        expect(shouldBeTrue).toBe(true);
        expect(shouldBeFalse).toBe(false);
    });

    it('should play sounds and animations', function() {

    });

    it('should add keypresses to a recording', function() {

    });

    it('should be able to change the theme', function() {
        var theme = currentTheme;

        nextTheme();

        expect(theme).not.toBe(currentTheme);
        expect(currentTheme).toBe(theme + 1);
    });

    it('should track the konami code easter egg', function() {

    });

});