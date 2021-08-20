$(".simplehighlight").click(function () {
	$(this).toggleClass("clicked");
});

window.setTimeout(function () {
	$(".alert")
		.fadeTo(500, 0)
		.slideUp(500, function () {
			$(this).remove();
		});
}, 3000);

$("table tbody").on("click", "td", function () {
	$(this).toggleClass("selected");
});

document.getElementById("select-all").onclick = function () {
	var checkboxes = document.querySelectorAll('input[type="checkbox"]');
	for (var checkbox of checkboxes) {
		checkbox.checked = this.checked;
	}
};

function CleanAllFields() {
	console.log("OK");
	$("input").each(function () {
		var idF = $(this).attr("id");
		if (idF == "btnLimparForm") {
			$(this).removeClass("btn-xs btnLimparForm");
			$(this).addClass("btn-xs btnLimparForm");
			console.log("pula essa");
		} else {
			var clean = $(this).val();
			if (clean.length > 1) {
				console.log(clean);
				$(this).val("");
			}
		}
		$("select").each(function () {
			$(this).prop("selectedIndex", 0).val();
		});
	});
}

// function Mudarestado(el) {
//     var display = document.getElementById(el).style.display;
//     if (display == "none")
//         document.getElementById(el).style.display = 'block';
//     else
//         document.getElementById(el).style.display = 'none';
// }

function Ocultarfiltros(el) {
	if (document.getElementById("filtro").classList.contains("hide")) {
		document.getElementById(el).classList.remove("hide");
	} else {
		document.getElementById(el).classList.add("hide");
	}
}

function Mudarestado(el) {
	if (document.getElementById("secondboxout").classList.contains("hide")) {
		document.getElementById(el).classList.remove("hide");
	} else {
		document.getElementById(el).classList.add("hide");
	}
}

// $(document).ready('change', function Hidetransp(el) {
//     var e = document.getElementById(el).style.display;
//     if (e.style.display){
//     e.style.display = ((e.style.display!='none') ? 'none' : 'block');
//     }
//     else {e.style.display='block'}
//     })

$(document).ready(function () {
	$("#btnExport").click(function (e) {
		e.preventDefault();
		var table_div = document.getElementById("cargasfiltro2");
		// esse "\ufeff" é importante para manter os acentos
		var blobData = new Blob(["\ufeff" + table_div.outerHTML], {
			type: "application/vnd.ms-excel",
		});
		var url = window.URL.createObjectURL(blobData);
		var a = document.createElement("a");
		a.href = url;
		a.download = "Cargas.xls";
		a.click();
	});
});

function createPDF() {
	var sTable = document.getElementById("cargasfiltro2").innerHTML;

	var style = "<style>";
	style =
		style + "table {width: 100%;font: 12px Calibri;  margin-top: 60px;}";
	style =
		style +
		"table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
	style = style + "white-space: nowrap;";
	style = style + "padding: 2px 3px;text-align: center;}";
	style = style + "</style>";

	// CREATE A WINDOW OBJECT.
	var win = window.open("", "", "_blank", "height=700,width=700");

	win.document.write("<html><head>");
	win.document.write("<title> Cargas  </title>"); // <title> FOR PDF HEADER.
	win.document.write(style); // ADD STYLE INSIDE THE HEAD TAG.
	win.document.write("</head>");
	win.document.write("<body>");
	win.document.write(sTable); // THE TABLE CONTENTS INSIDE THE BODY TAG.
	win.document.write(
		'<embed width="100%" height="100%" src="data:application/pdf;base64,' +
			base64 +
			'" type="application/pdf"/>'
	);
	win.document.write("</body></html>");

	win.document.close(); // CLOSE THE CURRENT WINDOW.
}

$(document).ready(function () {
	$("#id_data").mask("00/00/0000");
	$("#id_data__gte").mask("00/00/0000");
	$("#id_data__lte").mask("00/00/0000");
});

$(document).ready(function () {
	$("#id_data_agenda").mask("00/00/0000");
	$("#id_data_agenda__gte").mask("00/00/0000");
	$("#id_data_agenda__lte").mask("00/00/0000");
});

const getCellValue = (tr, idx) =>
	tr.children[idx].innerText || tr.children[idx].textContent;

const comparer = (idx, asc) => (a, b) =>
	((v1, v2) =>
		v1 !== "" && v2 !== "" && !isNaN(v1) && !isNaN(v2)
			? v1 - v2
			: v1.toString().localeCompare(v2))(
		getCellValue(asc ? a : b, idx),
		getCellValue(asc ? b : a, idx)
	);

// do the work...
document.querySelectorAll("th").forEach((th) =>
	th.addEventListener("click", () => {
		const table = th.closest("table");
		const tbody = table.querySelector("tbody");
		Array.from(tbody.querySelectorAll("tr"))
			.sort(
				comparer(
					Array.from(th.parentNode.children).indexOf(th),
					(this.asc = !this.asc)
				)
			)
			.forEach((tr) => tbody.appendChild(tr));
	})
);

$("#badgetransp").hover(
	function () {
		$("#badgetransp").removeClass("badge-info").addClass("badge-warning");
	},
	function () {
		$("#badgetransp").removeClass("badge-warning").addClass("badge-info");
	}
);

new ClipboardJS(".copy-data");

// Alterar destaque entrando e saindo com o Mouse
// const alternarDestaque = () => $("#filtro").toggleClass("hide");
// $("#btn_filtro").on("mouseenter", alternarDestaque);

function loadJson(selector) {
	return JSON.parse(
		document.querySelector(selector).getAttribute("data-json")
	);
}

$(document).ready(function () {
	const jsonMotoristas = loadJson("#jsonMotoristas");
	const resultMot = jsonMotoristas.map(({ motorista }) => motorista);
	var jsonPlacas = loadJson("#jsonPlacas");
	const resultPlaca = jsonPlacas.map(({ placa }) => placa);

	$("#id_motorista__icontains").autocomplete({
		source: resultMot,
	});
	$("#id_placa__icontains").autocomplete({
		source: resultPlaca,
	});
});

$(document).ready(function () {
	var totalsum = 0;
	lis = document.getElementsByClassName("pesocarregado");

	for (var i = 0; i < lis.length; i++) {
		totalsum += parseInt(lis[i].getAttribute("data-pesoCarregado"));
	}
	console.log(`Total Carregado: ${numberWithCommas(totalsum)} Kg`);

	var PesoTotalHtml = document.getElementById("totalPesoCarregadoJsID");

	if (PesoTotalHtml) {
		PesoTotalHtml.innerHTML = `${numberWithCommas(totalsum)} Kg`;
		var PesoTotalExcel = document.getElementById(
			"totalPesoCarregadoJsExcel"
		);
		PesoTotalExcel.innerHTML = `${numberWithCommas(totalsum)} Kg`;
	}

	var totalsumAgenda = 0;
	lisagenda = document.getElementsByClassName("pesoagendado");

	for (var i = 0; i < lisagenda.length; i++) {
		if (lisagenda[i].getAttribute("data-pesoAgendado") != null) {
			totalsumAgenda += parseInt(
				lisagenda[i].getAttribute("data-pesoAgendado")
			);
		} else {
			var totalsumAgenda = 0;
		}
	}

	var PesoTotalAgendado = document.getElementById("totalPesoAgendadoID");
	if (PesoTotalAgendado) {
		PesoTotalAgendado.innerHTML = `${numberWithCommas(totalsumAgenda)} Kg`;
	}

	var PesoTotalAgendadoExcel = document.getElementById("AgendadoTotalExcel");
	if (PesoTotalAgendadoExcel) {
		PesoTotalAgendadoExcel.innerHTML = `${numberWithCommas(
			totalsumAgenda
		)} Kg`;
		console.log(`Total Agendado: ${numberWithCommas(totalsumAgenda)} Kg`);
	}

	var PesoTotalGeralHtml = document.getElementById("pesoTotalHtml");
	if (PesoTotalGeralHtml) {
		var PesoTotalCalGeral = totalsum + totalsumAgenda;
		PesoTotalGeralHtml.innerHTML = `${numberWithCommas(
			PesoTotalCalGeral
		)} Kg`;
		var PesoTotalGeralExcel = document.getElementById("PesoTotalExcel");
		PesoTotalGeralExcel.innerHTML = `${numberWithCommas(
			PesoTotalCalGeral
		)} Kg`;
		console.log(`Total Geral: ${numberWithCommas(PesoTotalCalGeral)} Kg`);
	}
});

function numberWithCommas(x) {
	return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

$(document).ready(function () {
	$("#id_data__gte").addClass("datepicker");
	$("#id_data__lte").addClass("datepicker");
	$(".datepicker").datepicker({
		// format: "dd/mm/yyyy",
		locale: "pt-br",
		// startDate: "-3d",
	});
});

$(function () {
	$.datepicker.setDefaults({
		firstDay: 1,
		showOn: "focus",
		dateFormat: "dd/mm/yy",
		dayNames: [
			"Domingo",
			"Segunda",
			"Terça",
			"Quarte",
			"Quinta",
			"Sexta",
			"Sábado",
		],
		dayNamesMin: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sab"],
		monthNames: [
			"Janeiro",
			"Fevereiro",
			"Março",
			"Abril",
			"Maio",
			"Junho",
			"Julho",
			"Agosto",
			"Setembro",
			"Outubro",
			"Novembro",
			"Dezembro",
		],
	});
});
