/// Translations
///
/// This file is included in the template of the website when the user is logged in
/// and is a moderator. It is used to provide an interface for translating the website
/// into other languages, and to easily allow moderators to correct mistakes in the
/// translations.
/// 
/// The translations are stored in the database, and are loaded into the page when
/// the page is loaded via Jinja population, so no javascript is required to load
/// the translations in the first place. A moderator can then edit the translations
/// by clicking 3 times on the text they want to edit, which causes a popup to appear
/// containing a textarea with the current translation in it. The same interface also
/// includes the language code for the language being translated, and the label associated
/// with the text being translated. The moderator can then edit the translation and click
/// the save button to save the translation to the database.
///
/// The endpoint being used to save the translations via AJAX is /update-label/<lang>/<label>,
/// where <lang> is the language code for the language being translated, and <label> is the
/// label of the text being translated. The endpoint expects a POST request with the new
/// translation in the body of the request. The endpoint will return a 200 status code if
/// the translation was successfully saved, and a 400 status code if the translation was
/// not saved. The endpoint will also return a JSON object with the success message if the
/// translation was saved, and an error message if the translation was not saved.
///
/// The client side text is updated via javascript upon successful saving of the translation,
/// so that the user can see the updated translation without having to refresh the page.
/// The translation popup is also closed upon successful saving of the translation.
///

function tripleClick(element, callback) {
    let clickCount = 0;
    let clickTimeout;

    element.addEventListener("click", function () {
        clickCount++;

        if (clickCount === 1) {
            // First click
            clickTimeout = setTimeout(function () {
                clickCount = 0; // Reset click count if the user doesn't click again within a set time
            }, 300); // Adjust the time window (in milliseconds) for a triple click
        } else if (clickCount === 3) {
            // Third click (triple-click)
            clearTimeout(clickTimeout); // Clear the timeout

            // Call the callback function
            if (typeof callback === "function") {
                callback();
            }

            clickCount = 0; // Reset click count after triple-click
        }
    });
}

/// Set up the event listeners for the triple click on a text with class "translatable"
/// to open the translation popup
function setupTranslationPopup() {
    // Get all the elements with class "translatable"
    let translatableElements = document.getElementsByClassName("translatable");

    // Loop through the elements and add the event listener to each one
    for (let i = 0; i < translatableElements.length; i++) {
        // For each element, we add an event listener for the triple click
        tripleClick(translatableElements[i], function () {
            // When the triple click is detected, we call the function to open the translation popup
            openTranslationPopup(translatableElements[i]);
        });
    }
}

/// Open the translation popup for the given element
function openTranslationPopup(element) {
    // Get the language code and label from the element
    let lang = element.getAttribute("data-lang");
    let label = element.getAttribute("data-label");

    // Get the translation from the element
    let translation = element.innerHTML;

    // Get the translation popup
    let translationPopup = document.getElementById("translation-popup");

    // Get the translation popup form h2 element to update
    // the name of the label currently being translated
    let translationPopupFormH2 = document.getElementById("currentTranslationLabel");

    // Get the translation popup background
    let translationPopupBackground = document.getElementById("translationPopupBackground");

    // Get the translation popup close button
    let translationPopupCloseButton = document.getElementById("translationPopupCloseButton");

    // Get the translation popup form textarea
    let translationPopupFormTextarea = document.getElementById("translation-popup-form-textarea");

    // Get the translation popup form save button
    let translationPopupFormSaveButton = document.getElementById("translationsPopupSubmitButton");

    // Set the translation popup form label input value
    translationPopupFormLabel.value = label;

    // Set the translation popup form textarea value
    translationPopupFormTextarea.value = translation;

    // Set the translation popup form save button onclick function
    translationPopupFormSaveButton.onclick = function () {
        // When the save button is clicked, we call the function to save the translation
        saveTranslation(
            lang,
            label,
            translationPopupFormTextarea.value,
            element
        );
    };

    // We set that a click on the close button or the
    // background should close the translation popup
    translationPopupCloseButton.onclick = function () {
        closeTranslationPopup();
    };

    translationPopupBackground.onclick = function () {
        closeTranslationPopup();
    }

    // Show the translation popup
    translationPopup.style.display = "block";
}

/// Close the translation popup
function closeTranslationPopup() {
    // Get the translation popup
    let translationPopup = document.getElementById("translation-popup");

    // Hide the translation popup
    translationPopup.style.display = "none";
}

/// Save the translation to the database
function saveTranslation(lang, label, updated_translation, element) {
    // Get the translation popup form save button
    let translationPopupFormSaveButton = document.getElementById("translationsPopupSubmitButton");

    // Disable the save button
    translationPopupFormSaveButton.disabled = true;

    // Make the AJAX request to save the translation
    $.ajax({
        url: "/update-label/" + lang + "/" + label,
        type: "POST",
        data: updated_translation,
        contentType: "text/plain",
        success: function (data) {
            // If the translation was successfully saved, we update the text on the page
            // and close the translation popup
            element.innerHTML = updated_translation;
            closeTranslationPopup();
        },
        error: function (error) {
            // If there was an error saving the translation, we display an error message
            // and re-enable the save button
            alert("Error saving translation: " + error.responseText);
            translationPopupFormSaveButton.disabled = false;
        }
    });
}