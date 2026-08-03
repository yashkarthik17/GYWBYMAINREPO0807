# Website/adult/work/redo2/fetch_refs.py
"""Download the non-start-image reference medias recorded in redo/leg_3.json."""
import json, os, urllib.request

os.makedirs("refs", exist_ok=True)
d = json.load(open("../redo/leg_3.json"))
j = d[0] if isinstance(d, list) else d
medias = j["params"]["medias"]
n = 0
for m in medias:
    if m.get("role") == "start_image":
        continue
    n += 1
    url = m["data"]["url"]
    out = f"refs/ref_{n}.png"
    urllib.request.urlretrieve(url, out)
    print(out, "<-", url)
print(f"{n} refs")
