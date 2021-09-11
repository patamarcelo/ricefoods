$(document).ready(function () {
	$("#id_guias_notas").on("change", function () {
		var files = $("#id_guias_notas").prop("files");
		var names = $.map(files, function (val) {
			return val.name;
		});
		if (names.length > 0) {
			$("li").remove();
			$("#limpar_notas").remove();
			$("#id_guias_notas").after(
				`<div id="limpar_notas" style="cursor: not-allowed;"><h6 class="badge badge-pill bg-danger"> Limpar Notas</h6></div>`
			);
			$("#id_guias_notas").after(
				`<ol id="lista_notas_fiscais" style="padding-left : 25px; margin-top: 10px;"></ol>`
			);
		}
		for (let i = 0; i < names.length; i++) {
			console.log(names[i]);
			$("#lista_notas_fiscais").append(
				`<li id="${names[i]}"> &nbsp;&nbsp;&nbsp;&nbsp;${names[i]}</li>`
			);
		}

		$("#limpar_notas").on("click", function () {
			$("#id_guias_notas").val("");
			$("li").remove();
			$("#limpar_notas").remove();
			$("#id_guias_notas").css("background-color", "");
		});
	});
	$("input").each(function () {
		var input = $(this);
		input.on("change", function () {
			console.log(input);
			if (input.length > 0) {
				input.css("background-color", "green");
			}
		});
	});
});
