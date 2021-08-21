$(document).on("submit", "#contato", function (e) {
	e.preventDefault();
	var valida = $("#validator").val();
	if (valida == "12") {
		$("#validator").css("border-color", "green");
		$("#waittabeladash").show();
		$(this).submit();
	} else {
		$("#validator").val("");
		$("#validator").css("border-color", "red");
		$("#validator").focus();
	}
});

$(document).on("submit", "#contato2", function (e) {
	e.preventDefault();
	var valida = $("#validatorcont").val();
	if (valida == "12") {
		$("#waittabeladash2").show();
		$("#validatorcont").css("border-color", "green");
		$(this).submit();
	} else {
		$("#validatorcont").val("");
		$("#validatorcont").css("border-color", "red");
		$("#validatorcont").focus();
	}
});
