$(document).ready(function() {
    $("#id_peso").on("change", function () {
        id_peso_var = document.getElementById("id_peso").value
        if (id_peso_var) {
            console.log("ok")
        } else {
            document.getElementById("id_peso").value = 0    
            console.log("zero colocado")
        }
    });
});

window.onload = function () {
    id_peso_var = document.getElementById("id_peso").value;
    id_peso_var_str = id_peso_var.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    document.getElementById('id_peso').type = 'text';
    document.getElementById("id_peso").value = id_peso_var_str

    id_valornf_var = document.getElementById("id_valornf").value;
    id_valornf_var_str = id_valornf_var.toString().replace(/.([^.]*)$/, ",$1");
    id_valornf_var_str_final = id_valornf_var_str.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    console.log(id_valornf_var_str_final)
    // id_valornf_var_str = id_valornf_var.toString().replace(/([0-9])([0-9]{2})$/, '$1,$2')
    
    document.getElementById('id_valornf').type = 'text';
    document.getElementById("id_valornf").value = id_valornf_var_str_final
    
    
    $('#cargaeditform').on('submit', function() {
        str = document.getElementById("id_peso").value;
        document.getElementById("id_peso").value = (str.replace(/\./g,""));  
        
        strvalornf = document.getElementById("id_valornf").value;
        document.getElementById("id_valornf").value = (strvalornf.replace(/\./g,""));  
        strvalornffinal = document.getElementById("id_valornf").value;
        document.getElementById("id_valornf").value = (strvalornffinal.replace(/\,/g,"."));  
    });

    
    $("#id_peso").on({
            "keyup": function (event) {
            $(event.target).val(function (index, value ) {
                if (value.length > 1) {
                    return value.replace(/\D/g, "")
                    // .replace(/([0-9])([0-9]{2})$/, '$1,$2')
                    .replace(/^0+/, '')
                    .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
                } else {
                    return value.replace(/\D/g, "")
                    // .replace(/([0-9])([0-9]{2})$/, '$1,$2')
                    .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
                }
            });
        },
        
        "focus": function() { 
            $(this).select(); 
            console.log(this)
        }
    });

    
    
    $("#id_valornf").on({
            "keyup": function (event) {
            $(event.target).val(function (index, value ) {
                if (value.length > 1) {
                    return value.replace(/\D/g, "")
                    .replace(/([0-9])([0-9]{2})$/, '$1,$2')
                    .replace(/^0+/, '')
                    .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
                } else {
                    return value.replace(/\D/g, "")
                    .replace(/([0-9])([0-9]{2})$/, '$1,$2')
                    .replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
                }
            });
        },
        
        "focus": function() { 
            $(this).select(); 
            console.log(this)
        }
    });

}