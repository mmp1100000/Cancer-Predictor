function update_db(row) {
  console.log(row);
  table = document.getElementById("table");
  rows = table.rows;

  function setSelectedValue(selectObj, valueToSet) {
      for (var i = 0; i < selectObj.options.length; i++) {
          if (selectObj.options[i].text== valueToSet) {
              selectObj.options[i].selected = true;
              return;
          }
      }
  }
  current_rol =rows[row].getElementsByTagName("td")[3].innerHTML
  form_html = '<form onsubmit="myFunction(); return false;" id="selectorForm"><select id="rolSelect" onchange="this.form.submit();add_apply_button(' + row + ')"><option value="Doctor">Doctor</option><option value="Admin">Admin</option></select></form>';
  pos = form_html.indexOf(current_rol+'\"')+current_rol.length+1
  console.log([form_html.slice(0, pos), ' selected', form_html.slice(pos)].join(''))
  rows[row].getElementsByTagName("td")[3].innerHTML=[form_html.slice(0, pos), ' selected', form_html.slice(pos)].join('');

}

function add_apply_button(row){
    table = document.getElementById("table");
    rows = table.rows;
    selector=document.getElementById("rolSelect")


    function getSelectedOption(selector) {
        var opt;
        for ( var i = 0, len = selector.options.length; i < len; i++ ) {
            opt = selector.options[i];
            if ( opt.selected === true ) {
                break;
            }
        }
        return opt;
    }
    rows[row].getElementsByTagName("td")[5].innerHTML='<button type="button" onClick="return apply_change(\''+ row+'\',\'' + getSelectedOption(selector).value+ '\')">Apply</button>';
}


function apply_change(row,rol){
  table = document.getElementById("table");
  rows = table.rows;
  console.log(row)
  //console.log(rows[row].getElementsByTagName("td")[3].innerHTML)
  formBody={'uid':rows[row].getElementsByTagName("th")[0].innerHTML,'rol':rol}
  console.log(formBody)
// The rest of this code assumes you are not using a library.
// It can be made less wordy if you use one.
var form = document.createElement("form");
form.setAttribute("method", "post");
form.setAttribute("action", "/administration/user/edit");

for(var key in formBody) {
    if(formBody.hasOwnProperty(key)) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", formBody[key]);

        form.appendChild(hiddenField);
    }
}

document.body.appendChild(form);
form.submit();
}
