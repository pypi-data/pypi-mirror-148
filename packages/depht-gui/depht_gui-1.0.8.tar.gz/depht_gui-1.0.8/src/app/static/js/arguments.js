/**Show optional arguments.*/
function show_optional(opt_id, show_id, hide_id) {
  opt = document.getElementById(opt_id);
  show = document.getElementById(show_id)
  hide = document.getElementById(hide_id)

  if(opt.style.display === "none" || opt.style.display == "") {
    opt.style.display = "block";
    show.style.display = "none";
    hide.style.display = "block";
  } else {
    opt.style.display = "none";
    show.style.display = "block";
    hide.style.display = "none";
  }
}


/**
* Get a list of number of cores.
*/
function get_core_list(cpu_cores) {
  select = document.getElementById("cores");

  for(let i = 1; i <= cpu_cores; i++) {
    var option = document.createElement("option");
    option.text = option.value = i;

    if(i == cpu_cores/2) {
      option.selected = "selected";
    }

    select.add(option);
  }
}

function submit_form(submit_button_id) {
  submit_button = document.getElementById(submit_button_id)

  submit_button.value = "Loading...";
  submit_button.style.border = "2px solid red";
}
