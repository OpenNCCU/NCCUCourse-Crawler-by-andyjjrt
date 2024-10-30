import os
from dotenv import load_dotenv

load_dotenv()

YEAR = os.getenv("YEAR") or ""
SEM = os.getenv("SEM") or ""
USERNAME = os.getenv("USERNAME") or ""
PASSWORD = os.getenv("PASSWORD") or ""

SERVER_URL = "http://es.nccu.edu.tw/"
KEY = "angu1arjjlST@2019"
SEM_API = SERVER_URL + "semester/"
PERSON_API = SERVER_URL + "person/"
COURSE_API = SERVER_URL + "course/"
TRACE_API = SERVER_URL + "tracing/"


def url(id, year_sem=YEAR + SEM):
    return (
        "http://newdoc.nccu.edu.tw/teaschm/"
        + year_sem
        + "/statistic.jsp-tnum="
        + id
        + ".htm"
    )


def course_rate_url(param, year_sem=YEAR + SEM):
    return "http://newdoc.nccu.edu.tw/teaschm/" + year_sem + "/" + param


YEAR_SEM = YEAR + SEM


def rate_qry():
    return str(os.getenv("RATE_QRY")).split(",")


COURSERESULT_YEARSEM = ["1102", "1111", "1112", "1121"]

def courseresult_csv(sem):
    return sem + "CourseResult.csv"
