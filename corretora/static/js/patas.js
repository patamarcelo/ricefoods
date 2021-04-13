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
    var jsonData = loadJson("#jsonDataAgenda");
    var clienteinfonome = document.getElementById("clienteinfo").innerHTML;

    jsonData.forEach((e, i, array) => {
      if (clienteinfonome === e.nome) {
        var nome = e.nome;
        var dias_descarga = e.dias_descarga;
        var veiculos_dia = e.veiculos_dia;
        var prev_dias_peso = e.prev_dias[0];
        var descarga_sabado = e.descarga_sabado;
        var prev_dias_quant_agendado = e.prev_dias[1];
        console.log(`Clientes e  separados!!`);
        console.log(array);
        console.log(nome);
        console.log(dias_descarga);
        console.log(veiculos_dia);
        console.log(prev_dias_quant_agendado);
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

        while (
          totalmotagenda >= veiculos_dia ||
          (descarga_sabado == false && diasemanadescarga == 6) ||
          diasemanadescarga == 0
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
