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
"""Executable script for exporting NAPLAN outcomes from VCAA data service."""

from __future__ import annotations

import argparse
import os

from vicedtools.naplan import DataserviceSession

if __name__ == "__main__":
    from config import (naplan_outcomes_dir, dataservice_authenticator)

    parser = argparse.ArgumentParser(
        description='Export NAPLAN outcomes from VCAA data service')
    parser.add_argument('years',
                        nargs='+',
                        type=int,
                        help='the years to export')
    args = parser.parse_args()

    if not os.path.exists(naplan_outcomes_dir):
        os.makedirs(naplan_outcomes_dir)

    s = DataserviceSession(dataservice_authenticator)

    for year in args.years:
        s.export_naplan(year, naplan_outcomes_dir)
