$(document).ready(function () {
  $(".copy-data").click(function () {
    const t = 800;
    const t1 = 400;
    const t2 = 990;

    const valueeeee = $(this).attr("data-clipboard-text");
    var elementtextadv = document.getElementById("cargasmotcopy");
    elementtextadv.innerHTML = valueeeee;
    $("#clickeadvise").slideToggle(t1).delay(t2).slideToggle(t);
  });
});
