# Copyright 2021 VicEdTools authors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Executable script for exporting student details from OARS."""

import json
import os

from vicedtools.acer.oars import OARSSession


def export_oars_students(school_code, authenticator, oars_dir):
    """Exports OARS student data and saves it in candidates.json.

    Args:
        school_code: An OARS school string. E.g. https://oars.acer.edu.au/{your school string}/...
        authenticator: An instance of OARSAuthenticator.
        oars_dir: The directory to save the candidate data in.
    """
    export_file = os.path.join(oars_dir, "candidates.json")

    s = OARSSession(school_code, authenticator)
    candidates = s.get_candidates()
    with open(export_file, 'w') as f:
        json.dump(candidates, f)


if __name__ == "__main__":
    from config import (oars_dir, oars_authenticator, oars_school_code)

    if not os.path.exists(oars_dir):
        os.makedirs(oars_dir)

    export_oars_students(oars_school_code, oars_authenticator, oars_dir)
