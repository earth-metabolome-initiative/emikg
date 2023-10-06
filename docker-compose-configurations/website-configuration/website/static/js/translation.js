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
 * On click of the "translation_item" element, we set the value of the textarea
 * and set the class of the translation item as "selected", removing the class
 * from the previously selected translation item. Additionally, we set the save
 * button as disabled until any edit is made to the textarea.
 */
function selectTranslationItem(translation_item) {
    var textarea = $("#current_translation");
    var translation_label = translation_item.attr("reference-label");
    var textual_item = $("[data-label='" + translation_label + "']");
    textarea.val(textual_item.text());
    $(".selected_translation_item").removeClass("selected_translation_item");
    translation_item.addClass("selected_translation_item");
    $("#save_translation").addClass("disabled");

    // If the translation item happens to not be visible because
    // of the scroll, we scroll to it.
    var translations_list = $("#translations_list");
    var translation_item_position = translation_item.position();
    var translation_item_top = translation_item_position.top;
    var translation_item_height = translation_item.height();
    var translations_list_height = translations_list.height();
    var translations_list_top = translations_list.scrollTop();
    var translations_list_bottom = translations_list_top + translations_list_height;
    var translation_item_bottom = translation_item_top + translation_item_height;
    if (translation_item_top < translations_list_top) {
        translations_list.scrollTop(translation_item_top);
    } else if (translation_item_bottom > translations_list_bottom) {
        translations_list.scrollTop(translation_item_bottom - translations_list_height);
    }

    textarea.focus();
}

/**
 * Pupulate the translations widget's translations_list with elements with the class "translatable".
 */
function populateTranslationsList() {
    var translations = $(".translatable");
    var translations_list = $("#translations_list");
    translations_list.empty();
    var first = true;
    translations.each(function() {
        var translation = $(this);
        var translation_label = translation.attr("data-label");
        var translation_item = $("<li></li>");

        // We set an attribute "reference-label" on the translation_item
        // so that we can easily retrieve the translation_item
        // when the user clicks on it.
        translation_item.attr("reference-label", translation_label);

        translation_item.text(translation_label);
        translations_list.append(translation_item);

        // We set the onclick event of the translation_item
        // to call the selectTranslationItem function if the
        // translation_item is clicked.
        translation_item.click(function() {
            selectTranslationItem(translation_item);
        });

        if (first) {
            first = false;
            selectTranslationItem(translation_item);
        }
    });
}

/**
 * Displayes the translations widget.
 */
function displayTranslationsWidget() {
    var widget = $("#translation_widjet");
    populateTranslationsList();
    widget.show();
}

/**
 * Hides the translations widget.
 */
function hideTranslationsWidget() {
    var widget = $("#translation_widjet");
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

            // We click on the translation_item that has the same "reference-label"
            // as the element that was clicked.
            var translation_label = $(this).attr("data-label");
            var translation_item = $("li[reference-label='" + translation_label + "']");
            translation_item.click();
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
 * When there is any keystroke to the textarea with ID "current_translation",
 * we enable the save button with ID "save_translation".
 */
function enableSaveButtonOnKeystroke() {
    $("#current_translation").keyup(function() {
        $("#save_translation").removeClass("disabled");
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
    enableSaveButtonOnKeystroke();
});