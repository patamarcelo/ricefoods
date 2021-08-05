$(document).ready(function () {
	var totalsum = 0;
	lis = document.getElementsByClassName("comissaoAreceber");

	for (var i = 0; i < lis.length; i++) {
		totalsum += parseFloat(lis[i].getAttribute("data-comissao"));
	}

	var totalsum = numberWithCommas(parseFloat(totalsum).toFixed(2));
	console.log(`Total Gerado de comissão: R$ ${totalsum}`);
	var PesoTotalHtml = document.getElementById("totalComissaoGerado");
	var PesoTotalExcel = document.getElementById("totalComissaoGeradoExcel");

	if (PesoTotalHtml) {
		PesoTotalHtml.innerHTML = `<i><strong> R$ ${totalsum}</i></strong>`;
		PesoTotalExcel.innerHTML = `<i><strong> R$ ${totalsum}</i></strong>`;
	}
	
	var totalsumSaldo = 0;
	lis = document.getElementsByClassName("comissaosaldo");

	for (var i = 0; i < lis.length; i++) {
		totalsumSaldo += parseFloat(lis[i].getAttribute("data-comissaosaldo"));
	}

	var totalsumSaldo = numberWithCommas(parseFloat(totalsumSaldo).toFixed(2));
	console.log(`Total saldo de comissão R$ ${totalsumSaldo}`);
	var saldoTotalHtml = document.getElementById("totalcomissaoabertoID");
	var saldoTotalExcel = document.getElementById("totalcomissaoabertoIDExcel");

	if (saldoTotalHtml) {
		saldoTotalHtml.innerHTML = `<i><strong> R$ ${totalsumSaldo}</i></strong>`;
		saldoTotalExcel.innerHTML = `<i><strong> R$ ${totalsumSaldo}</i></strong>`;
	}
});

function numberWithCommas(x) {
	return x
		.toString()
		.replace(/\B(?=(\d{3})+(?!\d))/g, ".")
		.replace(/.([^.]*)$/, "," + "$1");
}

$(document).ready(function () {
	var totalsumcomissao = 0;
	liscomissao = document.getElementsByClassName("comissaopaga");

	for (var i = 0; i < liscomissao.length; i++) {
		totalsumcomissao += parseFloat(
			liscomissao[i].getAttribute("data-comissaopaga")
		);
	}

	var totalsumcomissao = numberWithCommas(
		parseFloat(totalsumcomissao).toFixed(2)
	);
	console.log(`Total Pago: R$ ${parseFloat(totalsumcomissao).toFixed(2)}`);
	var TotalPagoComissaoHtml = document.getElementById("totalpagocomissaoID");
	var TotalPagoComissaoExcel = document.getElementById(
		"totalpagocomissaoIDExcel"
	);

	console.log(typeof totalsumcomissao);
	console.log(totalsumcomissao);
	if (TotalPagoComissaoHtml) {
		if (totalsumcomissao === "0,00") {
			TotalPagoComissaoHtml.innerHTML = `<i><strong> R$ &nbsp; - </i></strong>`;
			TotalPagoComissaoExcel.innerHTML = `<i><strong> R$ &nbsp; - </i></strong>`;
		} else {
			TotalPagoComissaoHtml.innerHTML = `<i><strong> R$ ${totalsumcomissao}</i></strong>`;
			TotalPagoComissaoExcel.innerHTML = `<i><strong> R$ ${totalsumcomissao}</i></strong>`;
		}
	}
});
