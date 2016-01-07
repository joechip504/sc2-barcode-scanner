function exampleReplay() {
    $.ajax({url: "/results/22", success: function(result){
      $(result).hide().prependTo("#results").slideDown(1000);
    }});
}
