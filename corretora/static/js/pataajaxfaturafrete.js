$(document).ready(function () {
	$("#cursoropen").click(function () {
		$("#formFatura").slideToggle("slow");
		$("html,body").animate({ scrollTop: 9999 }, "slow");
	});
});

$(document).ready(function () {
	function onlyUnique(value, index, self) {
		return self.indexOf(value) === index;
	}	  
	var ids_cargas_table = [];
	var ids_cargas_table_unique = ids_cargas_table.filter(onlyUnique).sort()

		$("#switch").on("click", function () {
			var checkboxes = document
				.getElementById("bodycargasfiltro")
				.querySelectorAll('input[type="checkbox"][name=chkOrgRow]');
			for (var checkbox of checkboxes) {
				if (this.checked) {
					checkbox.checked = this.checked;
					let idInsert = checkbox.id.split("-").pop();
					ids_cargas_table.push(idInsert);
				} else {
					this.checked = false;
					let idtakeof = checkbox.id.split("-").pop();
					let index = ids_cargas_table.indexOf(idtakeof);
					if (index >= 0) {
					ids_cargas_table.splice(index, 1);
					}
				}
			}
			console.log(ids_cargas_table);
		});
	$("#bodycargasfiltro")
		.find("input:checkbox")
		.on("click", function () {
			if ($(this).is(":checked")) {
				let trid = $(this).closest("tr").attr("id"); // table row ID
				console.log(trid)
				let idInsert = trid.split("-").pop();
				ids_cargas_table.push(idInsert);
			} else {
				let trid = $(this).closest("tr").attr("id"); // table row ID
				console.log(trid)
				let idtakeof = trid.split("-").pop();
				let index = ids_cargas_table.indexOf(idtakeof);
				if (index >= 0) {
					ids_cargas_table.splice(index, 1);
				}
			}
			console.log(ids_cargas_table);
		});
	$("#formFaturaFretes button").on("click", function (event) {
		event.preventDefault();
		var urlformfatura = $("form[url-form-fatura]").attr("url-form-fatura");
		console.log(urlformfatura);

		var idscargaInput = ids_cargas_table_unique;
		var numeroInput = $("#faturanumero").val().trim();
		var empresaInput = $("#empresa option:selected").val().trim();
		var transportadoraInput = $("#transportadora option:selected")
			.val()
			.trim();
		var datafaturaInput = $("#datafatura").val().trim();
		var datavencimentofaturaInput = $("#datafaturavencimento").val().trim();
		var valorfaturaInput = $("#valorfatura").val().trim();
		var obsInput = $("#obs").val().trim();
		console.log(numeroInput);
		console.log(empresaInput);
		console.log(transportadoraInput);
		console.log(datafaturaInput);
		console.log(datavencimentofaturaInput);
		console.log(valorfaturaInput);
		console.log(obsInput);

		if (
			moment(datafaturaInput, "DD/MM/YYYY", true).isValid() &&
			moment(datavencimentofaturaInput, "DD/MM/YYYY", true).isValid()
		) {
			if (
				idscargaInput &&
				numeroInput &&
				empresaInput &&
				transportadoraInput &&
				datafaturaInput &&
				datavencimentofaturaInput &&
				valorfaturaInput
			) {
				// Create Ajax Call
				$.ajax({
					url: urlformfatura,
					data: {
						ids_carga: idscargaInput,
						numero: numeroInput,
						empresa: empresaInput,
						transportadora: transportadoraInput,
						datafatura: datafaturaInput,
						datavencimentofatura: datavencimentofaturaInput,
						valorfatura: valorfaturaInput,
						obs: obsInput,
					},
					dataType: "json",
					success: function (data) {
						if (data) {
							console.log(data);
							// updateToUserTabelClassificacao(data);
							$.notify(
								`Fatura Número ${
									data.numero
								} | Com valor de ${parseFloat(
									data.valor
								).toLocaleString("pt-br", {
									style: "currency",
									currency: "BRL",
								})} para a ${data.transp}`,
								{
									position: "bottom center",
									className: "success",
								}
							);
							UpdateFaturaFrete(ids_cargas_table_unique, data);
						}
						$("#formFaturaFretes").trigger("reset");
						$("#formFatura").slideToggle("slow");
						return false;
					},
					error: function (request, error) {
						$.notify(
							`Verificar se o numero de pedido já existe!!`,
							{ position: "bottom center" },
							"error"
						);
					},
				});
			} else {
				$.notify(
					`Dados incompletos!!`,
					{ position: "bottom center" },
					"error"
				);
			}
		} else {
			$.notify(`Data Inválida!!`, { position: "bottom center" }, "error");
		}
	});
});

function UpdateFaturaFrete(arr, data) {
	for (let i = 0; i < arr.length; i++) {
		var tr_id = "#user-" + arr[i];
		console.log(tr_id);
		$(`${tr_id} > td:nth-child(19)`).html(
			'<i class="text text-success fas fa-check"></i>'
		);
		$(`${tr_id} > td:nth-child(20)`).html(`${data.numero}`);
	}
}
