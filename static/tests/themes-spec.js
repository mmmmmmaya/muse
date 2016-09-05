describe('Tests theme getters and setters functionality', function() {

    it('should know how many themes there are', function () {
        var numThemes = getNumThemes();

        expect(numThemes).toBe(5);
    });

    it ('should know theme color sets', function() {
        var themeColors = getThemeColors(1);

        expect(themeColors.length).toBe(6);
        expect(themeColors[0]).toBe('#fd9696');
    });

    it('should know the background color for a given theme', function() {
        var bgColor = getThemeBg(1);

        expect(bgColor).toBe('#ededed');
    });

    it('should be able to change the theme', function() {
        var theme = currentTheme;

        nextTheme();

        expect(theme).not.toBe(currentTheme);
        expect(currentTheme).toBe(theme + 1);
    });

    it('should update the bgColor to match that of a given theme', function() {
        updateThemeBgColor(2);

        // bg color is stored as rgb in css, but my colors are stored as
        // hex codes. I'll just hard code this color value as rgb instead
        // of trying to calculate it.
        var themeBgColor = 'rgb(255, 245, 238)';
        var currentBgColor = $('body').css('background-color');

        expect(currentBgColor).toBe(themeBgColor);
    });
});