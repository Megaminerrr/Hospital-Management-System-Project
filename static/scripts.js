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
    let columns = [];
    switch(type){
    case "Treatments":
        columns = [
            {key: "Treatment_ID", label: "ID"},
            {key: "Medicine", label: "Medicine"},
            {key: "Perscription", label: "Perscription"}
        ];
        fetch("http://127.0.0.1:5000/api/treatments")
            .then(r => r.json())
            .then(data => buildTable(columns, data));

	break;
    case "Rooms":
        columns = [
            {key: "Room_ID", label: "ID"},
            {key: "Appt_ID", label: "Appointment ID"},
            {key: "room_type", label: "Type"}
        ];
        fetch("http://127.0.0.1:5000/api/rooms")
            .then(r => r.json())
            .then(data => buildTable(columns, data));
	break;
    case "Appointments":
        columns = [
            {key: "Appt_ID", label: "ID"},
            {key: "Doctor_ID", label: "Doctor"},
            {key: "Patient_ID", label: "Patient"},
            {key: "Date", label: "Date"},
            {key: "Time", label: "Time"}
        ];
        fetch("http://127.0.0.1:5000/api/appointments")
            .then(r => r.json())
            .then(data => buildTable(columns, data));
	break;
    case "Doctors":
        columns = [
            {key: "Doctor_ID", label: "ID"},
            {key: "First_Name", label: "First Name"},
            {key: "Last_Name", label: "Last Name"},
            {key: "Specialization", label: "Specialization"}
        ];
        fetch("http://127.0.0.1:5000/api/doctors")
            .then(r => r.json())
            .then(data => buildTable(columns, data));
	break;
    case "Patients":
	columns = [
	    {key: "Patient_ID", label: "ID"},
	    {key: "First_Name", label: "First Name"},
	    {key: "Last_Name", label: "Last Name"}
	];
	fetch("http://127.0.0.1:5000/api/patients")
	    .then(r => r.json())
	    .then(data => buildTable(columns, data));
	break;
    case "logs":

	break;
    }

}

class AppTopbar extends HTMLElement {
    connectedCallback() {
      this.innerHTML = `
        <div class="topbar">
          <div class="topbar_logo"><h1>Title</h1></div>
          <div class="topbar_elements">
            <div class="dropdown">
              <button class="btn_dropdown"></button>
              <div class="dropdown-content">
                <a href="/home">Home Page</a>
                <button class="btn_login" onclick="window.location.href='/logout'">Log Out</button>
              </div>
            </div>
          </div>
        </div>`;
    }
  }
  customElements.define('app-topbar', AppTopbar);