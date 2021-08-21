function loadJson(selector) {
	return JSON.parse(
		document.querySelector(selector).getAttribute("data-json")
	);
}

$(document).ready(function () {
	$("#id_inteiro").mask("00.00", { reverse: true });
	$("#id_renda").mask("00.00", { reverse: true });
	$("#id_impureza").mask("00.00", { reverse: true });
	$("#id_umidade").mask("00.00", { reverse: true });
	$("#id_gessado").mask("00.00", { reverse: true });
	$("#id_bbranca").mask("00.00", { reverse: true });
	$("#id_amarelo").mask("00.00", { reverse: true });
	$("#id_manchpic").mask("00.00", { reverse: true });
	$("#id_vermelhos").mask("00.00", { reverse: true });
	$("#id_valor_mot").mask("000.00", { reverse: true });
});

$(document).ready(function () {
	var idNotaFiscal = $("#id_notafiscal");
	idNotaFiscal.attr("maxlength", "10");
	var idNotaFiscalStr = document
		.getElementById("id_notafiscal")
		.value.toString()
		.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
	console.log(idNotaFiscalStr);
	document.getElementById("id_notafiscal").value = idNotaFiscalStr;
});

$(document).ready(function () {
	var idNotaFiscal = $("#id_notafiscal2");
	idNotaFiscal.attr("maxlength", "10");
	var idNotaFiscalStr = document
		.getElementById("id_notafiscal2")
		.value.toString()
		.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
	console.log(idNotaFiscalStr);
	document.getElementById("id_notafiscal2").value = idNotaFiscalStr;
});

$(document).ready(function () {
	$("#id_peso").on("change", function () {
		id_peso_var = document.getElementById("id_peso").value;
		if (id_peso_var) {
			console.log("ok");
		} else {
			document.getElementById("id_peso").value = 0;
			console.log("zero colocado");
		}
	});
});

$(document).ready(function () {
	id_peso_var = document.getElementById("id_peso").value;
	id_peso_var_str = id_peso_var
		.toString()
		.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
	document.getElementById("id_peso").type = "text";
	document.getElementById("id_peso").value = id_peso_var_str;

	id_valornf_var = document.getElementById("id_valornf").value;
	id_valornf_var_str = id_valornf_var.toString().replace(/.([^.]*)$/, ",$1");
	id_valornf_var_str_final = id_valornf_var_str.replace(
		/\B(?=(\d{3})+(?!\d))/g,
		"."
	);
	console.log(id_valornf_var_str_final);
	// id_valornf_var_str = id_valornf_var.toString().replace(/([0-9])([0-9]{2})$/, '$1,$2')

	document.getElementById("id_valornf").type = "text";
	document.getElementById("id_valornf").value = id_valornf_var_str_final;

	$("#cargaeditform").on("submit", function () {
		str = document.getElementById("id_peso").value;
		document.getElementById("id_peso").value = str.replace(/\./g, "");

		strNotaFiscal = document.getElementById("id_notafiscal").value;
		document.getElementById("id_notafiscal").value = strNotaFiscal.replace(
			/\./g,
			""
		);

		strNotaFiscal2 = document.getElementById("id_notafiscal2").value;
		document.getElementById("id_notafiscal2").value =
			strNotaFiscal2.replace(/\./g, "");

		strvalornf = document.getElementById("id_valornf").value;
		document.getElementById("id_valornf").value = strvalornf.replace(
			/\./g,
			""
		);
		strvalornffinal = document.getElementById("id_valornf").value;
		document.getElementById("id_valornf").value = strvalornffinal.replace(
			/\,/g,
			"."
		);
	});

	$("#cargaaddform").on("submit", function () {
		str = document.getElementById("id_peso").value;
		document.getElementById("id_peso").value = str.replace(/\./g, "");

		strNotaFiscal = document.getElementById("id_notafiscal").value;
		document.getElementById("id_notafiscal").value = strNotaFiscal.replace(
			/\./g,
			""
		);

		strNotaFiscal2 = document.getElementById("id_notafiscal2").value;
		document.getElementById("id_notafiscal2").value =
			strNotaFiscal2.replace(/\./g, "");

		strvalornf = document.getElementById("id_valornf").value;
		document.getElementById("id_valornf").value = strvalornf.replace(
			/\./g,
			""
		);
		strvalornffinal = document.getElementById("id_valornf").value;
		document.getElementById("id_valornf").value = strvalornffinal.replace(
			/\,/g,
			"."
		);
	});

	$("#id_peso").on({
		keyup: function (event) {
			$(event.target).val(function (index, value) {
				if (value.length > 1) {
					return (
						value
							.replace(/\D/g, "")
							// .replace(/([0-9])([0-9]{2})$/, '$1,$2')
							.replace(/^0+/, "")
							.replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".")
					);
				} else {
					return (
						value
							.replace(/\D/g, "")
							// .replace(/([0-9])([0-9]{2})$/, '$1,$2')
							.replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".")
					);
				}
			});
		},
	});

	$("#id_notafiscal").on({
		keyup: function (event) {
			$(event.target).val(function (index, value) {
				return (
					value
						.replace(/\D/g, "")
						// .replace(/([0-9])([0-9]{2})$/, '$1,$2')
						.replace(/^0+/, "")
						.replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".")
				);
			});
		},
	});

	$("#id_notafiscal2").on({
		keyup: function (event) {
			$(event.target).val(function (index, value) {
				return (
					value
						.replace(/\D/g, "")
						// .replace(/([0-9])([0-9]{2})$/, '$1,$2')
						.replace(/^0+/, "")
						.replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".")
				);
			});
		},
	});

	$("#id_valornf").on({
		keyup: function (event) {
			$(event.target).val(function (index, value) {
				if (value.length > 1) {
					return value
						.replace(/\D/g, "")
						.replace(/([0-9])([0-9]{2})$/, "$1,$2")
						.replace(/^0+/, "")
						.replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
				} else {
					return value
						.replace(/\D/g, "")
						.replace(/([0-9])([0-9]{2})$/, "$1,$2")
						.replace(/\B(?=(\d{3})+(?!\d)\.?)/g, ".");
				}
			});
		},

		focus: function () {
			$(this).select();
			console.log(this);
		},
	});
});

$(document).ready(function () {
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
				var color = element.color;
				console.log(pedido);
				console.log(fornecedor);
				console.log(cidade);
				console.log(cliente);
				console.log(" ");
				if (pedido === "900") {
					var elementfornecedor =
						document.getElementById("fornecedorinfo");
					elementfornecedor.innerHTML = "Escritório";
					var elementcidade = document.getElementById("cidadeinfo");
					elementcidade.innerHTML = cidade;
					var elementcliente = document.getElementById("clienteinfo");
					elementcliente.innerHTML = cliente;
					elementcliente.style.backgroundColor = "";
					elementcliente.style.backgroundColor = `${color}`;
					var elementcliente =
						document.getElementById("pedido_from_model");
					elementcliente.innerHTML = pedido;
				} else if (pedido === "901") {
					var elementfornecedor =
						document.getElementById("fornecedorinfo");
					elementfornecedor.innerHTML = "Escritório";
					var elementcidade = document.getElementById("cidadeinfo");
					elementcidade.innerHTML = cidade;
					var elementcliente = document.getElementById("clienteinfo");
					elementcliente.innerHTML = cliente;
					elementcliente.style.backgroundColor = "";
					elementcliente.style.backgroundColor = `${color}`;
					var elementcliente =
						document.getElementById("pedido_from_model");
					elementcliente.innerHTML = pedido;
				} else {
					var elementcidade = document.getElementById("cidadeinfo");
					elementcidade.innerHTML = cidade;
					var elementcliente =
						document.getElementById("fornecedorinfo");
					elementcliente.innerHTML = fornecedor;
					var elementcliente = document.getElementById("clienteinfo");
					elementcliente.innerHTML = cliente;
					elementcliente.style.backgroundColor = "";
					elementcliente.style.backgroundColor = `${color}`;
					var elementcliente =
						document.getElementById("pedido_from_model");
					elementcliente.innerHTML = pedido;
				}
			} else if (isNaN(idcontrato)) {
				var elementcidade = document.getElementById("cidadeinfo");
				elementcidade.innerHTML = "";
				var elementcliente = document.getElementById("fornecedorinfo");
				elementcliente.innerHTML = "";
				var elementcliente = document.getElementById("clienteinfo");
				elementcliente.innerHTML = "";
				var elementcliente =
					document.getElementById("pedido_from_model");
				elementcliente.innerHTML = "";
			}
		});
	});
});
