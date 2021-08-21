// function loadJson(selector) {
// 	return JSON.parse(
// 		document.querySelector(selector).getAttribute("data-json")
// 	);
// }

$(document).ready(function () {
	var linkAjax = $("#jsonData").attr("data-url-ajax");
	console.log(linkAjax);

	$.ajax({
		url: linkAjax,
		success: function (data) {
			const obj = JSON.parse(data);
			console.log(typeof obj);
			count = 0;
			for (let i = 0; i < obj.length; i++) {
				// console.log(count);
				// count += 1;
				console.log(obj[i].fields);
				// console.log(obj[i].fields.placa);
				$("ol").append(
					`<li> ${obj[i].fields.placa} - ${obj[i].fields.motorista}</li>`
				);
			}
		},
	});
});
