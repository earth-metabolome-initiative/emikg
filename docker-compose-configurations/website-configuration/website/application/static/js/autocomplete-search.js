// Autocomplete search
// -------------------
// A simple jQuery autocomplete search that performs
// ajax searches in response to the user typing in an
// input field. Specifically, we identify all output
// areas of interest as ul objects with class "autocomplete-search".
//
// All of these objects will necessarily have three attributes,
// one the name of the input field to monitor, second the action
// containing the URL to which to send the ajax request and third
// the method to use for the ajax request, either "GET" or "POST".
//
// As the user types in the input field, we send an ajax request
// to the specified URL with the input field value as the value
// of the "search" parameter. As the user types, we send a new
// request every 500 milliseconds. The response is expected to
// be a JSON object with a list of dictionaries, which are provided
// one-by-one to the function 'create_search_result' to populate
// the autocomplete search results, i.e. the child of the ul object.
//
// The JSON object is expected to have the following structure:
// {
//   "results": [
//     {
//       "id": "id1",
//       "name": "name1",
//       "description": "description1"
//     },
//     {
//       "id": "id2",
//       "name": "name2",
//       "description": "description2"
//     },
//     ...
//   ]
// }
//
// The function 'create_search_result' is expected to return a
// jQuery object that will be appended to the ul object.
//

// Create a search result
//
// target: the name of the type of target, such as 'taxons' or 'samples'
// result: a dictionary with the keys 'id', 'name' and 'description'
function create_search_result(target, result) {
    var li = $('<li></li>');
    var a = $('<a></a>');
    var span = $('<span></span>');
    // We retrieve the language from the html tag.
    var lang = $('html').attr('lang');
    // We compose the URL from the lang, target and the id.
    var url = '/' + lang + '/' + target + '/' + result.id;
    a.attr('href', url);
    a.text(result.name);
    span.text(result.description);
    li.append(a);
    return li;
}

// Autocomplete search
//
// This function is called when the document is ready.
// It sets up the autocomplete search for all ul objects
// with class "autocomplete-search".
function autocomplete_search() {
    // For each ul object with class "autocomplete-search"...
    $('ul.autocomplete-search').each(function() {
        // We retrieve the input field name, the action and the method.
        var input_name = $(this).attr('for');
        var action = $(this).attr('action');
        var url = "/autocomplete-" + action + "/";
        var method = $(this).attr('method');
        // We retrieve the input field.
        var input = $('input[name="' + input_name + '"]');
        // We set up a timeout to send the ajax request every 500 milliseconds.
        var timeout = null;
        input.keyup(function() {
            // If there is a timeout, we clear it.
            if (timeout) {
                clearTimeout(timeout);
            }
            // We set up a new timeout.
            timeout = setTimeout(function() {
                // We retrieve the search value.
                var search = input.val();
                // We create a loader, i.e. a span object with class "loader".
                var loader = $('<span></span>');
                loader.addClass('loader');
                // We send the ajax request.
                $.ajax({
                    url: url,
                    method: method,
                    data: {
                        search: search
                    },
                    success: function(data) {
                        // We empty the ul object.
                        $(this).empty();
                        // We iterate over the results.
                        for (var i = 0; i < data.length; i++) {
                            // We create a search result.
                            var result = create_search_result(action, data[i]);
                            // We append the search result to the ul object.
                            $(this).append(result);
                        }
                    },
                    complete: function() {
                        // We hide the loader.
                        loader.remove();
                    }
                });
            }, 500);
        });
    });
}

$(document).ready(autocomplete_search);