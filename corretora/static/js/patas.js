$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(document).ready(function () {
  $("#id_data").mask("00/00/0000");
});

$(document).ready(function () {
  $("#id_data_agenda").mask("00/00/0000");
});

// var contratos = { {% for p in pedidos %}  {{ p.id}}:  { contrato: "{{p.contrato}}" ,fornecedor: "{{ p.fornecedor.nome}}", cidadef: "{{p.fornecedor.cidade}}", cliente: "{{ p.cliente.nome_fantasia}}"}, {% endfor %} }

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute("data-json"));
}

window.onload = function () {
  $("#id_pedido").on("change", function () {
    var idcontrato = $(this).val();
    var idcontrato = parseInt(idcontrato);
    var jsonData = loadJson("#jsonData");
    var contratos = jsonData;
    console.log(idcontrato);

    contratos.forEach((element, index, array) => {
      if (element.id === idcontrato) {
        var pedido = element.contrato;
        var fornecedor = element.fornecedor;
        var cidade = element.cidadef;
        var cliente = element.cliente;
        console.log(pedido);
        console.log(fornecedor);
        console.log(cidade);
        console.log(cliente);
        console.log(" ");
        if (pedido === "900") {
          var elementfornecedor = document.getElementById("fornecedorinfo");
          elementfornecedor.innerHTML = "Escritório";
          var elementcidade = document.getElementById("cidadeinfo");
          elementcidade.innerHTML = cidade;
          var elementcliente = document.getElementById("clienteinfo");
          elementcliente.innerHTML = cliente;
          var elementcliente = document.getElementById("pedido_from_model");
          elementcliente.innerHTML = pedido;
        } else if (pedido === "901") {
          var elementfornecedor = document.getElementById("fornecedorinfo");
          elementfornecedor.innerHTML = "Escritório";
          var elementcidade = document.getElementById("cidadeinfo");
          elementcidade.innerHTML = cidade;
          var elementcliente = document.getElementById("clienteinfo");
          elementcliente.innerHTML = cliente;
          var elementcliente = document.getElementById("pedido_from_model");
          elementcliente.innerHTML = pedido;
        } else {
          var elementcidade = document.getElementById("cidadeinfo");
          elementcidade.innerHTML = cidade;
          var elementcliente = document.getElementById("fornecedorinfo");
          elementcliente.innerHTML = fornecedor;
          var elementcliente = document.getElementById("clienteinfo");
          elementcliente.innerHTML = cliente;
          var elementcliente = document.getElementById("pedido_from_model");
          elementcliente.innerHTML = pedido;
        }
      } else if (isNaN(idcontrato)) {
        var elementcidade = document.getElementById("cidadeinfo");
        elementcidade.innerHTML = "";
        var elementcliente = document.getElementById("fornecedorinfo");
        elementcliente.innerHTML = "";
        var elementcliente = document.getElementById("clienteinfo");
        elementcliente.innerHTML = "";
        var elementcliente = document.getElementById("pedido_from_model");
        elementcliente.innerHTML = "";
      }
    });
  });
};

// _____________________----------------------------------------------------------------

$(document).ready(function () {
  var data_carre = document.getElementById("id_data");
  var data_agenda = document.getElementById("id_data_agenda");
  var id_pedido = document.getElementById("id_pedido");

  Date.prototype.addDays = function (days) {
    var date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
  };

  function AddNewDays(data, days) {
    var dataString = data.split("/");
    var newdata = new Date(dataString[2], dataString[1] - 1, dataString[0]);
    novadata = newdata.addDays(days);
    novadata.toLocaleDateString();
    novadata = moment(novadata).format("DD/MM/YYYY");
    return novadata;
  }

  function getWeekDay(data) {
    var dataString = data.split("/");
    var newdata = new Date(dataString[2], dataString[1] - 1, dataString[0]);
    diadasemana = newdata.getDay();
    return diadasemana;
  }

  function totalAgendadosAgora(array, datadescarga) {
    if ((totalagendados = array[datadescarga])) {
      return totalagendados;
    } else {
      totalagendados = 0;
    }
    return totalagendados;
  }

  $("#id_data").on("change", function () {
    var jsonSemDescarga = loadJson("#jsonDataSemDescarga");
    
    
    var jsonData = loadJson("#jsonDataAgenda");
    console.log(jsonData);
    var clienteinfonome = document.getElementById("clienteinfo").innerHTML;

    var jsonCargas = loadJson("#jsonCargas");
    function agruparPor(objetoArray, propriedade) {
      return objetoArray.reduce(function (acc, obj) {
        let key = obj[propriedade];
        if (!acc[key]) {
          acc[key] = [];
        }
        acc[key].push(obj);
        return acc;
      }, {});
    }
    var grupodePessoas = agruparPor(jsonCargas, "cliente");
    var clientesName = Object.entries(grupodePessoas);
    var resultadoAgendamentoJS = {};
    for (var key in clientesName) {
      var obj = clientesName[key];
      datasAgendados = obj[1];
      const resultado = {};
      count = 1;
      datasAgendados.forEach((item) => {
        if (resultado.hasOwnProperty(item.data_agenda)) {
          count += 1;
          resultado[item.data_agenda] = count;
        } else {
          resultado[item.data_agenda] = 1;
        }
      });
      resultadoAgendamentoJS[obj[0]] = resultado;
    }

    jsonData.forEach((e, i, array) => {
      if (clienteinfonome === e.nome) {
        var nome = e.nome;
        var dias_descarga = e.dias_descarga;
        var veiculos_dia = e.veiculos_dia;
        // var prev_dias_peso = e.prev_dias[0];
        var descarga_sabado = e.descarga_sabado;
        // var prev_dias_quant_agendado = e.prev_dias[1];
        var clientesDatas = {};
        for (var key of Object.keys(resultadoAgendamentoJS)) {
          if (key === clienteinfonome) {
            console.log(key);
            newobj = resultadoAgendamentoJS[key];
            let entries = Object.entries(newobj);
            for (var [prop, val] of entries) {
              prop = moment(prop, "YYYY-MM-DD").format("DD/MM/YYYY");
              console.log(prop, val);
              clientesDatas[prop] = val;
            }
          }
        }
        let clientesDataSemDescarga = [];
        for (var key in jsonSemDescarga) {
          // skip loop if the property is from prototype
          if (!jsonSemDescarga.hasOwnProperty(key)) continue;
      
          var obj = jsonSemDescarga[key];
          for (var prop in obj) {
              // skip loop if the property is from prototype
              if (!obj.hasOwnProperty(prop)) continue;
              dataSem = moment(obj[prop], "YYYY-MM-DD").format("DD/MM/YYYY");
              clienteSem = prop
              if (clienteinfonome === clienteSem) {
                
                clientesDataSemDescarga.push(dataSem)
              }
          }
        }

        console.log(clientesDataSemDescarga)

        var prev_dias_quant_agendado = clientesDatas;
        console.log(clientesDatas);
        console.log(`Clientes e  separados!!`);
        console.log(array);
        console.log(nome);
        console.log(dias_descarga);
        console.log(veiculos_dia);
        console.log(prev_dias_quant_agendado);
        console.log(typeof prev_dias_quant_agendado);
        console.log(descarga_sabado);

        dataDescarga = AddNewDays(data_carre.value, e.dias_descarga);
        console.log(`Data Descarga: ${dataDescarga}`);

        diasemanadescarga = getWeekDay(dataDescarga);
        console.log(`Dia da Semana da descarga: ${diasemanadescarga}`);

        totalmotagenda = totalAgendadosAgora(
          prev_dias_quant_agendado,
          dataDescarga
        );
        console.log(`Total Agendado até o momento: ${totalmotagenda}`);
        console.log(clientesDataSemDescarga.includes(dataDescarga))
        console.log(clientesDataSemDescarga)
        console.log(dataDescarga)

        while (
          totalmotagenda >= veiculos_dia ||
          (descarga_sabado == false && diasemanadescarga == 6) ||
          diasemanadescarga == 0
          || clientesDataSemDescarga.includes(dataDescarga)
        ) {
          dataDescarga = AddNewDays(dataDescarga, 1);
          diasemanadescarga = getWeekDay(dataDescarga);
          totalmotagenda = totalAgendadosAgora(
            prev_dias_quant_agendado,
            dataDescarga
          );
        }
        console.log(`After loop While: ${dataDescarga}`);
        data_agenda.value = dataDescarga;
      }
    });
  });
  $("#id_situacao").on("change", function () {
    var jsonSemDescarga = loadJson("#jsonDataSemDescarga");

    var jsonData = loadJson("#jsonDataAgenda");
    console.log(jsonData);
    var clienteinfonome = document.getElementById("clienteinfo").innerHTML;

    var jsonCargas = loadJson("#jsonCargasCarregado");
    function agruparPor(objetoArray, propriedade) {
      return objetoArray.reduce(function (acc, obj) {
        let key = obj[propriedade];
        if (!acc[key]) {
          acc[key] = [];
        }
        acc[key].push(obj);
        return acc;
      }, {});
    }
    var grupodePessoas = agruparPor(jsonCargas, "cliente");
    var clientesName = Object.entries(grupodePessoas);
    var resultadoAgendamentoJS = {};
    for (var key in clientesName) {
      var obj = clientesName[key];
      datasAgendados = obj[1];
      const resultado = {};
      count = 1;
      datasAgendados.forEach((item) => {
        if (resultado.hasOwnProperty(item.data_agenda)) {
          count += 1;
          resultado[item.data_agenda] = count;
        } else {
          resultado[item.data_agenda] = 1;
        }
      });
      resultadoAgendamentoJS[obj[0]] = resultado;
    }

    jsonData.forEach((e, i, array) => {
      if (clienteinfonome === e.nome) {
        var nome = e.nome;
        var dias_descarga = e.dias_descarga;
        var veiculos_dia = e.veiculos_dia;
        // var prev_dias_peso = e.prev_dias[0];
        var descarga_sabado = e.descarga_sabado;
        // var prev_dias_quant_agendado = e.prev_dias[1];
        var clientesDatas = {};
        for (var key of Object.keys(resultadoAgendamentoJS)) {
          if (key === clienteinfonome) {
            console.log(key);
            newobj = resultadoAgendamentoJS[key];
            let entries = Object.entries(newobj);
            for (var [prop, val] of entries) {
              prop = moment(prop, "YYYY-MM-DD").format("DD/MM/YYYY");
              console.log(prop, val);
              clientesDatas[prop] = val;
            }
          }
        }

        let clientesDataSemDescarga = [];
        for (var key in jsonSemDescarga) {
          // skip loop if the property is from prototype
          if (!jsonSemDescarga.hasOwnProperty(key)) continue;
      
          var obj = jsonSemDescarga[key];
          for (var prop in obj) {
              // skip loop if the property is from prototype
              if (!obj.hasOwnProperty(prop)) continue;
              dataSem = moment(obj[prop], "YYYY-MM-DD").format("DD/MM/YYYY");
              clienteSem = prop
              if (clienteinfonome === clienteSem) {
                
                clientesDataSemDescarga.push(dataSem)
              }
          }
        }

        var prev_dias_quant_agendado = clientesDatas;
        console.log(clientesDatas);
        console.log(`Clientes e  separados!!`);
        console.log(array);
        console.log(nome);
        console.log(dias_descarga);
        console.log(veiculos_dia);
        console.log(prev_dias_quant_agendado);
        console.log(typeof prev_dias_quant_agendado);
        console.log(descarga_sabado);

        dataDescarga = AddNewDays(data_carre.value, e.dias_descarga);
        console.log(`Data Descarga: ${dataDescarga}`);

        diasemanadescarga = getWeekDay(dataDescarga);
        console.log(`Dia da Semana da descarga: ${diasemanadescarga}`);

        totalmotagenda = totalAgendadosAgora(
          prev_dias_quant_agendado,
          dataDescarga
        );
        console.log(`Total Agendado até o momento: ${totalmotagenda}`);
        console.log(clientesDataSemDescarga.includes(dataDescarga))
        console.log(clientesDataSemDescarga)
        console.log(dataDescarga)

        while (
          totalmotagenda >= veiculos_dia ||
          (descarga_sabado == false && diasemanadescarga == 6) ||
          diasemanadescarga == 0
          || clientesDataSemDescarga.includes(dataDescarga)
        ) {
          dataDescarga = AddNewDays(dataDescarga, 1);
          diasemanadescarga = getWeekDay(dataDescarga);
          totalmotagenda = totalAgendadosAgora(
            prev_dias_quant_agendado,
            dataDescarga
          );
        }
        console.log(`After loop While: ${dataDescarga}`);
        data_agenda.value = dataDescarga;
      }
    });
  });
});

function formatDate(date) {
  nd = moment(date, "YYY-MM-DD").format("DD/MM/YYYY");
  return nd;
}

// $(document).ready(function () {
//   var jsonDataDias = loadJson("#jsonDataDiasSemana");
//   var jsonCargas = loadJson("#jsonCargas");
//   function agruparPor(objetoArray, propriedade) {
//     return objetoArray.reduce(function (acc, obj) {
//       let key = obj[propriedade];
//       if (!acc[key]) {
//         acc[key] = [];
//       }
//       acc[key].push(obj);
//       return acc;
//     }, {});
//   }
//   var grupodePessoas = agruparPor(jsonCargas, "cliente");
//   var clientesName = Object.entries(grupodePessoas);
//   var resultadoAgendamentoJS = {};
//   for (var key in clientesName) {
//     var obj = clientesName[key];
//     datasAgendados = obj[1];
//     const resultado = {};
//     count = 1;
//     datasAgendados.forEach((item) => {
//       if (resultado.hasOwnProperty(item.data_agenda)) {
//         count += 1;
//         resultado[item.data_agenda] = count;
//       } else {
//         resultado[item.data_agenda] = 1;
//       }
//     });
//     resultadoAgendamentoJS[obj[0]] = resultado;
//   }

//   var clientesDatas = {};
//   for (var key of Object.keys(resultadoAgendamentoJS)) {
//     if (key === "Ruston - SP") {
//       console.log(key);
//       console.log(typeof key);
//       newobj = resultadoAgendamentoJS[key];
//       let entries = Object.entries(newobj);
//       for (var [prop, val] of entries) {
//         prop = moment(prop, "YYYY-MM-DD").format("DD/MM/YYYY");
//         console.log(prop, val);
//         clientesDatas[prop] = val;
//       }
//     }
//   }
//   console.log(clientesDatas);
// });

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
  tr_id = "#user-" + user.id;
  ordem = user.name;
  console.log(ordem);
  name = $(tr_id)
    .find("td[ordem-carregamento]")
    .toggleClass("text-success")
    .toggleClass("text-danger");
  if (ordem === true) {
    var aElement = $(tr_id).find("td[ordem-carregamento]");
    aElement.text("Enviada");
    aElement.attr("ordem-carregamento", "True");
  } else {
    var aElement = $(tr_id).find("td[ordem-carregamento]");
    aElement.text("Não Env.");
    aElement.attr("ordem-carregamento", "False");
  }
}

// Update Django Ajax Call
function editUser(id) {
  if (id) {
    tr_id = "#user-" + id;
    console.log(tr_id);
    name = $(tr_id).find("td[ordem-carregamento]").attr("ordem-carregamento");
    mot = $(tr_id).find("td[updatemotoristaUser]").attr("updatemotoristaUser");
    placa = $(tr_id).find("td[updatePlacaUser]").attr("updatePlacaUser");
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
    .toggleClass("text-success")
    .toggleClass("text-warning");
  if (ordem === true) {
    var aElement = $(tr_id).find("td[ordem-chegada]");
    aElement.attr("ordem-chegada", "True");
  } else {
    var aElement = $(tr_id).find("td[ordem-chegada]");
    aElement.attr("ordem-chegada", "False");
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
    
    tr_id = "#user-" + id;
    console.log(tr_id);
    buonny = $(tr_id).find("td[updateBuonnyUserBuonny]").attr("updateBuonnyUserBuonny");
    mot = $(tr_id).find("td[updatemotoristaUserBuonny]").attr("updatemotoristaUserBuonny");
    placa = $(tr_id).find("td[updatePlacaUserBuonny]").attr("updatePlacaUserBuonny");
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
  var tr_id = "#user-" + user.id;
  var buonny = user.buonny
  var bElement = $(tr_id).find("td[updateBuonnyUserBuonny]");
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


