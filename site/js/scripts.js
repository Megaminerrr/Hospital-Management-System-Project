function isAlpha(c) {
    return /^[A-Za-z]$/.test(c);
}
function isNumeric(c) {
    return /^[0-9]$/.test(c);
}

function CleanString(str){
    let cleanedStr = "";
    for (let i = 0; i < str.length; i++) {
	let c = str[i];
	if( isAlpha(c) || isNumeric(c) || c == ' '){
	    cleanedStr += c;
	}
    }
    return cleanedStr;
}

function filterList() {
    let input = CleanString(document.getElementById("searchInput").value.toLowerCase());
    let items = document.querySelectorAll(".list-box .item");

  items.forEach(item => {
    item.style.display = item.textContent.toLowerCase().includes(input)
      ? "block"
      : "none";
  });
}

function buildTable(columns, data) {
    const header = document.getElementById("tableHeader");
    const body = document.getElementById("tableBody");

    header.innerHTML = "";
    body.innerHTML = "";

    columns.forEach(col => {
        const th = document.createElement("th");
        th.textContent = col.label;
        header.appendChild(th);
    });

    data.forEach(row => {
        const tr = document.createElement("tr");

        columns.forEach(col => {
            const td = document.createElement("td");
            td.textContent = row[col.key] ?? "";
            tr.appendChild(td);
        });

        body.appendChild(tr);
    });
}

function DisplayRecords(type){
    const columns;
    switch(type){
    case "Treatments":

	break;
    case "Rooms":

	break;
    case "Appointments":
	
	break;
    case "Doctors":
	
	break;
    case "Patients":
	columns = [
	    {key: "Patient_ID", label: "ID"},
	    {key: "First_Name", label: "First Name"},
	    {key: "Last_Name", label: "Last Name"}
	];
	fetch("http://127.0.0.1:5000/patient/appointments")
	    .then(r => r.json())
	    .then(data => buildTable(columns, data));
	break;
    case "logs":

	break;
    }

}
