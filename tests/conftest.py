import logging
import os
import pathlib
from contextlib import nullcontext
from pathlib import Path

import datajoint as dj
import pytest
from element_interface.utils import QuietStdOut, find_full_path, value_to_bool

from workflow_volume.ingest import ingest_sessions
from workflow_volume.paths import get_vol_root_data_dir

# ------------------- SOME CONSTANTS -------------------


logger = logging.getLogger("datajoint")

pathlib.Path("./tests/user_data").mkdir(exist_ok=True)
pathlib.Path("./tests/user_data/lab").mkdir(exist_ok=True)

sessions_dirs = [
    "subject1/session1",
    "subject2/session1",
    "subject2/session2",
    "subject3/session1",
    "subject4/experiment1",
    "subject5/session1",
    "subject6/session1",
]


def pytest_addoption(parser):
    """
    Permit constants when calling pytest at command line e.g., pytest --dj-verbose False

    Arguments:
        --dj-verbose (bool):  Default True. Pass print statements from Elements.
        --dj-teardown (bool): Default True. Delete pipeline on close.
        --dj-datadir (str):  Default ./tests/user_data. Relative path of test CSV data.
    """
    parser.addoption(
        "--dj-verbose",
        action="store",
        default="True",
        help="Verbose for dj items: True or False",
        choices=("True", "False"),
    )
    parser.addoption(
        "--dj-teardown",
        action="store",
        default="True",
        help="Verbose for dj items: True or False",
        choices=("True", "False"),
    )
    parser.addoption(
        "--dj-datadir",
        action="store",
        default="./tests/user_data",
        help="Relative path for saving tests data",
    )


@pytest.fixture(autouse=True, scope="session")
def setup(request):
    """Take passed commandline variables, set as global"""
    global verbose, _tear_down, test_user_data_dir, verbose_context

    verbose = value_to_bool(request.config.getoption("--dj-verbose"))
    _tear_down = value_to_bool(request.config.getoption("--dj-teardown"))
    test_user_data_dir = Path(request.config.getoption("--dj-datadir"))
    test_user_data_dir.mkdir(exist_ok=True)

    if not verbose:
        logging.getLogger("datajoint").setLevel(logging.CRITICAL)

    verbose_context = nullcontext() if verbose else QuietStdOut()

    yield verbose_context, verbose


# --------------------  HELPER CLASS --------------------


def null_function(*args, **kwargs):
    pass


# ---------------------- FIXTURES ----------------------


@pytest.fixture(autouse=True, scope="session")
def dj_config(setup):
    """If dj_local_config exists, load"""
    if pathlib.Path("./dj_local_conf.json").exists():
        dj.config.load("./dj_local_conf.json")
    dj.config.update(
        {
            "safemode": False,
            "database.host": os.environ.get("DJ_HOST") or dj.config["database.host"],
            "database.password": os.environ.get("DJ_PASS")
            or dj.config["database.password"],
            "database.user": os.environ.get("DJ_USER") or dj.config["database.user"],
            "custom": {
                "ephys_mode": (
                    os.environ.get("EPHYS_MODE") or dj.config["custom"]["ephys_mode"]
                ),
                "database.prefix": (
                    os.environ.get("DATABASE_PREFIX")
                    or dj.config["custom"]["database.prefix"]
                ),
                "ephys_root_data_dir": (
                    os.environ.get("EPHYS_ROOT_DATA_DIR").split(",")
                    if os.environ.get("EPHYS_ROOT_DATA_DIR")
                    else dj.config["custom"]["ephys_root_data_dir"]
                ),
            },
        }
    )
    return


@pytest.fixture(autouse=True, scope="session")
def test_data(dj_config):
    """If data does not exist or partial data is present,
    attempt download with DJArchive to the first listed root directory"""
    test_data_exists = True

    for p in sessions_dirs:
        try:
            find_full_path(get_vol_root_data_dir(), p)
        except FileNotFoundError:
            test_data_exists = False  # If data not found
            break

    if not test_data_exists:  # attempt to djArchive dowload
        try:
            dj.config["custom"].update(
                {
                    "djarchive.client.endpoint": os.environ[
                        "DJARCHIVE_CLIENT_ENDPOINT"
                    ],
                    "djarchive.client.bucket": os.environ["DJARCHIVE_CLIENT_BUCKET"],
                    "djarchive.client.access_key": os.environ[
                        "DJARCHIVE_CLIENT_ACCESSKEY"
                    ],
                    "djarchive.client.secret_key": os.environ[
                        "DJARCHIVE_CLIENT_SECRETKEY"
                    ],
                }
            )
        except KeyError as e:
            raise FileNotFoundError(
                "Full test data not available.\nAttempting to download from DJArchive,"
                + " but no credentials found in environment variables.\nError:"
                + str(e)
            )

        import djarchive_client

        client = djarchive_client.client()

        test_data_dir = get_vol_root_data_dir()
        if isinstance(test_data_dir, list):  # if multiple root dirs, first
            test_data_dir = test_data_dir[0]

        client.download(
            "workflow-array-ephys-benchmark",
            "v2",
            str(test_data_dir),
            create_target=False,
        )
    return


@pytest.fixture(autouse=True, scope="session")
def pipeline():
    from workflow_volume import pipeline

    yield {
        "subject": pipeline.subject,
        "lab": pipeline.lab,
        "ephys": pipeline.ephys,
        "probe": pipeline.probe,
        "ephys_report": pipeline.ephys_report,
        "session": pipeline.session,
        "get_vol_root_data_dir": pipeline.get_vol_root_data_dir,
        "ephys_mode": pipeline.ephys_mode,
    }

    if _tear_down:
        with verbose_context:
            pipeline.subject.Subject.delete()


@pytest.fixture(scope="session")
def ingest_data(setup, pipeline, test_data):
    """For each input, generates csv in test_user_data_dir and ingests in schema"""
    # CSV as list of 3: filename, relevant tables, content
    all_csvs = {
        "file.csv": {
            "func": null_function,
            "args": {},
            "content": ["header,one,two", "info,a,b"],
        },
        "session.csv": {
            "func": ingest_sessions,
            "args": {},
            "content": ["header,one,two", "info,a,b"],
        },
    }
    # If data in last table, presume didn't tear down last time, skip insert
    if len(pipeline["ephys"].Clustering()) == 0:
        for csv_filename, csv_dict in all_csvs.items():
            csv_path = test_user_data_dir / csv_filename  # add prefix for rel path
            Path(csv_path).write_text("\n".join(csv_dict["content"]) + "\n")
            csv_dict["func"](verbose=verbose, skip_duplicates=True, **csv_dict["args"])

    yield all_csvs

    if _tear_down:
        with verbose_context:
            for csv in all_csvs:
                csv_path = test_user_data_dir / csv
                csv_path.unlink()
