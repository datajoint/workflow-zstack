from element_interface.utils import ingest_csv_to_table

from .pipeline import session, subject


def ingest_subjects(
    subject_csv_path: str = "./user_data/subjects.csv",
    skip_duplicates: bool = True,
    verbose: bool = True,
):
    """Inserts ./user_data/subject.csv data into corresponding subject schema tables

    Args:
        subject_csv_path (str): relative path of subject csv
        skip_duplicates (bool): Default True. Passed to DataJoint insert
        verbose (bool): Display number of entries inserted when ingesting
    """
    csvs = [subject_csv_path]
    tables = [subject.Subject()]
    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


def ingest_sessions(
    session_csv_path: str = "./user_data/sessions.csv",
    skip_duplicates: bool = True,
    verbose: bool = True,
):
    """
    Inserts data from a sessions csv into corresponding session schema tables
    By default, uses data from workflow_session/user_data/session/
        session_csv_path (str): relative path of session csv
        skip_duplicates (bool): Default True. See DataJoint `insert` function
        verbose (bool): Print number inserted (i.e., table length change)
    """
    csvs = [
        session_csv_path,
        session_csv_path,
    ]
    tables = [
        session.Session(),
        session.SessionDirectory(),
    ]

    ingest_csv_to_table(csvs, tables, skip_duplicates=skip_duplicates, verbose=verbose)


if __name__ == "__main__":
    ingest_sessions()
