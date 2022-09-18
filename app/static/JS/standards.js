function scrapeNRFA(){

    console.log("scrapeNFRA function called")

    let xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/nrfa/add", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhttp.onreadystatechange = function () {

        console.log("xhttp state changed.")

        if (xhttp.readyState == 4) {

            if (xhttp.status === 200) {

                alert("NRFA API successfully updated stations!")
            } else {
                alert("You ran into an error updating the stations via the NRFA API.")
                console.error(xhttp.statusText);
            }

        }

    }

    xhttp.send();

}