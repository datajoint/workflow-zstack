import datajoint as dj

from . import db_prefix

schema = dj.Schema(db_prefix + "reference")


@schema
class Device(dj.Lookup):
    """Table for managing lab equipment.

    Attributes:
        device ( varchar(32) ): Device short name.
        modality ( varchar(64) ): Modality for which this device is used.
        description ( varchar(256) ): Optional. Description of device.
    """

    definition = """
    device             : varchar(32)
    ---
    modality           : varchar(64)
    description=null   : varchar(256)
    """
    contents = [
        ["scanner1", "calcium imaging", ""],
        ["scanner2", "calcium imaging", ""],
    ]
