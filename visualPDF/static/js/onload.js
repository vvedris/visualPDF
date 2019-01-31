function AddAttr(){
  document.getElementById("id_Q2").setAttribute("min","0.1");
  document.getElementById("id_Q2").setAttribute("max","10000000000");
  document.getElementById("id_xmin").setAttribute("min","0.0000000001");
  document.getElementById("id_xmin").setAttribute("max","1");
  document.getElementById("id_xmax").setAttribute("min","0.0000000001");
  document.getElementById("id_xmax").setAttribute("max","1");
};

window.onload = AddAttr;
