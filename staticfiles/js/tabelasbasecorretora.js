///////////////////JS AJAX TABELAS/////////////////////////////////////////////
setInterval(function () {
  refreshTabelasDashboard();
}, 720000); // 12 Minutos
var urltabeladash = $("#waittabeladash").attr("data-tabeladash-url");
function refreshTabelasDashboard() {
  $("#lock-refresh-tabelasdash")
    .addClass("fa-spin")
    .delay(6000)
    .queue("fx", function () {
      $(this).removeClass("fa-spin");
    });
  // Whatever here.
  $.ajax({
    url: urltabeladash,
    beforeSend: function () {
      $("#waittabeladash").show();
    },
    complete: function () {
      $("#waittabeladash").hide();
    },
    success: function (data) {
      console.log(data);
      document.getElementById("ajaxtabeladash").innerHTML = data;

      setTimeout(function () {
        document.getElementById("contratodash").classList.remove("hide");
        document.getElementById("cargasdash").classList.remove("hide");
        document.getElementById("comidash").classList.remove("hide");
      }, 300);

      setTimeout(function () {
        document.getElementById("tabelascargas").classList.remove("hide");
      }, 200);

      setTimeout(function () {
        document.getElementById("tabelaspedidos").classList.remove("hide");
      }, 250);

      setTimeout(function () {
        document.getElementById("comidash").classList.add("hide");
        document.getElementById("ocultar").className =
          "fas fa-eye-slash text-danger";
      }, 2000);
    },
  });
}

function ocultarmostrar(el, el2) {
  if (document.getElementById("comidash").classList.contains("hide")) {
    document.getElementById(el).classList.remove("hide");
    document.getElementById(el2).className = "fas fa-eye text-info";
  } else {
    document.getElementById(el).classList.add("hide");
    document.getElementById(el2).className = "fas fa-eye-slash text-danger";
  }
}

///////////////////JS AJAX CARGAS/////////////////////////////////////////////

setInterval(function () {
  refreshTabelaCargas();
}, 900000); // 15 Minutos
var urlcarga = $("#waitcargas").attr("data-carga-url");
var urlpedido = $("#wait").attr("data-pedido-url");

function refreshTabelaCargas() {
  $("#lock-refresh")
    .addClass("fa-spin")
    .delay(6000)
    .queue("fx", function () {
      $(this).removeClass("fa-spin");
    });
  // Whatever here.
  $.ajax({
    url: urlcarga,
    beforeSend: function () {
      $("#waitcargas").show();
    },
    complete: function () {
      $("#waitcargas").hide();
    },
    success: function (data) {
      document.getElementById("ajaxcargas").innerHTML = data;
      $(document).ready(function () {
        $("#dtBasicExample2").DataTable({
          order: [[3, "asc"]],
        });
        $(".dataTables_length").addClass("bs-select");
      });

      $(".simplehighlight").click(function () {
        $(this).toggleClass("clicked");
      });

      //Chama a função com click em qualquer checkbox

      $("#tabelascargas10")
        .find("input:checkbox")
        .on("change", function () {
          //Atribui o valor do input p/ variável 'valor'
          var total = 0;
          $("#tabelascargas10")
            .find(":checkbox")
            .each(function () {
              if ($(this).is(":checked")) {
                console.log($(this).val());
                console.log(typeof parseFloat($(this).val()));

                total = total + parseFloat($(this).val());
                console.log(total);
              }
            });
          var total1 = total.toLocaleString("pt-BR");

          if (total1 == 0) {
            $("#icms").val("Peso em Kg");
          } else {
            $("#icms").val(total1);
          }
        });

      document.getElementById("select-all").onclick = function () {
        var checkboxes = document
          .getElementById("tabelascargas10")
          .querySelectorAll('input[type="checkbox"][name=icms]');
        for (var checkbox of checkboxes) {
          checkbox.checked = this.checked;
        }
      };

      document.getElementById("select-all-p").onclick = function () {
        var checkboxes = document
          .getElementById("tabelascargas10")
          .querySelectorAll('input[type="checkbox"][name=peso]');
        for (var checkbox of checkboxes) {
          checkbox.checked = this.checked;
        }
      };

      $(".copy-data").on("click", function () {
        const t = 800;
        const t1 = 400;
        const t2 = 990;

        const valueeeee = $(this).attr("data-clipboard-text");
        var elementtextadv = document.getElementById("cargasmotcopy");
        elementtextadv.innerHTML = valueeeee;
        $("#clickeadvise").slideToggle(t1).delay(t2).slideToggle(t);
      });
    },
  });
}

///////////////////JS AJAX PEDIDOS/////////////////////////////////////////////

setInterval(function () {
  refreshTabelaPedidos();
}, 960000); // 16 Minutos
function refreshTabelaPedidos() {
  $("#lock-refresh-pedidos")
    .addClass("fa-spin")
    .delay(120000)
    .queue("fx", function () {
      $(this).removeClass("fa-spin");
    });
  // Whatever here.
  $.ajax({
    url: urlpedido,
    beforeSend: function () {
      $("#wait").show();
    },
    complete: function () {
      $("#wait").hide();
    },
    success: function (data) {
      document.getElementById("ajaxpedidos").innerHTML = data;
      $(document).ready(function () {
        $("#dtBasicExample").DataTable({
          order: [[1, "asc"]],
        });
        $(".dataTables_length").addClass("bs-select");
      });

      $(".simplehighlight2").click(function () {
        $(this).toggleClass("clicked");
      });

      $("#dtBasicExample")
        .find("input:checkbox")
        .on("change", function () {
          //Atribui o valor do input p/ variável 'valor'

          var total = 0;
          $("#dtBasicExample")
            .find(":checkbox")
            .each(function () {
              if ($(this).is(":checked")) {
                total = total + parseInt($(this).val());
              }
            });
          var total1 = total.toLocaleString("pt-BR");

          if (total1 == 0) {
            $("#pedidossaldos").val("Peso em Kg");
          } else {
            $("#pedidossaldos").val(total1);
          }
        });

      document.getElementById("select-all-carregado").onclick = function () {
        var checkboxes = document
          .getElementById("pedidos10")
          .querySelectorAll('input[type="checkbox"][name=carregado]');
        for (var checkbox of checkboxes) {
          checkbox.checked = this.checked;
        }
      };

      document.getElementById("select-all-saldo").onclick = function () {
        var checkboxes = document
          .getElementById("pedidos10")
          .querySelectorAll('input[type="checkbox"][name=saldo]');
        for (var checkbox of checkboxes) {
          checkbox.checked = this.checked;
        }
      };

      document.getElementById("select-all-previsto").onclick = function () {
        var checkboxes = document
          .getElementById("pedidos10")
          .querySelectorAll('input[type="checkbox"][name=previsto]');
        for (var checkbox of checkboxes) {
          checkbox.checked = this.checked;
        }
      };

      document.getElementById("select-all-saldoprevisto").onclick =
        function () {
          var checkboxes = document
            .getElementById("pedidos10")
            .querySelectorAll('input[type="checkbox"][name=saldoprevisto]');
          for (var checkbox of checkboxes) {
            checkbox.checked = this.checked;
          }
        };
    },
  });
}

new ClipboardJS(".copy-data");
///////////////////INICIAR CARREGAMENTO AJAX DE TODAS/////////////////////////////////////////////

setInterval(refreshTabelaCargas(), 100);
setInterval(refreshTabelaPedidos(), 100);
setInterval(refreshTabelasDashboard(), 100);
