from flask import Blueprint, render_template, request
from ..Connections.db_standards import DB_WFD_STANDARDS

standards = Blueprint("standards", __name__)


@standards.route("/standards/", methods=["GET", "POST"])
def standards_route():
    connection = DB_WFD_STANDARDS()
    if request.method == "POST":
        # convert form data to dictionary and cast values to float
        standards_dict = {k: float(v) for (k, v) in dict(request.form).items()}
        if 'user' not in standards_dict:

            standards_dict['user'] = 'unknown'
        # get db values from form item names and send to db
        list_of_standards = []
        for key in standards_dict:
            if key == 'user':
                continue
            split_key = key.split("_")
            river_type = "_".join([str(i) for i in split_key[0:-2]])
            standard = split_key[-1]
            pollutant = split_key[-2]
            concentration = standards_dict[key]
            list_of_standards.append([river_type, standard, pollutant, concentration])
        connection.insert_standards(list_of_standards, standards_dict['user'])

    # get standards from db and concatenate values to create form item names
    # in the format: river-type_pollutant_standard e.g. 1_2_4_6_high_bod
    db_standards_list = connection.get_all_standards()
    db_standards_dict = { "_".join(i[0:3]) : i[3] for i in db_standards_list}

    return render_template("standards.html", standards=db_standards_dict)

