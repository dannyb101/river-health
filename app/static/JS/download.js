function htmlToCSV(filename) {
	let data = [];
	let rows = document.querySelectorAll("table tr");

	for (let i = 0; i < rows.length; i++) {
		let row = [], cols = rows[i].querySelectorAll("td, th");
				
		for (let j = 0; j < cols.length; j++) {
			if (cols[j].innerText == "Total Spill Discharge"){
				row.push("\n");
				row.push(" ");
				row.push(cols[j].innerText);
			} else if (cols[j].innerText == "Upstream River" || cols[j].innerText == "Initial Mixed River") {
				row.push(",");
				row.push(cols[j].innerText);
			} else if (cols[j].innerText == "BOD results" || cols[j].innerText == "Ammonia results"){
				row.push("\n");
				row.push(cols[j].innerText);
			} else {
				row.push(cols[j].innerText);
			}
        }
		        
		data.push(row.join(",")); 		
	}

	downloadCSVFile(data.join("\n"), filename);
}

function downloadCSVFile(csv, filename) {
	let csv_file, download_link;

	csv_file = new Blob([csv], {type: "text/csv"});

	download_link = document.createElement("a");

	download_link.download = filename;

	download_link.href = window.URL.createObjectURL(csv_file);

	download_link.style.display = "none";

	document.body.appendChild(download_link);

	download_link.click();
}

function click_download_button(filename){
    document.getElementById("download-button")
	htmlToCSV(filename);
}

const inputNames = {
	archive_id: 'Calculation ID',
	cso_bod_conc_mgl:"CSO BOD Concentration (mg/L)",
	cso_id: 'CSO ID', 
	cso_nh3_conc_mgl: "CSO NH3 Concentration (mg/L)",
	depth_exponent:  "Depth Exponent",
	num_sims: "Number of Monte Carlo Simulations",
	num_years: "Number of Years of Data",
	reaeration_constant: "Re-aearation Constant",
	river_bedwidth_m: "Bed Width (m)",
	river_bod_decay_rate_day: "BOD Decay Rate (1/day)",
	river_bod_mgl: "BOD Conc. Mean (mg/L)",
	river_bod_mgl_sd: "BOD Conc. SD (mg/L)",
	river_do_conc_mgl: "DO Conc. Mean (mg/L)",
	river_do_conc_mgl_sd: "DO Conc. SD (mg/L)",
	river_flow_ls: "Flow Rate Mean (l/s)",
	river_flow_ls_sd: "Flow Rate SD (l/s)",
	river_length_stretch_m: "Length (m)",
	river_longslope_m_m: "Long Slope (m/m)",
	river_mannings_no: "Mannings No.",
	river_nh3_decay_rate_day: "NH3 Decay Rate (1/day)",
	river_nh3_gain_bod_gN_gO2: "NH3 Gain From BOD Decay (gN/gO2)",
	river_nh3_mgl: "NH3 Conc. Mean (mg/L)",
	river_nh3_mgl_sd: "NH3 Conc. SD (mg/L)",
	river_nh3_yield_factor_gN_gO2: "NH3 Yield Factor (gO2/gN)",
	river_ph: "pH Mean",
	river_ph_sd: "pH SD",
	river_sideslope_m_m:  "Slide Slope (m/m)",
	river_stretch_name: "River Stretch Name", 
	river_temp_celcius: "Temp Mean (degC)", 
	river_temp_celcius_sd: "Temp SD (degC)",
	river_type: "River Type",
	sim_datetime : "Calculation Datetime",
	velocity_exponent: "Velocity Exponent"
}

function convertInputsToCSV(inputObject, valueNames) {
	/* input river stretch name at top of csv for ease of reference by usern
	(all other variables will be in alphabetical order due to using JSON.parse on python dictionary) */
    let csvOutput = 'Input, Value\n';
	csvOutput += valueNames['river_stretch_name'] + ',' + inputObject['river_stretch_name'] + '\n'; 
	for (let key in inputObject) {
		if (key != 'river_stretch_name'){
			if (key in valueNames){
				csvOutput += valueNames[key] + ',' + inputObject[key] + '\n';
			} else {
				csvOutput += key + ',' + inputObject[key] + '\n';
			}
		}
	}
	return csvOutput;
}

function downloadInputs(filename){
	const inputs = {
		... inputData,
		... csoInputData
	}
	let csv = convertInputsToCSV(inputs, inputNames);
	downloadCSVFile(csv, filename);
}