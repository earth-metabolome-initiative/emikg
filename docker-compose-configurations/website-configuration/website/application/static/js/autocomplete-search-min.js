function create_search_result(e,t){var a=$("<li></li>"),r=$("<a></a>"),n=$("<h4></h4>"),c=$("<span></span>");return r.attr("href",t.url),r.text(t.name),n.append(r),c.text(t.description),a.append(n),a.append(c),a}function autocomplete_search(){$("ul.autocomplete-search").each((function(){var e=$(this);e.hide();var t=e.attr("for"),a=e.attr("action"),r="/autocomplete-"+a+"/",n=e.attr("method"),c=$('input[name="'+t+'"]'),o=null;c.keyup((function(){o&&clearTimeout(o),o=setTimeout((function(){var t=c.val();if(t.length<=2)return e.empty(),void e.hide(300);var o=$("<span></span>");o.addClass("loader"),$.ajax({url:r,method:n,data:{search:t},success:function(t){e.empty();for(var r=0;r<t.matching_results.length;r++){var n=create_search_result(a,t.matching_results[r]);e.append(n)}t.matching_results.length>0?e.show(300):e.hide(300)},complete:function(){o.remove()}})}),50)}))}))}$(document).ready(autocomplete_search);