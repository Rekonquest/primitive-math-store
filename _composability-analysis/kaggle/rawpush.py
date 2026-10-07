import os, json
import requests
from requests.auth import HTTPBasicAuth

u = os.environ["KAGGLE_USERNAME"]; k = os.environ["KAGGLE_KEY"]
auth = HTTPBasicAuth(u, k)
base = "https://www.kaggle.com/api/v1"

def show(label, r):
    print(f"--- {label} -> {r.status_code}")
    print("   " + r.text[:400].replace("\n", " "))

# baselines
show("GET /datasets/list?mine", requests.get(base + "/datasets/list", params={"mine": "true"}, auth=auth))
show("GET /competitions/list", requests.get(base + "/competitions/list", auth=auth))
show("GET /users/" + u, requests.get(base + f"/kernels/list", params={"mine": "true"}, auth=auth))

# the actual push
src = open(r"C:\Projects\primitves math\_composability-analysis\kaggle\run.py", encoding="utf-8").read()
body = {
    "slug": f"{u}/ordo-composition-sim",
    "newTitle": "Ordo Composition Sim",
    "text": src,
    "language": "python",
    "kernelType": "script",
    "isPrivate": True,
    "enableGpu": False,
    "enableInternet": False,
    "datasetDataSources": [],
    "competitionDataSources": [],
    "kernelDataSources": [],
    "modelDataSources": [],
    "categoryIds": [],
}
show("POST /kernels/push", requests.post(base + "/kernels/push", auth=auth, json=body))
