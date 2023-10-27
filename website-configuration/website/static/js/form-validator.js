// Set of functions to validate the form, first
// via client-side and then via server-side.
//
// We validate all input fields with class "validate".
// We performs some validations by default, unless a specific
// attribute is present in the input field. For instance, we
// assume that all input fields cannot be empty, unless the
// attribute "empty" is present in the input field.
// Similarly, some specific validations are performed only if
// a specific attribute is present in the input field.
//
// Since we need to provide uniform error messages both when
// validating the form via client-side and server-side, and
// we need them to be adapted to the language of the user,
// we use a method called 'get_translation' that retrieves the
// error message from the backend associated to a given label
// and user language, as defined by the 'lang' attribute of
// the html tag.
//

// The translations vocabulary.
var translations = {};

// Function that retrieves the error message from the backend
// associated to a given label and user language.
//
// label: the label of the input field
//
function get_translation(label) {
    // If the label is already present in the client-side
    // translations vocabulary, we return it.
    if (label in translations) {
        return translations[label];
    }

    // We retrieve the language from the html tag.
    // var lang = $('html').attr('lang');

    // // We compose the URL from the lang and the label.
    // var url = '/' + lang + '/translation/' + label;

    // // We retrieve the message from the backend.
    // var message = $.ajax({
    //     url: url,
    //     async: false
    // }).responseText;
    return label;
}

function form_is_valid(form) {
    var valid = true;
    form.find('.validate').each(function () {
        var input = $(this);
        if (!input.hasClass('valid')) {
            valid = false;
        }
    });
    return valid;
}

// Function that displayes a new error message
// under the input field.
function show_error_message(input, message_label) {
    // We retrieve the error message from the backend.
    var message = get_translation(message_label);
    // We create a new span object with class "error-message".
    var p = $('<p></p>');
    p.addClass('error-message');
    // We add an attribute "for" to the span object
    // with the name of the input field.
    p.attr('for', input.attr('name'));
    p.text(message);
    // We find the parent p containing the input field.
    var parent = input.parents('fieldset');
    // We append the p object after the parent.
    parent.after(p);
    // We hide the error message after 10 seconds, or
    // after the user clicks on the error message.
    setTimeout(function () {
        p.remove(300);
    }, 10 * 1000);
    p.click(function () {
        p.remove(300);
        input.focus();
    });
}

// Function that checks if the input is empty.
function check_not_empty(input) {
    // If the input has the attribute "empty", we return true.
    if (input.attr('empty') != undefined) {
        return true;
    }
    // If the input field is an input of type file, we check whether
    // the input has a file.
    if (input.attr('type') == 'file') {
        // We retrieve the value of the input field.
        var files = input.prop('files');
        // If the input field has no file, we return the error message.
        if (files.length == 0) {
            show_error_message(
                input,
                "empty_input_field"
            );
            return false;
        }
        return true;
    }

    // We retrieve the value of the input field.
    var value = input.val();
    // We strip the value of the input field.
    value = value.trim();
    // If the input field is empty, we return the error message.
    if (value == '') {
        show_error_message(
            input,
            "empty_input_field"
        );
        return false;
    }
    return true;
}

// Function that checks whether the provided field has
// the must_be_equal_to attribute, and if so, whether
// the value of the field is equal to the value of the
// field with the name provided by the must_be_equal_to
// attribute.
function check_must_be_equal_to(input) {
    // If the input has the attribute "must_be_equal_to",
    // we check whether the value of the input field is
    // equal to the value of the input field with the name
    // provided by the must_be_equal_to attribute.
    if (input.attr('must_be_equal_to') != undefined) {
        // We retrieve the value of the input field.
        var value = input.val();
        // We retrieve the value of the attribute.
        var expected_value = input.attr('must_be_equal_to');
        // If the values are not equal, we return the error message.
        if (value != expected_value) {
            show_error_message(
                input,
                "must_be_equal_to"
            );
            return false;
        }
    }
    return true;
}

// Function that checks whether the provided field has a value
// that is contained within the group defined by the group attribute.
// The group attribute can either be 'taxon-name' or 'sample-name', 'taxon-id' or 'sample-id'. An
// error message is displayed if the value is not contained within
// the group.
function check_in_group(input) {
    // If the input has the attribute "in-group",
    // we check whether the value of the input field is
    // equal to the value of the input field with the name
    // provided by the must_be_equal_to attribute.
    if (input.attr('in-group') != undefined) {
        // We retrieve the value of the input field.
        var value = input.val();
        // We retrieve the value of the attribute.
        var group = input.attr('in-group');
        // We execute an ajax request to check whether the value
        // is contained within the group.
        let url = '/validate/' + group;
        let data = {
            candidate: value
        };
        let status = false;
        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            async: false,
            success: function (data) {
                status = data['valid'];
                if (data['valid'] == false) {
                    show_error_message(
                        input,
                        "not_in_group"
                    );
                }
            }
        });
        return status;
    }
    return true;
}

// Function that checks whether the provided field has a value
// that is not contained within the group defined by the group attribute.
function check_not_in_group(input) {
    // If the input has the attribute "not-in-group",
    // we check whether the value of the input field is
    // equal to the value of the input field with the name
    // provided by the must_be_equal_to attribute.
    if (input.attr('not-in-group') != undefined) {
        // We retrieve the value of the input field.
        var value = input.val();
        // We retrieve the value of the attribute.
        var group = input.attr('not-in-group');
        // We execute an ajax request to check whether the value
        // is contained within the group.
        let url = '/validate/' + group;
        let data = {
            candidate: value
        };
        let status = false;
        $.ajax({
            url: url,
            method: 'POST',
            data: data,
            async: false,
            success: function (data) {
                status = !data['valid'];
                if (data['valid']) {
                    show_error_message(
                        input,
                        "in_group"
                    );
                }
            }
        });
        return status;
    }
    return true;
}

function check_mime_type(input) {
    // If the input has the attribute "mime-type",
    // which is only allowed on input fields of type
    // file, we check whether the mime type of the file
    // is equal to the value of the attribute.
    // The mime type may be a comma-separated list of
    // mime types.
    if (input.attr('mime-type') != undefined) {
        // We retrieve the value of the input field.
        var files = input.prop('files');
        // We retrieve the value of the attribute.
        var mime_types = input.attr('mime-type').split(',');
        // We iterate across the files.
        for (var i = 0; i < files.length; i++) {
            // We retrieve the file.
            var file = files[i];
            // We retrieve the mime type of the file.
            var mime_type = file.type;
            // We check whether the mime type is in the list
            // of allowed mime types.
            if (mime_types.indexOf(mime_type) == -1) {
                show_error_message(
                    input,
                    "invalid_mime_type"
                );
                return false;
            }
        }
    }
    return true;
}
    

function validation_callback(input) {
    // We check whether the input already has a last-valid-value
    // attribute. If it has, we check that it is not equal to the
    // current value, otherwise we return.
    if (input.attr('last-validated-value') != undefined && input.attr('last-validated-value') != "" && input.attr('last-validated-value') == input.val()) {
        return;
    }
    // We remove error messages associated
    // to the input field, as defined by p objects
    // with the class "error-message" and with
    // the attribute "for" equal to the name of the
    // input field.
    $('p.error-message[for="' + input.attr('name') + '"]').remove();

    // We set the last-valid-value attribute to the
    // current value of the input field.
    input.attr('last-validated-value', input.val());

    // We retrieve the label associated to the input field,
    // that is the label with the attribute "for" equal to
    // the name of the input field.
    var label = $('label[for="' + input.attr('name') + '"]');

    // We check if the input is empty.
    if (
        check_not_empty(input) &&
        check_must_be_equal_to(input) &&
        check_in_group(input) &&
        check_not_in_group(input) &&
        check_mime_type(input)
    ) {
        input.removeClass('error');
        label.removeClass('error');
        input.addClass('valid');
        label.addClass('valid');
    } else {
        input.removeClass('valid');
        label.removeClass('valid');
        input.addClass('error');
        label.addClass('error');
    }
    // If the parent form is now valid, we enable the submit button.
    input.parents('form').find('button[type="submit"]').prop('disabled', !form_is_valid(input.parents('form')));
}

// We set up a timeout to validate the input after 300 milliseconds.
var timeout = null;
function timed_validation_callback(input) {
    // If there is a timeout, we clear it.
    if (timeout) {
        clearTimeout(timeout);
    }
    // We set up a new timeout.
    timeout = setTimeout(function () {
        validation_callback(input);
    }, 300);
}

$(document).ready(function () {
    // When the user goes out of focus of the input with
    // class "validate", we validate the input.
    $('.validate').blur(function () {
        if ($(this).attr('type') == 'file') {
            return;
        }
        timed_validation_callback($(this));
    });

    // When the user has a keyup event on the input with
    // class "validate", and stops typing for 300 milliseconds,
    // we validate the input.
    $('.validate').keyup(function () {
        timed_validation_callback($(this));
    });

    // We iterate across all form objects and if any of them
    // contains an input field with class "validate" which does
    // not have the class "valid", we disable the submit button.
    $('form').each(function () {
        var form = $(this);
        if (!form_is_valid(form)) {
            form.find('button[type="submit"]').prop('disabled', true);
        }
    });

    // We iterate across all form objects and if any of them
    // contains an input field with class "validate" which does
    // not have the class "valid", we prevent the form from
    // being submitted.
    $('form').submit(function (event) {
        // We always stop the form from being submitted.
        event.preventDefault();
        // We check if the form is valid.
        if (!form_is_valid($(this))) {
            // If the form is not valid, we return.
            return;
        }
        // We send the form via ajax.
        var form = $(this);
        var url = form.attr('action');
        var method = form.attr('method');

        $.ajax({
            url: url,
            method: method,
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            beforeSend: function () {
                // We disable the submit button.
                form.find('button[type="submit"]').prop('disabled', true);
                // We display all objects with class show-before-send.
                form.find('.show-before-send').show(300);
                // We hide all objects with class hide-before-send.
                form.find('.hide-before-send').hide(300);
            },
            complete: function () {
                // We wait for 3 seconds before hiding the elememts, so
                // to allow the user to understand that the task was
                // successfull.
                setTimeout(function () {
                    // We hide all objects with class show-before-send.
                    form.find('.show-before-send').hide(300);
                    // We show all objects with class hide-before-send.
                    form.find('.hide-before-send').show(300);
                }, 3 * 1000);
            },
            xhr: function() {
                // If the form contains a progress bar, we
                // update its content upon progress of the upload.
                if (form.find('.progress-bar').length == 0) {
                    return null;
                }
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function(evt) {
                    if (evt.lengthComputable) {
                        var percentComplete = ((evt.loaded / evt.total) * 100);
                        $(".progress-bar").width(percentComplete + '%');
                        // We format the completion percentage as an
                        // integer.
                        let percentage_text = Math.round(percentComplete);
                        $(".completion-percentage").html(percentage_text+'%');
                    }
                }, false);
                return xhr;
            },
            success: function (data) {
                // We clear out the form.
                form.find('input').val('');
                form.find('textarea').val('');

                // We remove the "valid" class from
                // all labels with class "validate" within
                // the form.
                form.find('input').removeClass('valid');
                form.find('textarea').removeClass('valid');
                form.find('label.valid').removeClass('valid');

                // We remove the "dropped" class from
                // all labels with class "dropzone" within
                // the form.
                form.find('label.dropzone').removeClass('dropped');

                // Disable submit button.
                form.find('button[type="submit"]').prop('disabled', true);

                // On success, we redirect the user to the
                // page defined by the url attribute of the
                // data returned, if any.
                if (!('redirect_url' in data)) {
                    return;
                }

                var redirect_url = data['redirect_url'];
                window.location.replace(redirect_url);
            },
            error: function (xhr, textStatus, errorThrown) {
                var data = xhr.responseJSON;
                // We retrieve the error messages from the backend.
                var errors = data['errors'];
                // We iterate across the error messages.
                for (var i = 0; i < errors; i++) {
                    // We retrieve the error message.
                    var error = errors[i];
                    // We retrieve the input field.
                    var input = form.find('input[name="' + error['field'] + '"]');
                    // We display the error message.
                    show_error_message(input, error['message']);
                }
            }
        });
    });

    // For all labels of file inputs with class dropzone,
    // we handle the drop, dragin and dragout events.
    $('label.dropzone').each(function () {
        var label = $(this);
        var input = label.find('input[type="file"]');
        // We handle the drop event.
        label.on('drop', function (event) {
            event.preventDefault();
            event.stopPropagation();
            // We remove the class "dragover" from the label.
            label.removeClass('dragover');
            // We retrieve the files.
            var files = event.originalEvent.dataTransfer.files;
            // We set the files in the input field.
            input.prop('files', files);
            // We add the dropped property to the dropzone.
            label.addClass('dropped');
            // If the associated input file has
            // the class validate, we validate it.
            if (input.hasClass('validate')) {
                timed_validation_callback(input);
            }
        });

        // We also need to handle the event where the user
        // clicks and then selects a file.
        input.change(function () {
            // We add the dropped property to the dropzone.
            // If there is a file, we add the dropped property
            // to the dropzone.
            if (input.prop('files').length > 0) {
                label.addClass('dropped');
            } else {
                label.removeClass('dropped');
            }
            // If the associated input file has
            // the class validate, we validate it.
            if (input.hasClass('validate')) {
                timed_validation_callback(input);
            }
        });

        // We handle the dragover event.
        label.on('dragover', function (event) {
            event.preventDefault();
            event.stopPropagation();
            // We add the class "dragover" to the label.
            label.addClass('dragover');
        });

        // We handle the dragout event.
        label.on('dragout', function (event) {
            event.preventDefault();
            event.stopPropagation();
            // We remove the class "dragover" from the label.
            label.removeClass('dragover');
        });
    });
});