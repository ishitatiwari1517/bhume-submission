import sys
from pathlib import Path
from bhume import load, write_predictions
from bhume.baseline import _utm_for
from shapely.affinity import translate
import geopandas as gpd

village_path = sys.argv[1]
v = load(village_path)

utm = _utm_for(v.example_truths.geometry.iloc[0])

official = v.plots.to_crs(utm)
truth = v.example_truths.to_crs(utm)

samples = []

for pn in truth.index:
    o = official.loc[pn].geometry.centroid
    t = truth.loc[pn].geometry.centroid

    samples.append({
        "x": o.x,
        "y": o.y,
        "dx": t.x - o.x,
        "dy": t.y - o.y,
    })

preds = official.copy()
confs = []
statuses = []

for idx, row in preds.iterrows():

    c = row.geometry.centroid

    weights = []
    dxs = []
    dys = []

    for s in samples:
        d = ((c.x - s["x"])**2 + (c.y - s["y"])**2) ** 0.5

        w = 1 / max(d, 1)

        weights.append(w)
        dxs.append(w * s["dx"])
        dys.append(w * s["dy"])

    dx = sum(dxs) / sum(weights)
    dy = sum(dys) / sum(weights)
    nearest = min(
        ((c.x - s["x"])**2 + (c.y - s["y"])**2) ** 0.5
        for s in samples
    )

    confidence = max(
        0.3,
        min(
            0.95,
            1 - nearest / 4000
        )
    )

    confs.append(confidence)

    if confidence < 0.45:
        statuses.append("flagged")
    else:
        statuses.append("corrected")

    preds.at[idx, "geometry"] = translate(
        row.geometry,
        dx,
        dy
    )

preds = preds.to_crs("EPSG:4326")

preds["status"] = statuses
preds["confidence"] = confs
preds["method_note"] = "inverse distance weighted shift"

out = Path(village_path) / "predictions_idw.geojson"

write_predictions(
    out,
    preds
)

print("done")
