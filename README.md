# BhuMe Boundary Correction Submission

## Approach

I started from the provided global median shift baseline.

The example truths showed that the offset was not constant across the village. Different plots had different shifts, suggesting a spatially varying error field.

To model this, I used inverse-distance weighted interpolation.

For each example truth:

- Compute centroid offset between official and corrected boundary.
- Store the observed dx, dy shift.

For every plot:

- Find weighted influence from all example truths.
- Estimate local dx, dy using inverse-distance weighting.
- Translate the plot geometry using the estimated shift.

## Confidence

Confidence is based on distance to the nearest example truth.

Plots closer to known corrections receive higher confidence.

Plots farther away receive lower confidence.

## Files

- `improved.py` : prediction generation code
- `data/vadnerbhairav/predictions.geojson`
- `data/malatavadi/predictions.geojson`

## Running

```bash
uv run python improved.py <village_path>

## Results

### Vadnerbhairav

Baseline (global median shift):

* Median IoU: 0.713

IDW interpolation:

* Median IoU: 0.996

### Malatavadi

Baseline (global median shift):

* Median IoU: 0.588

IDW interpolation:

* Median IoU: 0.936

## Limitations

This approach models spatially varying translation using the provided example truths.

It does not currently:

* Use imagery directly for edge detection.
* Use boundary raster information.
* Model rotation or shape deformation.

Future work would combine image-derived field boundaries with spatial interpolation for improved robustness.

## AI Usage

AI tools were used extensively for:

* Understanding the assignment
* Exploring the provided codebase
* Debugging implementation issues
* Evaluating alternative approaches

All design decisions, testing, evaluation, and final submission preparation were performed by the author.

