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

	for (let i = 0; i < res.length; i++) {
		console.log(res[i].base);
		console.log(res[i].local);
		console.log(res[i].total);
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
					`<tr><td>${countCard}</td><td class="copy-data" data-clipboard-text="${jsonData[j].numero}">${cardNumberHtml}</td><td>${iconAvailable}</td><td>${jsonData[j].cartaobase}</td></tr>`
				);
			}
		}
		console.log(res[i].base);
		$(`#sub${res[i].base}`)
			.text(res[i].total)
			.addClass("text text-success font-weight-bold");
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
	$(".copy-data").click(function () {
		const t = 800;
		const t1 = 400;
		const t2 = 1390;

		const valueeeee = $(this).attr("data-clipboard-text");
		var elementtextadv = document.getElementById("cargasmotcopy");
		var newValFormEdit = valueeeee
			.replace(/\D/g, "")
			.replace(/^0+/, "")
			.replace(/\B(?=(\d{4})+(?!\d)\.?)/g, " ");
		elementtextadv.innerHTML = "Cartão Copiado: " + newValFormEdit;
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

// $("#CardVP input").on({
// 	keyup: function (event) {
// 		$(event.target).val(function (index, value) {
// 			return value
// 				.replace(/\D/g, "")
// 				.replace(/\B(?=(\d{4})+(?!\d)\.?)/g, " ");
// 		});
// 	},
// });
