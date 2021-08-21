function ocultarmostrar(el, el2) {
    if (document.getElementById("comissoes").classList.contains('hide')) {
        document.getElementById(el).classList.remove('hide');
        document.getElementById(el2).className = "fas fa-eye text-info";
    }
    else {
        document.getElementById(el).classList.add('hide');
        document.getElementById(el2).className = "fas fa-eye-slash text-danger";
    }
}



setTimeout(function () {
    document.getElementById("contratos").classList.remove("hide");
    document.getElementById("comissoes").classList.remove("hide");
    document.getElementById("carregamentos").classList.remove("hide");
}, 100);

setTimeout(function () {
    document.getElementById("comissoes").classList.add("hide");
    document.getElementById("ocultm").className = "fas fa-eye-slash text-danger";
}, 2000);
