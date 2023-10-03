import datajoint as dj

from . import db_prefix

schema = dj.Schema(db_prefix + "reference")


@schema
class Device(dj.Lookup):
    definition = """
    device_id           : smallint
    ---
    device_name         : varchar(32)  # user-friendly name of the device
    device_description  : varchar(256)
    """
