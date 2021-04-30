$(document).ready(function () {
  $(".copy-data").click(function () {
    const t = 800;
    const t1 = 400;
    const t2 = 500;

    // const attr = e.target.attr("data-clipboard-text");
    // alert('marcelo'));
    const valueeeee = $(this).attr("data-clipboard-text");
    // console.log(valueeeee);
    // console.log(typeof valueeeee);
    var elementtextadv = document.getElementById("cargasmotcopy");
    elementtextadv.innerHTML = valueeeee;
    $("#clickeadvise").slideToggle(t1).delay(t2).slideToggle(t);
  });
});
