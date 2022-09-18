from flask import Blueprint, render_template
from ..Connections.db_archive import DB_ARCHIVE

archive = Blueprint('archive', __name__)

# Route to defaults page
@archive.route('/archive/', methods=['GET'])
def archive_route():

    archive_conn = DB_ARCHIVE()

    # Check that there are previous calculations and display error page if not
    if archive_conn.get_most_recent_id() == 0:
        return render_template('archive-empty.html', active_page='archive')

    archives = archive_conn.get_all_archive_results()

    return render_template('archive.html', archives=archives)