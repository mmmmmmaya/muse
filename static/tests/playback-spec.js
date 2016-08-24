describe('Tests playback functionality', function() {

    it('should play a recording', function() {
        var temp_app = {
            waitThenPress: waitThenPress
        };

        spyOn(temp_app, 'waitThenPress');

        var keypresses = [{
            "timestamp": 123,
            "key": 'a',
            "theme": 2
        }]

        playbackRecording(keypresses);

        expect(waitThenPress).toHaveBeenCalled();
    });

    it('should wait a specific amount of time and then action app', function() {
        var temp_app = {
            actionApp: actionApp
        };

        spyOn(temp_app, 'actionApp');

        var start = Date.now();
        var wait = 200;
        var keypress = {
            "timestamp": 123,
            "key": 'a',
            "theme": 2
        }

        waitThenPress(keypress, wait);

        expect(currentTheme).toBe(2);
        expect(Date.now()).toBeGreaterThan(start+wait);
        expect(actionApp).toHaveBeenCalled();
    })

});