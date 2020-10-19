$(document).ready(function () {
    //when a group is shown, save it as the active accordion group
    $("#accordionExample").on('shown.bs.collapse', function () {
        var active = $("#accordionExample .show").attr('id');
        $.cookie('activeAccordionGroup', active);
      //  alert(active);
    });
    $("#accordionExample").on('hidden.bs.collapse', function () {
        $.removeCookie('activeAccordionGroup');
    });
    var last = $.cookie('activeAccordionGroup');
    if (last != null) {
        //remove default collapse settings
        $("#accordionExample .panel-collapse").removeClass('show');
        //show the account_last visible group
        $("#" + last).addClass("show");
    }
});