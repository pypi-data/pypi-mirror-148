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
"""Executable script for exporting Compass reports data."""

from __future__ import annotations

import argparse
import json
import os

from vicedtools.compass import CompassSession, get_report_cycle_id

if __name__ == "__main__":
    from config import (root_dir, compass_folder, reports_folder,
                        compass_authenticator, compass_school_code,
                        report_cycles_json)

    parser = argparse.ArgumentParser(
        description='Export all Compass progress reports.')
    parser.add_argument('--forceall',
                        '-a',
                        action="store_true",
                        help='force re-download existing reports')
    parser.add_argument('--forcerecent',
                        '-r',
                        action="store_true",
                        help='force re-download most recent report')
    args = parser.parse_args()

    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"{root_dir} does not exist as root directory.")
    if not os.path.isdir(root_dir):
        raise NotADirectoryError(f"{root_dir} is not a directory.")
    compass_dir = os.path.join(root_dir, compass_folder)
    if not os.path.exists(compass_dir):
        os.mkdir(compass_dir)
    reports_dir = os.path.join(compass_dir, reports_folder)
    if not os.path.exists(reports_dir):
        os.mkdir(reports_dir)

    report_cycles_file = os.path.join(compass_dir, report_cycles_json)
    with open(report_cycles_file, 'r', encoding='utf-8') as f:
        cycles = json.load(f)

    s = CompassSession(compass_school_code, compass_authenticator)

    for i in range(len(cycles)):
        cycle = cycles[i]
        file_name = os.path.join(
            reports_dir, f"SemesterReports-{cycle['year']}-{cycle['name']}.csv")
        if (not os.path.exists(file_name) or args.forceall or
            (args.forcerecent and i == 0)) and cycle['type'] == 1:
            print(f"Exporting {cycle['year']} {cycle['name']}")
            s.export_reports(cycle['id'], reports_dir)
