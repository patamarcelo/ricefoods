function loadJson(selector) {
	return JSON.parse(
		document.querySelector(selector).getAttribute("data-json")
	);
}

Date.prototype.addDays = function (days) {
	const date = new Date(this.valueOf());
	date.setDate(date.getDate() + days);
	return date;
};

function AddDays(date, days) {
	var newdate = new Date(date);
	var newdatePlus = newdate.addDays(days);
	return newdatePlus;
}

function FormatData(data) {
	return moment(data).format("DD/MM/YYYY");
}

function FormatPlaca(placa) {
	return `${placa.slice(0, 3)} ${placa.slice(3, 9)}`;
}
function Formatpeso(x) {
	if (x > 0) {
		return x
			.toString()
			.replace(/\B(?=(\d{3})+(?!\d))/g, ".")
			.replace(/.([^.]*)$/, "." + "$1");
	} else {
		return x;
	}
}

let diasDaSemana = [
	"Segunda-Feira",
	"Terça-Feira",
	"Quarta-Feira",
	"Quinta-Feira",
	"Sexta-Feira",
	"Sábado",
	"Domingo",
	"Segunda-Feira",
	"Terça-Feira",
	"Quarta-Feira",
	"Quinta-Feira",
	"Sexta-Feira",
	"Sábado",
	"Domingo",
];

let curr = new Date();
var FirstDay = curr.getDate() - curr.getDay();
var firstday = new Date(curr.setDate(FirstDay));
var TesteDayStr = moment(firstday).format("YYYY-MM-DD");
var firstWeek = [];

for (let i = 2; i <= 15; i++) {
	var newDataTo = AddDays(TesteDayStr, i);
	var newDataToAdd = moment(newDataTo).format("YYYY-MM-DD");
	firstWeek.push(newDataToAdd);
}

console.log(firstWeek[0]);
console.log(firstWeek);
function TotalCarregado(array, data, status) {
	var TotalCarregado = 0;
	for (let i = 0; i < array.length; i++) {
		if (array[i].data_agenda >= data && array[i].situacao == status) {
			TotalCarregado += 1;
		}
	}
	return TotalCarregado;
}

$(document).ready(function () {
	var jsonData = loadJson("#jsonDataAgenda");

	var TotalCarregadoArray = TotalCarregado(
		jsonData,
		firstWeek[0],
		"Carregado"
	);

	var totalDeCargasGeral = 0;
	for (let i = 0; i < firstWeek.length; i++) {
		var HeadDataDate = firstWeek[i];
		var headDataHtml = `${diasDaSemana[i]} - ${FormatData(firstWeek[i])}`;
		var idHead = `HeadDia${i}`;
		var diaAtual = document.getElementById(idHead);
		var totalDeCargas = 0;
		diaAtual.innerHTML = headDataHtml;
		var totalDeCargasCarregado = 0;
		var totalDeCargasCarregadoCabecalho = 0;
		var placasCarregadas = [];
		var placasAgendadas = [];
		for (let j = 0; j < jsonData.length; j++) {
			if (jsonData[j].data_agenda === HeadDataDate) {
				totalDeCargas++;

				var clonedDiv = $(`#dadosagendamento${i}`).clone();
				clonedDiv.attr("id", `dadosagendamentoC${j}`);
				clonedDiv.css("display", "block");
				$(`#dadosagendamento${i}`).before(clonedDiv);
				$(`#dadosagendamentoC${j} .motoristaAgendaClass`).text(
					`${jsonData[j].motorista}`
				);
				$(`#dadosagendamentoC${j} .motoristaAgendaClass`).css(
					"white-space",
					"nowrap"
				);
				$(`#dadosagendamentoC${j} .motoristaAgendaClass`).css(
					"overflow",
					"hidden"
				);
				if (jsonData[j].nfiscal == null) {
					$(`#dadosagendamentoC${j} .nfAgendaClass`).text("Sem NF");
					$(`#dadosagendamentoC${j} .nfAgendaClass`).css(
						"color",
						"red"
					);
				} else {
					$(`#dadosagendamentoC${j} .nfAgendaClass`).text(
						`NF ${Formatpeso(jsonData[j].nfiscal)}`
					);
				}
				if (jsonData[j].peso == 0) {
					$(`#dadosagendamentoC${j} .pesoAgendaClass`).addClass(
						"text-primary"
					);
				}
				if (jsonData[j].situacao == "Carregado") {
					totalDeCargasGeral++;
					totalDeCargasCarregado += jsonData[j].peso;
					placasCarregadas.push(jsonData[j].placa);
					$(`#dadosagendamentoC${j} .enumerateitemAgendaClass`).text(
						`${totalDeCargasGeral}`
					);
					$(`#dadosagendamentoC${j} .pesoAgendaClass`).text(
						`${Formatpeso(jsonData[j].peso)} Kg`
					);
					$(`#dadosagendamentoC${j} .placaAgendaClass`).text(
						`${FormatPlaca(jsonData[j].placa)}`
					);

					$(`#dadosagendamentoC${j} .dadosmotoristas`).removeClass(
						"bg-warning"
					);
					$(`#dadosagendamentoC${j} .dadosmotoristas`).css(
						"background-color",
						"rgb(0,128,0,0.2)"
					);
					$(
						`#dadosagendamentoC${j} .enumerateitemAgendaClass`
					).addClass("text-success");
				} else {
					totalDeCargasCarregado += jsonData[j].veiculo;
					placasAgendadas.push(jsonData[j].placa);
					TotalCarregadoArray += 1;
					$(`#dadosagendamentoC${j} .enumerateitemAgendaClass`).text(
						`${TotalCarregadoArray}`
					);

					$(`#dadosagendamentoC${j} .pesoAgendaClass`).text(
						`${Formatpeso(jsonData[j].veiculo)} Kg`
					);
					$(`#dadosagendamentoC${j} .placaAgendaClass`).text(
						`${FormatPlaca(jsonData[j].placa)}`
					);
					var getUrlD = $(`#dadosagendamentoC${j} a:eq(0)`)
						.attr("target", "_blank")
						.attr("data-url-attr")
						.replace("123456789987", `${jsonData[j].id}`);
					$(`#dadosagendamentoC${j} a:eq(0)`).attr(
						"href",
						`${getUrlD}`
					);
				}
			} else {
				console.log("Error");
			}

			var PlacasSemDuplicidades = [...new Set(placasCarregadas)];
			var PlacasSemDuplicidadesAgenda = [...new Set(placasAgendadas)];

			var TotalPlacas =
				PlacasSemDuplicidades.length +
				PlacasSemDuplicidadesAgenda.length;
			if (TotalPlacas > 1) {
				$(`#DivDia${i} .quantidadeDeCargas`).text(
					`${TotalPlacas} Cargas`
				);
			} else {
				$(`#DivDia${i} .quantidadeDeCargas`).text(
					`${TotalPlacas} Carga`
				);
			}
			$(`#DivDia${i} .pesoDeCargas`).text(
				`${Formatpeso(totalDeCargasCarregado)} Kg`
			);
		}
	}
	$(".resumodados").each(function () {
		var pesoTotalGerado = $(this).find("span:eq(1)").text();
		if (pesoTotalGerado === "0 Kg") {
			$(this).css("display", "none");
		} else {
			console.log("nao encontrei a classe");
		}
	});

	// for (let i = 0; i < secondWeek.length; i++) {
	// 	var headDataHtml2 = `${diasDaSemana[i]} - ${FormatData(secondWeek[i])}`;
	// 	var idHead2 = `HeadDia${i}Semana2`;
	// 	var diaAtual2 = document.getElementById(idHead2);
	// 	diaAtual2.innerHTML = headDataHtml2;
	// }

	// var totalDeCargas = 0;
	// for (let i = 1; i <= 8; i++) {
	// 	totalDeCargas++;
	// 	var clonedDiv = $("#dadosagendamento0").clone();
	// 	clonedDiv.attr("id", `dadosagendamento${i}`);
	// 	clonedDiv.css("display", "block");
	// 	$("#dadosagendamento0").after(clonedDiv);
	// 	$(`#dadosagendamento${i} .motoristaAgendaClass`).text("Marcelo Pata");
	// 	$(`#dadosagendamento${i} .placaAgendaClass`).text(`${i}`);
	// 	$(`#dadosagendamento${i} .pesoAgendaClass`).text(`${i + 202}`);
	// 	$(`#dadosagendamento${i} .nfAgendaClass`).text(`NF ${i + 33939999}`);
	// 	$(`#dadosagendamento${i} .enumerateitemAgendaClass`).text(`NF ${i}`);
	// }
	// $("#DivDia0 .quantidadeDeCargas").text(`${totalDeCargas} Cargas`);

	// console.log(jsonData.length);
	// var count = 0;
	// for (let i = 0; i < jsonData.length; i++) {
	// 	if (jsonData[i].situacao == "Agendado") {
	// 		count++;
	// 		console.log(
	// 			`Contagem: ${count}`,
	// 			jsonData[i].situacao,
	// 			FormatData(jsonData[i].data_agenda),
	// 			FormatPlaca(jsonData[i].placa),
	// 			jsonData[i].motorista,
	// 			jsonData[i].nfiscal,
	// 			jsonData[i].peso,
	// 			jsonData[i].veiculo
	// 		);
	// 	} else {
	// 		count++;
	// 		console.log(
	// 			`Contagem: ${count}`,
	// 			jsonData[i].situacao,
	// 			FormatData(jsonData[i].data_agenda),
	// 			FormatPlaca(jsonData[i].placa),
	// 			jsonData[i].motorista,
	// 			jsonData[i].veiculo
	// 		);
	// 	}
	// }
});
