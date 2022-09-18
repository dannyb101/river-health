function hideTextIfTyping(element_id, text_id){
    document.getElementById(element_id).addEventListener('keyup', () => {
      document.getElementById(text_id).classList.add('invisible')
    })
}

hideTextIfTyping("river_flow_ls", "autopopulated_from_flow")
hideTextIfTyping("river_flow_ls_sd", "autopopulated_from_flow")
hideTextIfTyping("river_bod_mgl", "autopopulated_from_bod")
hideTextIfTyping("river_bod_mgl_sd", "autopopulated_from_bod")
hideTextIfTyping("river_nh3_mgl", "autopopulated_from_nh3")
hideTextIfTyping("river_nh3_mgl_sd", "autopopulated_from_nh3")

//Start river stretch dropdown

// Show river stretch dropdown
function showRiverStretches(){
    document.getElementById('stretch_list_container').style.display='block';
  }
  
  // Hide river stretch dropdown
  function hideRiverStretches(){
    document.getElementById('stretch_list_container').style.display='none';
  }
  
  function delayedHideRiverStretches(){
    setTimeout(hideRiverStretches, 300);
  }
  
  // Populate stretch name input by clicking item in dropdown
  function populateStretchName(listItem){
    let stretch_name = listItem.innerText;
    document.getElementById('river_stretch_name').value = stretch_name;
    document.getElementById('stretch_list_container').style.display='none'; 
  }

    // Filter dropdown results by typing
    document.getElementById('river_stretch_name').addEventListener('keyup', () => {
  
      let userInput = document.getElementById('river_stretch_name').value.toLowerCase()
      let listOfRiverStretchs = document.getElementById("river_stretches").getElementsByTagName('li')
    
      for (i = 0; i < listOfRiverStretchs.length; i++) {
        riverStretch = listOfRiverStretchs[i]
        riverStretchValue = riverStretch.textContent || riverStretch.innerText
    
        if (riverStretchValue.toLowerCase().indexOf(userInput) > -1) {
          riverStretch.style.display = "";
        } else {
          riverStretch.style.display = "none";
        }
      }
    })
 
//End river stretch dropdown

// Start nrfa dropdown

  // Show nrfa station dropdown
  function showNRFAStations(){
    document.getElementById('nrfa_station_stretch_list_container').style.display='block';
  }
  
  // Hide nrfa station dropdown
  function hideNRFAStations(){
    document.getElementById('nrfa_station_stretch_list_container').style.display='none';
  }
  
  function delayedHideNRFAStations(){
    setTimeout(hideNRFAStations, 300);
  }
  
  // Populate nrfa station input by clicking item in dropdown
  function populateNRFAStation(listItem){
    let NRFAStationSelected = listItem.innerText;
    document.getElementById('nrfa_station').value = NRFAStationSelected;
    getFlowDataByNRFAStationId(listItem.id);
    document.getElementById('nrfa_station_id').value = listItem.id;
    document.getElementById('nrfa_station_stretch_list_container').style.display='none'; 
  }
  
  // Filter dropdown results by typing
  document.getElementById('nrfa_station').addEventListener('keyup', () => {
  
    let userNRFAStationInput = document.getElementById('nrfa_station').value.toLowerCase()
    let listOfNRFAStations = document.getElementById("nrfa_stations").getElementsByTagName('li')
  
    for (i = 0; i < listOfNRFAStations.length; i++) {
      NRFAStation = listOfNRFAStations[i]
      NRFAStationValue = NRFAStation.textContent || NRFAStation.innerText
  
      if (NRFAStationValue.toLowerCase().indexOf(userNRFAStationInput) > -1) {
        NRFAStation.style.display = "";
      } else {
        NRFAStation.style.display = "none";
      }
    }
  })
  
  function getFlowDataByNRFAStationId(id){

    const numYears = document.getElementById('num_years').value;
  
    var query_server = "/nrfa/mean_and_sd_flow" + "?station_id=" + id + "&num_years=" + numYears;
  
    let xhttp = new XMLHttpRequest();
    xhttp.open("GET", query_server, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  
    xhttp.onreadystatechange = function () {
  
      if (xhttp.readyState == 4) {
  
          if (xhttp.status === 200) {
  
            const mean_and_sd_json = JSON.parse(xhttp.responseText);
            document.getElementById('river_flow_ls').value = (mean_and_sd_json.river_flow_ls).toFixed(2);
            document.getElementById('river_flow_ls_sd').value = (mean_and_sd_json.river_flow_ls_sd).toFixed(2);

            document.getElementById('autopopulated_from_flow').innerHTML = "Flow rate autopopulated from NRFA API data"
            document.getElementById('autopopulated_from_flow').classList.remove('invisible')
  
          } else {
              alert("Error getting mean and s.d. from NRFA API. Dates may be out of range. Please enter values manually.")
              console.error(xhttp.statusText);
          }
  
      }
  
    }
  
  xhttp.send();
  
  }
  
  // ----- END OF JAVASCRIPT FOR STATIONS ----- //

// End nrfa dropdown

//Start previous calcs dropdown

function showPreviousSimulations(){
    document.getElementById('prev_calcs_container').style.display='block';
  }
  
  // Hide list of previous simulations dropdown
function hidePrevCalcs(){
    document.getElementById('prev_calcs_container').style.display='none';
  }
  
function delayedHidePreviousSimulations(){
    setTimeout(hidePrevCalcs, 300);
  }
  
  // Populate list of previous simulations box by clicking item in dropdown
  //List is populated with newest simulations at the top, as these are the ones
  //most likely to be used in serialisation
function populatePreviousSimulations(listItem){
    let name_of_simulation = listItem.innerText;
    document.getElementById('description_of_simulation').value = name_of_simulation;
    //adding the value of mean and sd to the input boxes depending on chosen id
    document.getElementById('river_flow_ls').value = listItem.getAttribute('data-flow-mean');
    document.getElementById('river_flow_ls_sd').value = listItem.getAttribute('data-flow-sd');
    //signalling to the user where the input details are from
    document.getElementById('autopopulated_from_flow').innerHTML = "Flow rate autopopulated from a previous simulation"
    document.getElementById('autopopulated_from_flow').classList.remove('invisible')
    //adding the value of mean and sd to the input boxes depending on chosen id
    document.getElementById('river_bod_mgl').value = listItem.getAttribute('data-bod-mean');
    document.getElementById('river_bod_mgl_sd').value = listItem.getAttribute('data-bod-sd');
    //signalling to the user where the input details are from
    document.getElementById('autopopulated_from_bod').innerHTML = "BOD autopopulated from a previous simulation"
    document.getElementById('autopopulated_from_bod').classList.remove('invisible')
    //adding the value of mean and sd to the input boxes depending on chosen id
    document.getElementById('river_nh3_mgl').value = listItem.getAttribute('data-nh3-mean');
    document.getElementById('river_nh3_mgl_sd').value = listItem.getAttribute('data-nh3-sd');
    //signalling to the user where the input details are from
    document.getElementById('autopopulated_from_nh3').innerHTML = "NH3 autopopulated from a previous simulation"
    document.getElementById('autopopulated_from_nh3').classList.remove('invisible')
    document.getElementById('prev_calcs_container').style.display='none'; 

  }

  // hide the list of previous simulations when the user clicks outside of it
  document.addEventListener('click', (event) => {
    let box = document.getElementById('prev_calcs_container');
    if(!box.contains(event.target) && !document.getElementById('description_of_simulation').contains(event.target)){
      box.style.display = 'none';
    }
  })

//End previous calcs dropdown
  