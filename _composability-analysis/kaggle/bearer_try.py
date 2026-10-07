import os, json
import requests

u = os.environ["KAGGLE_USERNAME"]; k = os.environ["KAGGLE_KEY"]
print("token prefix:", k[:4], "| len:", len(k), "| looks like KGAT:", k.startswith("KGAT"))

src = open(r"C:\Projects\primitves math\_composability-analysis\kaggle\run.py", encoding="utf-8").read()
body = {
    "slug": f"{u}/ordo-composition-sim", "newTitle": "Ordo Composition Sim",
    "text": src, "language": "python", "kernelType": "script",
    "isPrivate": True, "enableGpu": False, "enableInternet": False,
    "datasetDataSources": [], "competitionDataSources": [],
    "kernelDataSources": [], "modelDataSources": [], "categoryIds": [],
}

# Try BEARER auth on the REST push (new-platform style)
r = requests.post("https://www.kaggle.com/api/v1/kernels/push",
                  headers={"Authorization": f"Bearer {k}"}, json=body)
print("REST push w/ Bearer ->", r.status_code, r.text[:300].replace("\n", " "))

# Probe the official MCP endpoint with Bearer (JSON-RPC initialize)
init = {"jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05",
                   "capabilities": {}, "clientInfo": {"name": "probe", "version": "1"}}}
mr = requests.post("https://www.kaggle.com/mcp",
                   headers={"Authorization": f"Bearer {k}",
                            "Content-Type": "application/json",
                            "Accept": "application/json, text/event-stream"},
                   json=init, timeout=30)
print("MCP initialize ->", mr.status_code, mr.text[:300].replace("\n", " "))
