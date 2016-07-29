$(document).ready(function() {

  // Clicking enter on text field
  $("#uname").keypress(function (e) {
   var key = e.which;
   if(key == 13) { // the enter key code
      $("#get_names").click();
      return false;
    }
  });

  $("#get_names").on('click', function() {
    uname = $.trim($("#uname").val())
    if(uname.length > 2) {
      $("#p2").removeClass("hidden");
      $(".suggestions .results").addClass("hidden");
      $(".error").addClass("hidden");
      $.get('/get_names', {uname: uname})
        .done(function(data) {
          $(".suggestions").removeClass('hidden')
          $(".suggestions .results").html('');
          $.each(data, function(key, value_ar) {
            count = 0;
            $(".suggestions .results").append("<h5>" + key + "</h5>");
            $.each(value_ar, function(index, value) {
              count += 1
              $(".suggestions .results").append("<div>" + value['updated_name']
                + " ( Pokemon: <a href=\"" + value['url'] + "\" target='_blank'>"
                + value['pokemon_name'] + "</a> ) </div>");
            });
            if(count == 0) {
              $(".suggestions .results").append("<div>No suggestions</div>");
            }
          });
          $("#p2").addClass("hidden");
          $(".suggestions .results").removeClass("hidden")
        })
    } else {
      $(".error").removeClass("hidden");
      //$(".suggestions .results").addClass("hidden");
    }
  });
});