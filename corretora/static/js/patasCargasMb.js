// $(document).ready(function () {
//   $('[data-toggle="tooltip"]').tooltip();
// });

// $(document).ready(function () {
//   $("#id_data").mask("00/00/0000");
// });

// $(document).ready(function () {
//   $("#id_data_agenda").mask("00/00/0000");
// });

// var contratos = { {% for p in pedidos %}  {{ p.id}}:  { contrato: "{{p.contrato}}" ,fornecedor: "{{ p.fornecedor.nome}}", cidadef: "{{p.fornecedor.cidade}}", cliente: "{{ p.cliente.nome_fantasia}}"}, {% endfor %} }



$("form#updateUser").on("submit", function (event) {
  event.preventDefault();
  var urlform = $("[data-validate-username-url]").attr(
    "data-validate-username-url"
  );
  var idInput = $('input[name="formId"]').val().trim();
  var nameInput = $('input[name="formName"]').is(":checked");

  if (nameInput === true) {
    var valName = "True";
  } else {
    var valName = "False";
  }
  // Create Ajax Call
  $.ajax({
    url: urlform,
    data: {
      id: idInput,
      name: valName,
    },
    dataType: "json",
    success: function (data) {
      if (data.user) {
        updateToUserTabel(data.user);
        console.log(data.user);
        $.notify(`${nplaca} - ${mot} | Status da Ordem atualizado com sucesso!!`, 'success');
      }
    },
  });
  $("form#updateUser").trigger("reset");
  $("#myModal").modal("hide");
  return false;
});

function updateForm() {
  $("form#updateUser").trigger("reset");
}

function updateToUserTabel(user) {
  tr_id = "#CargaId" + user.id;
  ordem = user.name;
  console.log(ordem);
  name = $(tr_id)
    .find("i[ordem-carregamento]")
  if (ordem === true) {
    var aElement = $(tr_id).find("i[ordem-carregamento]");
    aElement.attr("ordem-carregamento", "True"); 
    aElement.addClass('text-success fas fa-check');
    aElement.removeClass('text-danger fa-times');
    
  } else {
    var aElement = $(tr_id).find("i[ordem-carregamento]");
    aElement.attr("ordem-carregamento", "False");
    aElement.addClass('text-danger fas fa-times');
    aElement.removeClass('text-success fa-check');
    
  }
}

// Update Django Ajax Call
function editUser(id) {
  if (id) {
    tr_id = "#CargaId" + id;
    console.log(tr_id);
    name = $(tr_id).find("i[ordem-carregamento]").attr("ordem-carregamento");
    mot = $(tr_id).find("i[updatemotoristaUser]").attr("updatemotoristaUser");
    placa = $(tr_id).find("i[updatePlacaUser]").attr("updatePlacaUser");
    nplaca = placa.slice(0, 3) + " " + placa.slice(3);

    var placaform = document.getElementById("updatePlacaUser");
    placaform.innerHTML = nplaca + " - " + " " + mot;

    $("#form-id").val(id);
    
    if (name === "True") {
      $("#form-name").attr("checked", true);
    } else {
      $("#form-name").attr("checked", false);
    }
  }
}










//UpdateUserChegada
$("form#updateUserChegada").on("submit", function (event) {
  event.preventDefault();
  var urlform = $("[data-validate-username-url-chegada]").attr(
    "data-validate-username-url-chegada"
  );
  console.log(urlform)
  var idInput = $('input[name="formIdChegada"]').val().trim();
  var nameInput = $('input[name="formNameChegada"]').is(":checked");

  if (nameInput === true) {
    var valName = "True";
  } else {
    var valName = "False";
  }
  // Create Ajax Call
  $.ajax({
    url: urlform,
    data: {
      id: idInput,
      name: valName,
    },
    dataType: "json",
    success: function (data) {
      if (data.user) {
        updateToUserTabelChegada(data.user);
        console.log(data.user);
        $.notify(`${nplaca} - ${mot} | Chegada atualizada com sucesso!!`, 'success');
      }
    },
  });
  $("form#updateUserChegada").trigger("reset");
  $("#myModalChegada").modal("hide");
  return false;
});

function updateFormChegada() {
  $("form#updateUserChegada").trigger("reset");
}

function editUserChegada(id) {
  if (id) {
    tr_id = "#user-" + id;
    console.log(tr_id);
    name = $(tr_id).find("td[ordem-chegada]").attr("ordem-chegada");
    mot = $(tr_id).find("td[updatemotoristaUserChegada]").attr("updatemotoristaUserChegada");
    placa = $(tr_id).find("td[updatePlacaUserChegada]").attr("updatePlacaUserChegada");
    nplaca = placa.slice(0, 3) + " " + placa.slice(3);

    var placaform = document.getElementById("updatePlacaUserChegada");
    placaform.innerHTML = nplaca + " - " + " " + mot;

    $("#form-id-chegada").val(id);
    if (name === "True") {
      $("#form-name-chegada").attr("checked", true);
    } else {
      $("#form-name-chegada").attr("checked", false);
    }
  }
}



function updateToUserTabelChegada(user) {
  tr_id = "#user-" + user.id;
  ordem = user.name;
  console.log(ordem);
  name = $(tr_id)
    .find("td[ordem-chegada]")
  if (ordem === true) {
    var aElement = $(tr_id).find("td[ordem-chegada]");
    aElement.attr("ordem-chegada", "True");
    aElement.addClass('text-success');
    aElement.removeClass('text-danger');
    
  } else {
    var aElement = $(tr_id).find("td[ordem-chegada]");
    aElement.attr("ordem-chegada", "False");
    aElement.addClass('text-danger');
    aElement.removeClass('text-success');
  }
}







//UpdateUserBuonny
$("form#updateUserBuonny").on("submit", function (event) {
  event.preventDefault();
  var urlform = $("[data-validate-username-url-Buonny]").attr(
    "data-validate-username-url-Buonny"
  );
  console.log(urlform)
  var idInput = $('input[name="formIdBuonny"]').val().trim();
  var nameInput = $('input[name="formNameBuonny"]').val().trim();

  
  // Create Ajax Call
  $.ajax({
    url: urlform,
    data: {
      id: idInput,
      name: nameInput,
    },
    dataType: "json",
    success: function (data) {
      if (data.user) {
        updateToUserTabelBuonny(data.user);
        console.log(data.user);
        $.notify(`${nplaca} - ${mot} | Buonny atualizada com sucesso!!`, 'success');
      }
    },
  });
  $("form#updateUserBuonny").trigger("reset");
  $("#myModalBuonny").modal("hide");
  return false;
});

function updateFormBuonny() {
  $("form#updateUserBuonny").trigger("reset");
}



function editUserBuonny(id) {
  if (id) {
    tr_id = "#CargaId" + id;
    console.log(tr_id);
    buonny = $(tr_id).find("strong[updateBuonnyUserBuonny]").attr("updateBuonnyUserBuonny");
    mot = $(tr_id).find("strong[updatemotoristaUserBuonny]").attr("updatemotoristaUserBuonny");
    placa = $(tr_id).find("strong[updatePlacaUserBuonny]").attr("updatePlacaUserBuonny");
    nplaca = placa.slice(0, 3) + " " + placa.slice(3);

    var placaform = document.getElementById("updatePlacaUserBuonny");
    placaform.innerHTML = nplaca + " - " + " " + mot;

    $("#form-id-Buonny").val(id);
    $("#form-name-Buonny").val(buonny);
  }
}


function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

function updateToUserTabelBuonny(user) {
  var tr_id = "#CargaId" + user.id;
  var buonny = user.buonny
  var bElement = $(tr_id).find("strong[updateBuonnyUserBuonny]");
  bElement.attr("updateBuonnyUserBuonny", buonny);
  
  if (typeof buonny === 'string') {
    bElement.text(capitalize(buonny));
  } else {
    bElement.text(buonny);
  };

  bElement.removeAttr("class");
  
  if (buonny.includes('dast')) {
    bElement.addClass("text-danger");
  } else if (buonny.includes('sul')) {
    bElement.addClass("text-warning");
  } else if (buonny.includes('nviad')) {
    bElement.addClass("text-info");
  } else {
    bElement.addClass("text-success"); 
  } 
}


