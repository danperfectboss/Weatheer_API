alertify.set('notifier','position', 'bottom-left');

function validateKey(event){
    key = (document.all) ? event.keyCode : event.which;
    key_text = String.fromCharCode(key)
    regexPatern = /^[A-z áéíóúÁÉÍÓÚäëïöüÄËÏÖÜ]+$/

    return regexPatern.test(key_text)
}


function validateEmpty(){
    var city = $('#city').val()
    var country = $('#country').val()

    if (city != '' && country != ''){
        checkRadioButton()
        
        return true
    }else{
        alertify.error('Fields City and Country must not be empty');
        return false
    }
}

function checkRadioButton(){

    if($('#Json').is(':checked')){
        $('#formID').attr('action', '/weather');
    }else if($('#Pretty').is(':checked')){
        $('#formID').attr('action', '/pretty_weather');
    }

}