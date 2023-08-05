import os
import re

import numpy as np
import pandas as pd

root_dir = "C:\\Users\\gbr\\Documents\\data"

# vass
iedriver_path = "C:\\Users\\gbr\\Documents\\data\\scripts and notebooks\\IEDriverServer.exe"
vass_grid_password = [('4', '4'), ('5', '4'), ('4', '5'), ('5', '5'),
                      ('3', '6'), ('6', '6')]
vass_year = "2020"
vass_username = "gbr"
vass_password = """}{P][p00"""
vass_folder = "vass exports"
vass_dir = os.path.join(root_dir, vass_folder)
vass_student_details_dir = os.path.join(vass_dir, "personal details summary")
vass_school_program_dir = os.path.join(vass_dir, "school program summary")
vass_predicted_scores_dir = os.path.join(vass_dir, "predicted scores")
vass_school_scores_dir = os.path.join(vass_dir, "school scores")
vass_gat_scores_dir = os.path.join(vass_dir, "gat scores")
vass_external_scores_dir = os.path.join(vass_dir, "external scores")

# compass
from vicedtools.compass.compasssession import CompassConfigAuthenticator

compass_username = 'gbr'
compass_password = '}{P][p00'
compass_authenticator = CompassConfigAuthenticator(compass_username,
                                                   compass_password)
compass_school_code = "gwsc-vic"
compass_folder = "compass exports"
student_details_folder = "student details"
sds_folder = "SDS export"
learning_tasks_folder = "learning tasks"
reports_folder = "reports"
progress_reports_folder = "progress reports"
student_details_csv = os.path.join(root_dir, compass_folder,
                                   student_details_folder,
                                   "student details.csv")
student_household_information_csv = os.path.join(
    root_dir, compass_folder, student_details_folder,
    "student household information.csv")
sds_dir = os.path.join(root_dir, compass_folder, sds_folder)
reports_file = os.path.join(root_dir, compass_folder, "reports.csv")
reports_summary_file = os.path.join(root_dir, compass_folder,
                                    "reports_summary.csv")
compass_dir = os.path.join(root_dir, compass_folder)
progress_reports_dir = os.path.join(root_dir, compass_folder,
                                    progress_reports_folder)
learning_tasks_dir = os.path.join(root_dir, compass_folder,
                                  learning_tasks_folder)
reports_dir = os.path.join(root_dir, compass_folder, reports_folder)
academic_groups_json = os.path.join(compass_dir, "academic groups.json")
progress_report_cycles_json = os.path.join(compass_dir,
                                           "progress report cycles.json")
report_cycles_json = os.path.join(compass_dir, "report cycles.json")

# naplan
from vicedtools.naplan.dataservicesession import DataServiceConfigAuthenticator

dataservice_username = "Glen01"
dataservice_password = "HXZ55cdt"
dataservice_authenticator = DataServiceConfigAuthenticator(
    dataservice_username, dataservice_password)
naplan_dir = os.path.join(root_dir, "naplan exports")
naplan_outcomes_dir = os.path.join(naplan_dir, "outcomes exports")
naplan_sssr_dir = os.path.join(naplan_dir, "sssr exports")

# oars
oars_username = "gbr"
oars_password = "}{P][p00acer"
from vicedtools.acer import OARSConfigAuthenaticator

oars_authenticator = OARSConfigAuthenaticator(oars_username, oars_password)
oars_school_code = "glen-waverley-secondary-college"

oars_dir = os.path.join(root_dir, "OARS exports")
pat_scores_csv = os.path.join(oars_dir, "pat scores.csv")
pat_most_recent_csv = os.path.join(oars_dir, "pat most recent.csv")
ewrite_scores_csv = os.path.join(oars_dir, "eWrite scores.csv")
ewrite_criteria_csv = os.path.join(oars_dir, "eWrite criteria.csv")
pat_sittings_dir = os.path.join(oars_dir, "PAT sittings")
ewrite_sittings_dir = os.path.join(oars_dir, "eWrite sittings")
oars_tests_json = os.path.join(oars_dir, "tests.json")
scale_constructs_json = os.path.join(oars_dir, "scale constructs.json")

# gcp
student_details_table_id = "gwsc-school-data.student_details.student_details"
student_enrolments_table_id = "gwsc-school-data.student_details.student_enrolments"
pat_scores_table_id = "gwsc-school-data.student_results.pat_scores"
pat_most_recent_table_id = "gwsc-school-data.student_results.pat_most_recent"
naplan_outcomes_table_id = "gwsc-school-data.student_results.naplan"
reports_table_id = "gwsc-school-data.student_results.reports"
reports_summary_table_id = "gwsc-school-data.student_results.reports_summary"
gat_table_id = "gwsc-school-data.student_results.gat"
ewrite_scores_table_id = "gwsc-school-data.student_results.ewrite_scores"
ewrite_criteria_table_id = "gwsc-school-data.student_results.ewrite_criteria"
vce_study_scores_table_id = "gwsc-school-data.vce_data.study_scores"
vce_adjusted_scores_table_id = "gwsc-school-data.vce_data.adjusted_scores"
bucket = "gwsc-student-details"

# gwsc
subjects_file = "C:/Users/gbr/Documents/data/SDS exports/subjects metadata.csv"
replace_values = {
    "SubjectName": {
        "9 Design and Technologies - Textiles Yr9":
            "9 Design & Technologies - Textiles Yr9",
        "9 Design &Technologies - Textiles Yr9":
            "9 Design & Technologies - Textiles Yr9",
        "9 Design &Technologies - Wood Yr9":
            "9 Design & Technologies - Wood Yr9",
        "9 Design and Technologies - Materials Yr9":
            "9 Design & Technologies - Wood Yr9",
        "11 System Engineering Electronics Yr11":
            "11 Systems Engineering Yr11",
        "9 Digital Technologies Yr9":
            "9 Digital Technology Yr9",
        "9 Digital technologies Yr9":
            "9 Digital Technology Yr9",
        "11 Computing Yr11":
            "11 Applied Computing Yr11",
        "11 Studio Art Yr11":
            "11 Studio Arts Yr11",
        "9 Art - Drawing and Painting Yr9":
            "9 Art - Drawing & Painting Yr9",
        "9 Coaching Leadership and Sport Yr9":
            "9 Coaching Leadership &Sport Yr9"
    },
    "Result": {
        "Needs Improvement": "Below Standard",
        "Ungraded": "Not Demonstrated"
    }
}

replace_subject_codes = {
    "SubjectCode": {
        "GTR": "GTAR",
        "GUITAR": "GTAR",
        "VOICE": "VOX",
        "BASSGUITAR": "BGTR",
        "B_GTRA": "BGTR",
        "TRMPT": "TMPT",
        "VIOLIN": "VLN"
    }
}

grade_order = [
    "Exempt", "Modified", "Not Demonstrated", "Unsatisfactory", "Rarely",
    "Below Standard", "Satisfactory", "Sometimes", "Competent", "Good",
    "Very Good", "Usually", "Excellent", "Consistently", "Outstanding"
]
results_dtype = pd.api.types.CategoricalDtype(categories=grade_order,
                                              ordered=True)


def learning_tasks_result_mapper(result):
    if result == "Not Demonstrated":
        return 0.35
    if result == "Below Standard":
        return 0.46
    if result == "Satisfactory":
        return 0.55
    if result == "Competent":
        return 0.64
    if result == "Good":
        return 0.73
    if result == "Very Good":
        return 0.82
    if result == "Excellent":
        return 0.91
    if result == "Outstanding":
        return 1.0
    return float('nan')


def work_habits_result_mapper(result):
    if result == "Unsatisfactory":
        return 0.35
    if result == "Satisfactory":
        return 0.55
    if result == "Good":
        return 0.73
    if result == "Very Good":
        return 0.82
    if result == "Excellent":
        return 1.0
    return np.nan


def progress_report_result_mapper(result):
    if result == "Rarely":
        return 0.25
    if result == "Sometimes":
        return 0.5
    if result == "Usually":
        return 0.75
    if result == "Consistently":
        return 1.0
    return np.nan


progress_report_items = [
    "Completes all set learning", "Contribution in class", "Perseverance",
    "Ready to learn", "Respectfully works/communicates with others",
    "Uses feedback to improve"
]


def gwsc_class_code_parser(class_code, pattern_string):
    m = re.search(pattern_string, class_code)
    if m:
        subject_code = m.group('code')
        # test for Global Goodies vs Geography
        if subject_code == "10GG":
            m = re.search("10GGD[12345]", class_code)
            if m:
                subject_code = "10GL"
        return subject_code
    else:
        print(class_code + " not found")
        return ""
