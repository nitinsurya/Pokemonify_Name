$(document).ready(function() {

  $("#get_names").on('click', function() {
    uname = $.trim($("#uname").val())
    if(uname.length > 3) {
      $.get('/get_names', {uname: uname})
        .done(function(data) {
          $(".suggestions").removeClass('hidden')
          $(".suggestions .results").html('');
          count = 0;
          $.each(data, function(index, value) {
            count += 1
            $(".suggestions .results").append("<div>" + capitalizeFirstLetter(value['updated_name'])
              + " ( " + capitalizeFirstLetter(value['pokemon_name']) + " ) </div>");
          })
          if(count == 0) {
            $(".suggestions .results").append("<div>No suggestions</div>");
          }
        })
    }
  });
});

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}