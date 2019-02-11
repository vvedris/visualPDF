document.getElementById("id_id_fixed_0_2").addEventListener("click", fixedxq);
document.getElementById("id_id_fixed_0_1").addEventListener("click", fixedxq);

function fixedxq(){
  if (document.getElementById('id_id_fixed_0_2').checked){
    var x = document.getElementById('id_Q2');
    var xl = document.querySelectorAll("label[for='id_Q2']");
    var Q2min, Q2max, Q2maxl, Q2minl;

    xl[0].innerHTML = "X"
    x.value="0.1";
    x.setAttribute("min","0.0000000001");
    x.setAttribute("max","1");

    Q2minl = document.querySelectorAll("label[for='id_xmin']");
    Q2minl[0].innerHTML = "Q2min";
    Q2min = document.getElementById('id_xmin');
    Q2min.value="10";
    Q2min.setAttribute("min","0.1");
    Q2min.setAttribute("max","10000000000");

    Q2maxl = document.querySelectorAll("label[for='id_xmax']");
    Q2maxl[0].innerHTML = "Q2max"
    Q2max = document.getElementById('id_xmax');
    Q2max.value="100";
    Q2max.setAttribute("min","0.1");
    Q2max.setAttribute("max","10000000000");

  }
  else if(document.getElementById('id_id_fixed_0_1').checked){
    var Q = document.getElementById('id_Q2');
    var Ql = document.querySelectorAll("label[for='id_Q2']");
    var Xmin, Xmax, Xminl, Xmaxl;

    Ql[0].innerHTML = "Q2"
    Q.value="100";
    Q.setAttribute("min","0.1");
    Q.setAttribute("max","10000000000");

    Xminl = document.querySelectorAll("label[for='id_xmin']");
    Xminl[0].innerHTML = "Xmin";
    Xmin = document.getElementById('id_xmin');
    Xmin.value="0.0001";
    Xmin.setAttribute("min","0.0000000001");
    Xmin.setAttribute("max","1");

    Xmaxl = document.querySelectorAll("label[for='id_xmax']");
    Xmaxl[0].innerHTML = "Xmax"
    Xmax = document.getElementById('id_xmax');
    Xmax.value="1";
    Xmax.setAttribute("min","0.0000000001");
    Xmax.setAttribute("max","1");
  };
};
