"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
from typing import Union
from pathlib import Path
from threading import RLock, Lock
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion[Constants]


PATH_TYPE = Union[str, os.PathLike, Path]

LOCK_TYPE = Union[type[Lock], type[RLock]]

# region[Main_Exec]

if __name__ == '__main__':
    pass

# endregion[Main_Exec]
