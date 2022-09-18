from app.Connections import db_archive, db_serialised_inputs

def test_archive_id_matches_mixed_data_id():
    """
    GIVEN a database archive and mixed_data connection
    WHEN the method is called
    THEN check that the most recent id in the archives table matched the one in the mixed_outputs table
    """
    output_mixed_data_connection = db_serialised_inputs.DB_SERIALISED_INPUTS()
    archive_connection = db_archive.DB_ARCHIVE()
    recent_id = archive_connection.get_most_recent_id()

    if recent_id == 0:
        assert recent_id == 0
    else:
        archive_by_id = archive_connection.get_archive_by_id(recent_id)
        mixed_data_by_id = output_mixed_data_connection.get_mixed_results_by_id(recent_id)
        assert archive_by_id[0]['id'] == mixed_data_by_id[0]['id']