(function($){
    $(function() {
        $(".datepicker-widget").each(function () {
            var options = {};
            if ($(this).attr('data-date-format') == undefined) {
                options = { format: "dd-mm-yyyy"};
            } 
            $(this).datepicker(options);
        });
    })
})(jQuery)
