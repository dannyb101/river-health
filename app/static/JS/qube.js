//Function which takes the uploaded csv, takes the second column,
//and calculates its mean and standard deviation.
//These are then inserted to the HTML form as values
function calculateMeanSdFromQubeCsv(str) {
	const [arr, headers] = convertCsvToArray(str);
	//declaring variables
	let sum = 0;
	let sumVariance = 0;
	let riverFlowData = 0;
	//looping through second column of csv i.e. column with river flow
	for (let i = 0; i < arr.length; i++) {
		riverFlowData = arr[i].split(",")[1];
		//adding each river flow datapoint to the previous datapoints
		sum += parseFloat(riverFlowData);
	}
	let riverFlowMean = sum / arr.length;
	//standard deviation calculation
	for (let i = 0; i < arr.length; i++) {
		riverFlowData = arr[i].split(",")[1];
		let variance = Math.pow(riverFlowMean - riverFlowData, 2);
		sumVariance += parseFloat(variance);
	}
	let meanVariance = sumVariance / arr.length;
	let riverFlowSD = Math.sqrt(meanVariance);

  //inserted calculated numbers as form values
  document.getElementById('river_flow_ls').value = (riverFlowMean*1000).toFixed(3);
  document.getElementById('river_flow_ls_sd').value = (riverFlowSD*1000).toFixed(3);
  //signalling to the user where the input details are from
  document.getElementById('autopopulated_from_flow').innerHTML = "Flow rate autopopulated from a QUBE csv file"
  document.getElementById('autopopulated_from_flow').classList.remove('invisible')
}

//The above function is run, when the QUBE river csv is uploaded
const csvUploadListener = (file_upload) => {
	const myFormInside = document.getElementById(file_upload);

	//ensuring above function happens on uploading qube csv
	myFormInside.onchange = function (e) {
		e.preventDefault();
		var input = myFormInside.files[0];
		const reader = new FileReader();

		reader.onload = function (e) {
			const text = e.target.result;
			if (file_upload == "qube_csv") {
				const data = calculateMeanSdFromQubeCsv(text);
				JSON.stringify(data);
			} else if (file_upload == "cso_csv") {
				const data = generateCsoInputs(text);
			}
		};
		reader.readAsText(input);
	};
};

const generateCsoInputs = (csv) => {
	const [arr, headers] = convertCsvToArray(csv);
  let numCsos
	if (
		headers.some((element) => {
			return element.toLowerCase() === "seconds";
		})
	) {
    numCsos = headers.length - 2;
		console.log("Headers includes seconds");
	} else {
    numCsos = headers.length - 1;
		console.log("Headers does not include seconds");
	}
  
  const inputHtml = getInputHtml(numCsos);
  const csoCardElement = document.getElementById("cso_card");
  const div = document.createElement("div");
  
  removePreviousChildren(csoCardElement);
  
  div.innerHTML = inputHtml;
  while (div.children.length > 0) {
    csoCardElement.appendChild(div.children[0]);
  }
};

const convertCsvToArray = (str) => {
	const delimiter = ",";
	//splitting csv data
	const arr = str.slice(str.indexOf("\n") + 1).split("\n");
	//separating headers from data
	const headers = str.slice(0, str.indexOf("\n")).split(delimiter);
	return [arr, headers];
};

const removePreviousChildren = (parent) => {
  console.log(parent.children.length);
  while (parent.children.length > 1) {
    parent.removeChild(parent.lastChild);
  }
}

const getInputHtml = (numCsos) => {
  const bodDefaultValue = defaults.cso_bod_conc_mgl
  const nh3DefaultValue = defaults.cso_nh3_conc_mgl
  
  let inputHtml = "";
  for (let i = 1; i <= numCsos; i++) {
    inputHtml += `
    <div class="d-flex flex-row"  style="text-align: left;">
    <div class="form-group p-2 col-sm-6 text-align-center">
  
    <label for="cso_id_${i}">ID</label>
      <div class="col-sm-12 input-group">
        <span class="input-group-text">CSO ${i}</span>
        <input
          type="text"
          id="cso_id_${i}"
          name="cso_id_${i}"
          class="form-control"
          required
          placeholder="e.g. usk001"
        />
      </div>


      
    </div>

      <div class="form-group p-2 col-sm-3">
        <label for="cso_bod_conc_mgl_1">BOD conc.</label>
        <div class="input-group">
          <input
            type="text"
            id="cso_bod_conc_mgl_${i}"
            name="cso_bod_conc_mgl_${i}"
            value="${bodDefaultValue}"
            class="no_negs_no_commas_regex form-control"
            required
          />
          <span class="input-group-text units"> mg/l </span>
        </div>
      </div>

      <div class="form-group p-2 col-sm-3">
        <label for="cso_nh3_conc_mgl_${i}">NH<sub>3</sub> conc.</label>
        <div class="input-group">
          <input
            type="text"
            id="cso_nh3_conc_mgl_${i}"
            name="cso_nh3_conc_mgl_${i}"
            value="${nh3DefaultValue}"
            class="no_negs_no_commas_regex form-control"
            required
          />
          <span class="input-group-text units"> mg/l </span>
        </div>
      </div>

  </div>`
  }
  return inputHtml;
}

window.onload = csvUploadListener("qube_csv");
window.onload = csvUploadListener("cso_csv");
