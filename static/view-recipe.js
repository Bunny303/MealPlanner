(function ()
{
    var previousValue;
    $("#portion_number").focus(function ()
    {
        previousValue = this.value;
    }).change(function()
    {
        var newValue = this.value;
        //get all ingredient quantities and calculate the new ones
        $(".ing-quantity").each(function()
        {
            var oldQuantity = parseFloat($(this).text());
            $(this).text(oldQuantity*newValue/previousValue);

        });
        //remove focus
        $(this).blur()
    });
})();
