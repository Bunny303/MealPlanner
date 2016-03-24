function addIngredientField(recipeIngredientId)
{
    var container = document.getElementById("container");
    var innerContainer = document.createElement("div");
    container.appendChild(innerContainer);

    var ingredient_name = document.getElementById("ingredient_name").value;
    var ingredient_unit = document.getElementById("ingredient_unit").value;
    var ingredient_quantity = document.getElementById("ingredient_quantity").value;

    var input = document.createElement("input");
    input.type = "text";
    input.name = "ingredient_quantity";
    input.readOnly=true;
    input.value = ingredient_quantity;
    innerContainer.appendChild(input);

    input = document.createElement("input");
    input.type = "text";
    input.name = "ingredient_unit";
    input.readOnly=true;
    input.value = ingredient_unit;
    innerContainer.appendChild(input);

    input = document.createElement("input");
    input.type = "text";
    input.name = "ingredient_name";
    input.readOnly=true;
    input.value = ingredient_name;
    innerContainer.appendChild(input);

    var ingredient_name = document.getElementById("ingredient_name").value = "";
    var ingredient_unit = document.getElementById("ingredient_unit").value = "kg";
    var ingredient_quantity = document.getElementById("ingredient_quantity").value = "";

    var button = document.createElement("button");
    button.onclick = function(){
        deleteRecipeIngredient(recipeIngredientId);
    };
    button.innerText = 'Remove';
    button.type = 'button';
    innerContainer.appendChild(button);
}

function set_portion_number(portionNumber)
{
    if(portion_number!=1)
    {
        var selectEl = document.getElementById("portion_number");
        selectEl.options[portionNumber-1].selected = true;
    }
}

function createRecipeIngredient(recipe_id)
{
    var ingredient_name = document.getElementById("ingredient_name").value;
    var ingredient_unit = document.getElementById("ingredient_unit").value;
    var ingredient_quantity = document.getElementById("ingredient_quantity").value;
    var data = {
        ingredient_name: ingredient_name,
        ingredient_unit: ingredient_unit,
        ingredient_quantity: ingredient_quantity,
        recipe_id: recipe_id
    };

    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": "/add-ingredient/",
        "data": data,
        "success": function(data){
            addIngredientField(data.id);
        },
    });
}

function removeIngredientField(parentContainer)
{
    while (parentContainer.firstChild)
    {
        parentContainer.removeChild(parentContainer.firstChild);
    }
    parentContainer.remove();
}

function deleteRecipeIngredient(recipe_ingredient_id)
{
    var data = {
        recipe_ingredient_id: recipe_ingredient_id
    };
    var element = event.target;
    var parent = element.parentNode;

    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": "/delete-ingredient/",
        "data": data,
        "success": function(results){
            //todo: check if success == true
            removeIngredientField(parent);
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}

function removeMealField(recipe_id)
{
    $("#"+recipe_id).remove();
}

function removeMeal(recipe_id, day_name)
{
    var data = {
        recipe_id: recipe_id,
        day_name: day_name
    };

    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": "/remove-meal/",
        "data": data,
        "success": function(results){
            //todo: check if success == true
            removeMealField(recipe_id);
        },
        failure: function(errMsg) {
            console.log(errMsg);
        }
    });
}

$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});


