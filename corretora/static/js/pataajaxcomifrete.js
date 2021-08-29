function loadJson(selector) {
	return JSON.parse(
		document.querySelector(selector).getAttribute("data-json")
	);
}

$("#updateUserClassificacao #form-name-renda").on({
	"keyup": function (event) {
	$(event.target).val(function (index, value ) {
			return value.replace(/\D/g, "")
			.replace(/([0-9])([0-9]{2})$/, '$1,$2')
			
	});
	}
});

$("#form-name-renda").on("change", function (e) {
	var valPorTon = $("#form-name-renda").val()
	var idInput = $('input[name="formIdClassificacao"]').val().trim();
	tr_id = "#user-" + idInput;
	console.log(tr_id)
	pesoCarga = $(tr_id).find("td[data-pesoCarregado]").attr("data-pesoCarregado");
	console.log(parseFloat(pesoCarga)/ 1000)
	console.log(parseFloat(valPorTon))
	var ValorTotal = ((parseFloat(pesoCarga) / 1000) * parseFloat(valPorTon));
	if (ValorTotal) {
		var ValorTotalFormat = ValorTotal.toLocaleString('pt-br', {minimumFractionDigits: 2});
	}
	$("#form-name-inteiro").val(ValorTotalFormat);	


	
})
//   var jsonData = loadJson("#jsonData");

//UpdateUserBuonny
$("form#updateUserClassificacao").on("submit", function (event) {
	event.preventDefault();
	var urlform = $("[data-validate-username-url-Classificacao]").attr(
		"data-validate-username-url-Classificacao"
	);
	console.log(urlform);
	var idInput = $('input[name="formIdClassificacao"]').val().trim();
	var RendaInput = $('input[name="formNameRenda"]').val().trim();
	var InteiroInput = $('input[name="formNameInteiro"]').val().trim();
	

	console.log(
		RendaInput,
		InteiroInput,
	);

	// Create Ajax Call
	$.ajax({
		url: urlform,
		data: {
			id: idInput,
			renda: RendaInput,
			inteiro: InteiroInput,
		},
		dataType: "json",
		success: function (data) {
			if (data) {
				console.log(data)
				updateToUserTabelClassificacao(data);
				// $.notify(`${nplaca} - ${mot} - NF ${formatNumber(nfiscal)} | Classificação atualizada com sucesso!!`, 'success');
			}
		},
	});
	$("form#updateUserClassificacao").trigger("reset");
	$("#myModalClassificacao").modal("hide");
	return false;
});

function updateFormClassificacao() {
	$("form#updateUserClassificacao").trigger("reset");
}


function formatNumber(num) {
	return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1.')
}

function editUserClassificacao(id) {
	if (id) {
		tr_id = "#user-" + id;
		console.log(tr_id);

		fornecedor = $(tr_id)
			.find("td[data-fornecedor-nome]")
			.attr("data-fornecedor-nome");
		cliente = $(tr_id)
			.find("td[data-cliente-nome]")
			.attr("data-cliente-nome");
		nfiscal = $(tr_id).find("td[data-nfiscal]").attr("data-nfiscal");

		mot = $(tr_id)
			.find("td[updatemotoristaUser]")
			.attr("updatemotoristaUser");
		placa = $(tr_id).find("td[updatePlacaUser]").attr("updatePlacaUser");

		console.log(mot);
		console.log(placa);

		var renda = $(tr_id)
			.find("td[data-ajax-renda]")
			.attr("data-ajax-renda");

		var inteiro = $(tr_id)
			.find("td[data-ajax-inteiro]")
			.attr("data-ajax-inteiro");
		

		var clienteColor = $(tr_id).find("td[data-cliente-color]").attr("data-cliente-color");
		console.log(clienteColor);
		console.log(typeof clienteColor);
		console.log('Marcelo PAta')

		nplaca = placa.slice(0, 3) + " " + placa.slice(3);
		var placaform = document.getElementById("updatePlacaUserClassificacao");
		var nfiscalform = document.getElementById("updateNfiscalClassificacao");
		var fornecedorform = document.getElementById(
			"updateFornecedorClassificacao"
		);
		var clienteform = document.getElementById("updateClienteClassificacao");

		placaform.innerHTML = nplaca + " - " + " " + mot;
		
		if (nfiscal !== "None") {
			nfiscalform.innerHTML = "NF " + formatNumber(nfiscal);
		} else {
			nfiscalform.innerHTML = "Sem Nota Fiscal";
		}
		fornecedorform.innerHTML = fornecedor;
		clienteform.innerHTML = cliente;
		clienteform.style.backgroundColor = clienteColor;

		console.log(id);
		$("#form-id-Classificacao").val(id);

		if (renda == "None") {
			$("#form-name-renda").val("");
		} else {
			$("#form-name-renda").val(renda);
		}

		if (inteiro == "None") {
			$("#form-name-inteiro").val("");
		} else {
			$("#form-name-inteiro").val(inteiro);
		}
	}
}

function capitalize(string) {
	return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

function AttrOrNone(x) {
	if (x) {
		return x;
	} else {
		return 0;
	}
}

function updateToUserTabelClassificacao(data) {
	var tr_id = "#user-" + data.id;
	
	

	if (data.comi_frete_total == null) {
		var comiTotal = 0
	} else {
		var comiTotal = parseFloat(data.comi_frete_total).toLocaleString('pt-br', {minimumFractionDigits: 2});
	}

	var comiTon = parseFloat(data.comi_frete_ton).toLocaleString('pt-br', {minimumFractionDigits: 2});
	
	console.log(`Comiton: ${comiTon}`)
	console.log(`Comitotal: ${comiTotal}`)
	console.log(typeof comiTon)
	console.log(typeof comiTotal)
	console.log(comiTotal == 0)
	console.log(comiTotal === 0)
	if (data.comi_frete_ton == "0.00" ) {
		var tablerenda = $(tr_id).find("td[data-ajax-renda]");
		tablerenda.attr("data-ajax-renda", AttrOrNone(comiTon));
		$(tr_id).find("a.valorportonhtml").html(`<i class=" far fa-times-circle text-danger"></i>`);
	} else {
		var tablerenda = $(tr_id).find("td[data-ajax-renda]");
		tablerenda.attr("data-ajax-renda", AttrOrNone(comiTon));
		$(tr_id).find("a.valorportonhtml").html(`R$ ${comiTon}`);
	}

	var tableinteiro = $(tr_id).find("td[data-ajax-inteiro]");
	tableinteiro.attr("data-ajax-inteiro", AttrOrNone(comiTotal));
	
	if (comiTotal == 0 ) {	
		var tableinteiroTotal = $(tr_id).find("td[data-comiFreteCarga]");
		tableinteiroTotal.attr("data-comiFreteCarga", AttrOrNone(data.comi_frete_total));
		tableinteiroTotal.html(`<i class=" far fa-times-circle text-danger"></i>`);
	} else {
		var tableinteiroTotal = $(tr_id).find("td[data-comiFreteCarga]");
		tableinteiroTotal.attr("data-comiFreteCarga", AttrOrNone(data.comi_frete_total));
		tableinteiroTotal.html(`R$ ${comiTotal}`)
		$(tr_id).find("input:checkbox").val(data.comi_frete_total)
	}
	// $(`${tr_id} > td:nth-child(19)`).html(`<div class="custom-control custom-switch"><input type="checkbox" name="chkOrgRow" class="custom-control-input" value="${data.comi_frete_total}" id="switch-${data.id}">  <label class="custom-control-label" for="switch-${data.id}"></label></div>`)
	// $(tr_id).find("a.valortotalcominhtml").html(`R$ ${comiTotal}`);

	

	// if (typeof Classificacao === "string") {
	//   bElement.text(capitalize(Classificacao));
	// } else {
	//   bElement.text(Classificacao);
	// }

	// bElement.removeAttr("class");

	if (
		data.renda &&
		data.inteiro
	) {
		// classFaList.removeClass("text-warning");
		// classFaList.removeClass("text-danger");
		// classFaList.addClass("text-success");
	} else if (
		data.renda ||
		data.inteiro 
	) {
		// classFaList.removeClass("text-danger");
		// classFaList.removeClass("text-success");
		// classFaList.addClass("text-warning");
	} else {
		// classFaList.removeClass("text-success");
		// classFaList.removeClass("text-warning");
		// classFaList.addClass("text-danger");
	}
}
