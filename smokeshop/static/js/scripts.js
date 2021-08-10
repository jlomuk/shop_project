// Get the current year for the copyright
$('#year').text(new Date().getFullYear());

// init tooltips
$('[data-toggle="tooltip"]').tooltip();


$('#minus').on('click', function() {
    let currentAmount = $('#id_quantity').val()
    if (+currentAmount > 1) currentAmount--;
    $('#id_quantity').attr('value', String(currentAmount))
})


$('#plus').on('click', function() {
    let currentAmount = $('#id_quantity').val()
    if (+currentAmount < 10) currentAmount++;
    $('#id_quantity').attr('value', String(currentAmount))
})


$('.decrement_cart').on('click', function() {
    let input = $(this).parents('form').find('input.form-control');
    let value = +input.val();
    if (value > 1) value--;
    $(input).attr('value', String(value))
})


$('.increment_cart').on('click', function() {
    let input = $(this).parents('form').find('input.form-control');
    let value = +input.val();
    if (value < 10) value++;
    $(input).attr('value', String(value))
})


function setTotalCost() {
    let totalCost = parseInt(document.getElementById("cart_price").innerHTML);
    totalCost += getSumOfElements('transport');
    totalCost = totalCost.toFixed(2);
    document.getElementById("order-total").innerHTML = `${totalCost} руб`
}


function getSumOfElements(elementName) {
    let sum = 0;
    radios = document.getElementsByName(elementName);
    for (let i = 0; i < radios.length; i++) {
        if(radios[i].checked){
            if(radios[i].getAttribute('amount') !== 'free'){
                sum += parseInt(radios[i].getAttribute('amount'));
            }
        }
    }
    return sum;
}