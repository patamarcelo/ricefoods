$(".simplehighlight").click(function () {
  $(this).toggleClass("clicked");
});

$(document).ready(function () {
  $("#cargas5").DataTable({
    searching: false,
  });
  $(".dataTables_length").addClass("bs-select");
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
  style = style + "table {width: 100%;font: 12px Calibri;  margin-top: 60px;}";
  style =
    style + "table, th, td {border: solid 1px #DDD; border-collapse: collapse;";
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

const alternarDestaque = () => $("#filtro").toggleClass("hide");
$("#btn_filtro").on("mouseenter", alternarDestaque);

function loadJson(selector) {
  return JSON.parse(document.querySelector(selector).getAttribute("data-json"));
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