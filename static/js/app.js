$(document).ready(function() {
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
          count = 0;
          $.each(data, function(index, value) {
            count += 1
            $(".suggestions .results").append("<div>" + capitalizeFirstLetter(value['updated_name'])
              + " ( Pokemon: " + capitalizeFirstLetter(value['pokemon_name']) + " ) </div>");
          })
          if(count == 0) {
            $(".suggestions .results").append("<div>No suggestions</div>");
          }
          $("#p2").addClass("hidden");
          $(".suggestions .results").removeClass("hidden")
        })
    } else {
      $(".error").removeClass("hidden");
    }
  });
});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}