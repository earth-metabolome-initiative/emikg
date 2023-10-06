$(document).ready(function() {
    $('#hamburgerButton').click(function() {
        $("#LateralBar").toggleClass("displayed");
    });
    // If the users clicks anywhere on the page,
    // we hide the lateral bar.
    $(document).click(function(event) {
        // We retrieve the lateral bar.
        var lateral_bar = $('#LateralBar');
        // We retrieve the hamburger button.
        var hamburger_button = $('#hamburgerButton');
        // We retrieve the target of the event.
        var target = $(event.target);
        // If the target is not the lateral bar, the hamburger button
        // or a child of the lateral bar or the hamburger button,
        // we hide the lateral bar.
        if (
            !target.is(lateral_bar) &&
            !target.is(hamburger_button) &&
            lateral_bar.has(target).length === 0 &&
            hamburger_button.has(target).length === 0
        ) {
            lateral_bar.removeClass('displayed');
        }
    });
});