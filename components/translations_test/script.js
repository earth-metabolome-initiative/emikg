// Translations widget
// -------------------
// 
// The translation widjet is a jQuery-based widget that allows website moderators to
// translate a text into a different language.
//
// It is displayed when a moderator user either:
// - clicks 3 times on short succession on an element they want to translate with the class "translatable"
// - hits the hot-keys "Ctrl + Alt + T"
// 
// It is hidden when the user either:
// - clicks on the "translation_widjet_close" button
// - clicks on the background, with id "translation_widjet_background"
// - hits the hot-keys "Ctrl + Alt + T"
// - hits the "Escape" key
//
// The widjet has the ID "translation_widjet".


/**
 * Displayes the translations widget.
 */
function displayTranslationsWidget() {
    var widget = $("#translation_widjet");
    console.log("displayTranslationsWidget");
    widget.show();
}

/**
 * Hides the translations widget.
 */
function hideTranslationsWidget() {
    var widget = $("#translation_widjet");
    console.log("hideTranslationsWidget");
    widget.hide();
}

/**
 * Toggles the translations widget.
 * If the widget is hidden, it is displayed.
 * If the widget is displayed, it is hidden.
 */
function toggleTranslationsWidget() {
    var widget = $("#translation_widjet");
    if (widget.is(":visible")) {
        hideTranslationsWidget();
    } else {
        displayTranslationsWidget();
    }
}

/**
 * Hides the translations widget if it is visible upon the user clicking ESC.
 */
function hideTranslationsWidgetOnEsc() {
    $(document).keyup(function(e) {
        if (e.keyCode == 27) {
            hideTranslationsWidget();
        }
    });
}

/**
 * Hides the translations widget if the user clicks on the background.
 * The background has the ID "translation_widjet_background".
 */
function hideTranslationsWidgetOnBackgroundClick() {
    $("#translation_widjet_background").click(function() {
        hideTranslationsWidget();
    });
}

/**
 * Hides the translations widget if the user clicks on the "translation_widjet_close" button.
 */
function hideTranslationsWidgetOnCloseButtonClick() {
    $("#translation_widjet_close").click(function() {
        hideTranslationsWidget();
    });
}

/**
 * Shows the translations widget if the user clicks 3 times in short succession on an element with the class "translatable".
 */
function showTranslationsWidgetOnTripleClick() {
    var clicks = 0;
    var timeout = 0;
    $(".translatable").click(function() {
        clicks++;
        if (clicks == 1) {
            timeout = setTimeout(function() {
                clicks = 0;
            }, 400);
        } else if (clicks == 3) {
            clearTimeout(timeout);
            clicks = 0;
            displayTranslationsWidget();
        }
    });
}

/**
 * Toggle the translations widget if the user hits the hot-keys "Ctrl + Alt + T".
 */
function toggleTranslationsWidgetOnHotKeys() {
    $(document).keydown(function(e) {
        if (e.ctrlKey && e.altKey && e.keyCode == 84) {
            toggleTranslationsWidget();
        }
    });
}

/**
 * Enables all of the events described above upon the document being ready.
 */
$(document).ready(function() {
    hideTranslationsWidgetOnEsc();
    hideTranslationsWidgetOnBackgroundClick();
    hideTranslationsWidgetOnCloseButtonClick();
    showTranslationsWidgetOnTripleClick();
    toggleTranslationsWidgetOnHotKeys();
});