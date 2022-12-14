function loadJson(selector) {
	return JSON.parse(
		document.querySelector(selector).getAttribute("data-json")
	);
}

$(document).ready(function () {
	var jsonData = loadJson("#jsonCartaoVp");
	var cartaoBase = [];
	for (let i = 0; i < jsonData.length; i++) {
		cartaoBase.push(jsonData[i].cartaobase); //Adiciona as filials dentro do array, sem filtro
		console.log(jsonData[i].id, jsonData[i].cartaobase_name);
		console.log(jsonData[i].numero, jsonData[i].disponivel);
	}
	var filtCartaoBase = [...new Set(cartaoBase)]; // TODAS AS FILIAS FILTRADAS

	//RESUMO DE LOCAIS + QUANTIDADES
	var totalPorLocal = [];
	var totalPorLocal2 = [];
	for (let i = 0; i < filtCartaoBase.length; i++) {
		count = 0;
		for (let j = 0; j < jsonData.length; j++) {
			if (filtCartaoBase[i] === jsonData[j].cartaobase) {
				count++;
				totalPorLocal.push({
					local: `${filtCartaoBase[i]}`,
					base: `${jsonData[j].cartaobase_name}`,
				});
			}
		}
		totalPorLocal2.push({
			local: `${filtCartaoBase[i]}`,
			contagem: `${count}`,
		});
	}

	const uniq = new Set(totalPorLocal.map((e) => JSON.stringify(e)));
	const res = Array.from(uniq).map((e) => JSON.parse(e));

	for (let i = 0; i < res.length; i++) {
		for (let j = 0; j < totalPorLocal2.length; j++) {
			if (res[i].local == totalPorLocal2[j].local) {
				res[i].total = totalPorLocal2[j].contagem;
			}
		}
	}

	const numberTOAdviseCardMissing = 10;
	for (let i = 0; i < res.length; i++) {
		countCard = 0;
		for (let j = 0; j < jsonData.length; j++) {
			if (res[i].base == jsonData[j].cartaobase_name) {
				countCard++;
				var cardNumberHtml = jsonData[j].numero
					.replace(/\D/g, "")
					.replace(/^0+/, "")
					.replace(/\B(?=(\d{4})+(?!\d)\.?)/g, " ");

				var iconAvailable =
					jsonData[j].disponivel == false
						? '<i class="far fa-check-circle text-success"></i>'
						: '<i class="far fa-times-circle text-danger"></i>';

				$(`#table${res[i].base} > tbody:last-child`).append(
					`<tr id="cardVPtr-${jsonData[j].id}"><td>${countCard}</td><td class="copy-data" data-clipboard-text="${jsonData[j].numero}">${cardNumberHtml}</td><td onClick="editUserCardVP(${jsonData[j].id})" data-toggle="modal" data-target="#myModalCartaoVP")" data-disponivel="${jsonData[j].disponivel}">${iconAvailable}</td><td>${jsonData[j].cartaobase}</td></tr>`
				);
			}
		}

		console.log(res[i].base);
		var totalCardNumberColor =
			res[i].total < numberTOAdviseCardMissing
				? "text-danger"
				: "text-success";
		$(`#sub${res[i].base}`)
			.text(res[i].total)
			.addClass(`text ${totalCardNumberColor} font-weight-bold`);
	}

	for (let i = 0; i < res.length; i++) {
		if (res[i].total < numberTOAdviseCardMissing) {
			$("#divOcultarCartoesVpCargas").addClass("filial-sem-cartaovp");
		}
	}
});

$("#cartoesVPCard a").on("click", function (e) {
	e.preventDefault();
	$(this).tab("show");
});

var cardVp = $("#CardVP");
function ocultarmostrar(el, el2) {
	if (document.getElementById("CardVP").classList.contains("hide")) {
		cardVp.slideToggle(1000);
		cardVp.removeClass("hide");
		document.getElementById(el2).className = "fas fa-eye text-info";
	} else {
		cardVp.slideToggle(500);
		cardVp.addClass("hide");
		document.getElementById(el2).className = "fas fa-eye-slash text-danger";
	}
}

$(document).ready(function () {
	$("#CardVP .copy-data").click(function () {
		const t = 800;
		const t1 = 400;
		const t2 = 1390;

		const valueeeee = $(this).attr("data-clipboard-text");
		var elementtextadv = document.getElementById("cargasmotcopy");
		console.log(elementtextadv);
		var newValFormEdit = valueeeee
			.replace(/\D/g, "")
			.replace(/^0+/, "")
			.replace(/\B(?=(\d{4})+(?!\d)\.?)/g, " ");
		elementtextadv.innerHTML = "Cart??o Copiado: " + newValFormEdit;
		$("#clickeadvise").slideToggle(t1).delay(t2).slideToggle(t);
	});
});

function MyFunction(tableid, inputid) {
	var input, filter, table, tr, td, i, txtValue, txtValue2;
	input = document.getElementById(inputid);
	filter = input.value.toUpperCase();
	table = document.getElementById(tableid);
	tr = table.getElementsByTagName("tr");
	for (i = 0; i < tr.length; i++) {
		td = tr[i].getElementsByTagName("td")[0];
		td1 = tr[i].getElementsByTagName("td")[1];
		if (td || td1) {
			txtValue = td.textContent || td.innerText;
			txtValue2 = td1.textContent || td1.innerText;
			if (
				txtValue.toUpperCase().indexOf(filter) > -1 ||
				txtValue2.toUpperCase().indexOf(filter) > -1
			) {
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
}

$("#CardVP input").on({
	keyup: function (event) {
		$(event.target).val(function (index, value) {
			return value.replace(/\D/g, "").replace(/(\d{4}(?!\s))/g, "$1 ");
			// .replace(/\B(?=(\d{4})+(?!\d))/g, " ")
		});
	},
});

$(document).ready(function () {
	$(".card-body input").attr("maxlength", "19");
});

//UpdateCartaoVP

$("form#updateCardVPForm").on("submit", function (event) {
	event.preventDefault();

	var urlform = $("[data-validate-url-cardvp]").attr(
		"data-validate-url-cardvp"
	);
	console.log(urlform);
	var idInput = $('input[name="formIdCardVP"]').val().trim();
	var cardvpInput = $('input[name="formCardVPInput"]').is(":checked");
	var cardNumberVal = $(`#cardVPtr-${idInput}`)
		.find("td[data-clipboard-text]")
		.attr("data-clipboard-text")
		.replace(/\D/g, "")
		.replace(/^0+/, "")
		.replace(/\B(?=(\d{4})+(?!\d)\.?)/g, " ");

	if (cardvpInput === true) {
		var valCardAjax = "True";
	} else {
		var valCardAjax = "False";
	}
	// Create Ajax Call
	$.ajax({
		url: urlform,
		data: {
			id: idInput,
			name: valCardAjax,
		},
		dataType: "json",
		success: function (data) {
			if (data.user) {
				updateCardDispTable(data.user);
				console.log(data.user);
				$.notify(
					`${cardNumberVal} | Cart??o atualizado com sucesso!!`,
					"success"
				);
			}
		},
	});
	$("form#updateCardVPForm").trigger("reset");
	$("#myModalCartaoVP").modal("hide");
	return false;
});

function updateFormCardVp() {
	$("form#updateCardVPForm").trigger("reset");
}

function editUserCardVP(id) {
	if (id) {
		tr_id = "#cardVPtr-" + id;
		console.log(tr_id);
		cardDisponivel = $(tr_id)
			.find("td[data-disponivel]")
			.attr("data-disponivel");
		console.log(cardDisponivel);
		cartao = $(tr_id)
			.find("td[data-clipboard-text]")
			.attr("data-clipboard-text");

		var cartaoForm = document.getElementById("updateCradVPUser");
		cartaoForm.innerHTML = cartao
			.replace(/\D/g, "")
			.replace(/^0+/, "")
			.replace(/\B(?=(\d{4})+(?!\d)\.?)/g, " ");

		$("#form-id-cardvp").val(id);
		if (cardDisponivel === "true") {
			$("#form-name-disponivel").attr("checked", true);
		} else {
			$("#form-name-disponivel").attr("checked", false);
		}
	}
	var cardvpInput = $('input[name="formCardVPInput"]').is(":checked");
	console.log(cardvpInput);
}

function updateCardDispTable(user) {
	tr_id = "#cardVPtr-" + user.id;
	disponivel = user.name;
	console.log(disponivel);
	dataDisponivelTable = $(tr_id).find("td[data-disponivel]");
	if (disponivel === false) {
		var aElement = $(tr_id).find("i");
		console.log(aElement);
		dataDisponivelTable.attr("data-disponivel", "false");
		aElement.removeClass("fa-times-circle text-danger");
		aElement.addClass("fa-check-circle text-success");
	} else {
		var aElement = $(tr_id).find("i");
		dataDisponivelTable.attr("data-disponivel", "true");
		console.log(aElement);
		aElement.removeClass("fa-check-circle text-success");
		aElement.addClass("fa-times-circle text-danger");
	}
}
