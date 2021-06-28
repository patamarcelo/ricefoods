function loadJson(selector) {
	return JSON.parse(
		document.querySelector(selector).getAttribute("data-json")
	);
}

$("#updateUserClassificacao input").on({
	"keyup": function (event) {
	$(event.target).val(function (index, value ) {
			return value.replace(/\D/g, "")
			.replace(/([0-9])([0-9]{2})$/, '$1,$2')
			.replace(/\B(?=(\d{2})+(?!\d)\.?)/g, ",");		
	});
	}
});


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
	var ImpurezaInput = $('input[name="formNameImpureza"]').val().trim();
	var UmidadeInput = $('input[name="formNameUmidade"]').val().trim();
	var GessadoInput = $('input[name="formNameGessado"]').val().trim();
	var BbrancaInput = $('input[name="formNameBbranca"]').val().trim();
	var AmareloInput = $('input[name="formNameAmarelo"]').val().trim();
	var ManchpicInput = $('input[name="formNameManchpic"]').val().trim();
	var VermelhosInput = $('input[name="formNameVermelhos"]').val().trim();
	var ObsInput = $('textarea[name="formNameObs"]').val().trim();

	console.log(
		RendaInput,
		InteiroInput,
		ImpurezaInput,
		UmidadeInput,
		GessadoInput,
		BbrancaInput,
		AmareloInput,
		ManchpicInput,
		VermelhosInput,
		ObsInput
	);

	// Create Ajax Call
	$.ajax({
		url: urlform,
		data: {
			id: idInput,
			renda: RendaInput,
			inteiro: InteiroInput,
			impureza: ImpurezaInput,
			umidade: UmidadeInput,
			gessado: GessadoInput,
			bbranca: BbrancaInput,
			amarelo: AmareloInput,
			manchpic: ManchpicInput,
			vermelhos: VermelhosInput,
			obs: ObsInput,
		},
		dataType: "json",
		success: function (data) {
			if (data) {
				updateToUserTabelClassificacao(data);
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
		var impureza = $(tr_id)
			.find("td[data-ajax-impureza]")
			.attr("data-ajax-impureza");
		var umidade = $(tr_id)
			.find("td[data-ajax-umidade]")
			.attr("data-ajax-umidade");
		var gessado = $(tr_id)
			.find("td[data-ajax-gessado]")
			.attr("data-ajax-gessado");
		var bbranca = $(tr_id)
			.find("td[data-ajax-bbranca]")
			.attr("data-ajax-bbranca");
		var amarelo = $(tr_id)
			.find("td[data-ajax-amarelo]")
			.attr("data-ajax-amarelo");
		var manchpic = $(tr_id)
			.find("td[data-ajax-manchpic]")
			.attr("data-ajax-manchpic");
		var vermelhos = $(tr_id)
			.find("td[data-ajax-vermelhos]")
			.attr("data-ajax-vermelhos");
		var obs = $(tr_id).find("td[data-ajax-obs]").attr("data-ajax-obs");

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
		console.log(impureza);
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

		if (impureza == "None") {
			$("#form-name-impureza").val("");
		} else {
			$("#form-name-impureza").val(impureza);
		}

		if (umidade == "None") {
			$("#form-name-umidade").val("");
		} else {
			$("#form-name-umidade").val(umidade);
		}

		if (gessado == "None") {
			$("#form-name-gessado").val("");
		} else {
			$("#form-name-gessado").val(gessado);
		}

		if (bbranca == "None") {
			$("#form-name-bbranca").val("");
		} else {
			$("#form-name-bbranca").val(bbranca);
		}

		if (amarelo == "None") {
			$("#form-name-amarelo").val("");
		} else {
			$("#form-name-amarelo").val(amarelo);
		}

		if (manchpic == "None") {
			$("#form-name-manchpic").val("");
		} else {
			$("#form-name-manchpic").val(manchpic);
		}

		if (vermelhos == "None") {
			$("#form-name-vermelhos").val("");
		} else {
			$("#form-name-vermelhos").val(vermelhos);
		}

		if (obs == "None") {
			$("#form-name-obs").val("");
		} else {
			$("#form-name-obs").val(obs);
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
		return "None";
	}
}

function updateToUserTabelClassificacao(data) {
	var tr_id = "#user-" + data.id;
	var classFaList = $(tr_id).find("td .fa-list-alt");

	var tablerenda = $(tr_id).find("td[data-ajax-renda]");
	tablerenda.attr("data-ajax-renda", AttrOrNone(data.renda));

	var tableinteiro = $(tr_id).find("td[data-ajax-inteiro]");
	tableinteiro.attr("data-ajax-inteiro", AttrOrNone(data.inteiro));

	var tableimpureza = $(tr_id).find("td[data-ajax-impureza]");
	tableimpureza.attr("data-ajax-impureza", AttrOrNone(data.impureza));

	var tableumidade = $(tr_id).find("td[data-ajax-umidade]");
	tableumidade.attr("data-ajax-umidade", AttrOrNone(data.umidade));

	var tablegessado = $(tr_id).find("td[data-ajax-gessado]");
	tablegessado.attr("data-ajax-gessado", AttrOrNone(data.gessado));

	var tablebbranca = $(tr_id).find("td[data-ajax-bbranca]");
	tablebbranca.attr("data-ajax-bbranca", AttrOrNone(data.bbranca));

	var tableamarelo = $(tr_id).find("td[data-ajax-amarelo]");
	tableamarelo.attr("data-ajax-amarelo", AttrOrNone(data.amarelo));

	var tablemanchpic = $(tr_id).find("td[data-ajax-manchpic]");
	tablemanchpic.attr("data-ajax-manchpic", AttrOrNone(data.manchpic));

	var tablevermelhos = $(tr_id).find("td[data-ajax-vermelhos]");
	tablevermelhos.attr("data-ajax-vermelhos", AttrOrNone(data.vermelhos));

	var tableobs = $(tr_id).find("td[data-ajax-obs]");
	tableobs.attr("data-ajax-obs", AttrOrNone(data.obs));

	// if (typeof Classificacao === "string") {
	//   bElement.text(capitalize(Classificacao));
	// } else {
	//   bElement.text(Classificacao);
	// }

	// bElement.removeAttr("class");

	if (
		data.renda &&
		data.inteiro &&
		data.impureza &&
		data.umidade &&
		data.gessado &&
		data.bbranca &&
		data.amarelo &&
		data.manchpic &&
		data.vermelhos
	) {
		classFaList.removeClass("text-warning");
		classFaList.removeClass("text-danger");
		classFaList.addClass("text-success");
	} else if (
		data.renda ||
		data.inteiro ||
		data.impureza ||
		data.umidade ||
		data.gessado ||
		data.bbranca ||
		data.amarelo ||
		data.manchpic ||
		data.vermelhos
	) {
		classFaList.removeClass("text-danger");
		classFaList.removeClass("text-success");
		classFaList.addClass("text-warning");
	} else {
		classFaList.removeClass("text-success");
		classFaList.removeClass("text-warning");
		classFaList.addClass("text-danger");
	}
}
