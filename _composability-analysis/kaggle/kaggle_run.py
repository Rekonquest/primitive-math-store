import os, sys, json, time
import requests

u = os.environ["KAGGLE_USERNAME"]; k = os.environ["KAGGLE_KEY"]
H = {"Authorization": f"Bearer {k}"}
SLUG = "ordo-composition-sim"
action = sys.argv[1] if len(sys.argv) > 1 else "push"

def push():
    src = open(r"C:\Projects\primitves math\_composability-analysis\kaggle\run.py", encoding="utf-8").read()
    body = {
        "slug": f"{u}/{SLUG}", "newTitle": "Ordo Composition Sim", "text": src,
        "language": "python", "kernelType": "script", "isPrivate": True,
        "enableGpu": False, "enableInternet": False,
        "datasetDataSources": [], "competitionDataSources": [],
        "kernelDataSources": [], "modelDataSources": [], "categoryIds": [],
    }
    r = requests.post("https://www.kaggle.com/api/v1/kernels/push", headers=H, json=body)
    j = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    print("PUSH", r.status_code, "| url:", j.get("url"), "| version:", j.get("versionNumber"),
          "| error:", repr(j.get("error")))
    print("budget in pushed run.py:",
          [ln for ln in src.splitlines() if ln.startswith("TIME_BUDGET_SEC")][:1])

def status():
    s = requests.get("https://www.kaggle.com/api/v1/kernels/status", headers=H,
                     params={"userName": u, "kernelSlug": SLUG})
    print("STATUS", s.status_code, s.text[:300])

def output():
    s = requests.get("https://www.kaggle.com/api/v1/kernels/output", headers=H,
                     params={"userName": u, "kernelSlug": SLUG})
    print("OUTPUT", s.status_code, s.text[:1500])

if action == "push":
    push(); time.sleep(4); status()
elif action == "status":
    status()
elif action == "output":
    output()
