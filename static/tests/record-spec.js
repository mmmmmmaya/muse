describe("Tests recording functionality", function() {

    it("should turn recording on and off", function () {
        var recording = appIsRecording;
        toggleRecording();
        expect(recording).not.toBe(appIsRecording);
    });

    it("should send recordings to the server and clear recordingArray", function(done) {
        var recordingArray = [{"timestamp": 123,
                               "key": 'a',
                               "theme": 1}];
        var msg = $('#save-message-div');

        sendSongToServer();

        expect(recordingArray.length).toBe(0);
        expect(msg.html).not.toBe('');

        done();
    });

});