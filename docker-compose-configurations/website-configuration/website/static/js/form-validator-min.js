var translations={};function get_translation(t){if(t in translations)return translations[t];var a="/"+$("html").attr("lang")+"/translation/"+t;return $.ajax({url:a,async:!1}).responseText}function form_is_valid(t){var a=!0;return t.find(".validate").each((function(){$(this).hasClass("valid")||(a=!1)})),a}function show_error_message(t,a){var r=get_translation(a),e=$("<p></p>");e.addClass("error-message"),e.attr("for",t.attr("name")),e.text(r),t.parent("p").after(e),t.addClass("error"),setTimeout((function(){e.remove(300)}),1e4),e.click((function(){e.remove(300),t.focus()}))}function check_not_empty(t){if(null!=t.attr("empty"))return!0;var a=t.val();return""!=(a=a.trim())||(show_error_message(t,"empty_input_field"),!1)}function check_must_be_equal_to(t){if(null!=t.attr("must_be_equal_to")&&t.val()!=t.attr("must_be_equal_to"))return show_error_message(t,"must_be_equal_to"),!1;return!0}function check_in_group(t){if(null!=t.attr("in-group")){var a=t.val();let r="/validate/"+t.attr("in-group"),e={candidate:a},n=!1;return $.ajax({url:r,method:"POST",data:e,async:!1,success:function(a){n=a.valid,0==a.valid&&show_error_message(t,"not_in_group")}}),n}return!0}function check_not_in_group(t){if(null!=t.attr("not-in-group")){var a=t.val();let r="/validate/"+t.attr("not-in-group"),e={candidate:a},n=!1;return $.ajax({url:r,method:"POST",data:e,async:!1,success:function(a){n=!a.valid,a.valid&&show_error_message(t,"in_group")}}),n}return!0}function validation_callback(t){null!=t.attr("last-valid-value")&&""!=t.attr("last-valid-value")&&t.attr("last-valid-value")==t.val()||($('p.error-message[for="'+t.attr("name")+'"]').remove(),t.attr("last-valid-value",t.val()),check_not_empty(t)&&check_must_be_equal_to(t)&&check_in_group(t)&&check_not_in_group(t)?(t.removeClass("error"),t.addClass("valid")):(t.removeClass("valid"),t.addClass("error")),t.parents("form").find('button[type="submit"]').prop("disabled",!form_is_valid(t.parents("form"))))}var timeout=null;function timed_validation_callback(t){timeout&&clearTimeout(timeout),timeout=setTimeout((function(){validation_callback(t)}),300)}$(document).ready((function(){$(".validate").blur((function(){timed_validation_callback($(this))})),$(".validate").keyup((function(){timed_validation_callback($(this))})),$("form").each((function(){var t=$(this);form_is_valid(t)||t.find('button[type="submit"]').prop("disabled",!0)})),$("form").submit((function(t){if(t.preventDefault(),form_is_valid($(this))){var a=$(this),r=a.attr("action"),e=a.attr("method"),n=a.serialize();$.ajax({url:r,method:e,data:n,success:function(t){if(a.find("input").val(""),a.find("textarea").val(""),"redirect_url"in t){var r=t.redirect_url;window.location.replace(r)}},error:function(t){for(var r=t.errors,e=0;e<r;e++){var n=r[e];show_error_message(a.find('input[name="'+n.field+'"]'),n.message)}}})}})),$("label.dropzone").each((function(){var t=$(this),a=t.find('input[type="file"]');t.on("drop",(function(r){r.preventDefault(),r.stopPropagation(),t.removeClass("dragover");var e=r.originalEvent.dataTransfer.files;a.prop("files",e),t.addClass("dropped")})),t.on("dragover",(function(a){a.preventDefault(),a.stopPropagation(),t.addClass("dragover")})),t.on("dragout",(function(a){a.preventDefault(),a.stopPropagation(),t.removeClass("dragover")}))}))}));