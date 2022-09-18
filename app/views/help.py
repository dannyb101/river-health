from flask import Blueprint, render_template

help = Blueprint('help', __name__)

# Route to defaults page
@help.route('/help/', methods=['GET'])
def help_route():
    return render_template('help.html')