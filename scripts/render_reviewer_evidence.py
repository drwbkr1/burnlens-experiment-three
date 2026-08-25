#!/usr/bin/env python3
"""Render deterministic public-safe M6 reviewer evidence from accepted records."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "records/evaluation/EXPERIMENT-THREE-M5-RETROSPECTIVE-EVALUATION-2026-001.json"
TRAINING_RECORD = ROOT / "records/training/EXPERIMENT-THREE-M4-FROZEN-TRAINING-2026-001.json"
OUTPUT_DIR = ROOT / "docs/evidence/generated"
MANIFEST = ROOT / "records/release/EXPERIMENT-THREE-PUBLIC-EVIDENCE-MANIFEST-2026-001.json"
SEEDS = (20260725, 20260726, 20260727)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def svg_document(width: int, height: int, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">\n'
        f'<title id="title">{html.escape(title)}</title>\n'
        '<desc id="desc">Public-safe numerical evidence; no benchmark pixels, labels, '
        'model weights, predictions, or geospatial rasters are embedded.</desc>\n'
        '<rect width="100%" height="100%" fill="#f7f4ed"/>\n'
        '<style>text{font-family:Segoe UI,Arial,sans-serif;fill:#17252a}.title{font-size:30px;font-weight:700}.sub{font-size:16px;fill:#4a5a60}.label{font-size:15px;font-weight:600}.small{font-size:13px;fill:#46565c}.metric{font-size:18px;font-weight:700}.axis{stroke:#98a6aa;stroke-width:1}.grid{stroke:#d7dddf;stroke-width:1}.selected{stroke:#ab3c2f;stroke-width:2;stroke-dasharray:6 5}.train{fill:none;stroke:#197278;stroke-width:3}.val{fill:none;stroke:#d95f32;stroke-width:3}</style>\n'
        f'{body}\n</svg>\n'
    )


def architecture_svg() -> str:
    boxes = [
        (70, 145, 180, 100, "6 channels", "pre/post S2"),
        (320, 145, 210, 100, "Conv 1×1", "6 → 8 + ReLU"),
        (600, 145, 210, 100, "Conv 1×1", "8 → 8 + ReLU"),
        (880, 145, 210, 100, "Conv 1×1", "8 → 1 logit"),
        (1160, 145, 180, 100, "Probability", "sigmoid"),
    ]
    parts = [
        '<text x="70" y="55" class="title">A deliberately data-sized neural detector</text>',
        '<text x="70" y="85" class="sub">One shared pointwise network • arbitrary H×W • no spatial-context or patch-position memory</text>',
    ]
    for index, (x, y, w, h, top, bottom) in enumerate(boxes):
        fill = "#d9ece8" if index in (1, 2, 3) else "#e8e4da"
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="#31545a" stroke-width="2"/>')
        parts.append(f'<text x="{x+w/2}" y="{y+42}" text-anchor="middle" class="metric">{top}</text>')
        parts.append(f'<text x="{x+w/2}" y="{y+70}" text-anchor="middle" class="small">{bottom}</text>')
        if index < len(boxes) - 1:
            nx = boxes[index + 1][0]
            parts.append(f'<line x1="{x+w+12}" y1="{y+h/2}" x2="{nx-12}" y2="{y+h/2}" stroke="#31545a" stroke-width="3"/>')
            parts.append(f'<path d="M {nx-22} {y+h/2-7} L {nx-12} {y+h/2} L {nx-22} {y+h/2+7}" fill="none" stroke="#31545a" stroke-width="3"/>')
    parts.extend([
        '<rect x="70" y="300" width="1270" height="72" rx="12" fill="#fff" stroke="#d2cbc0"/>',
        '<text x="95" y="332" class="metric">137 trainable parameters</text>',
        '<text x="95" y="357" class="small">(6×8+8) + (8×8+8) + (8×1+1). Size was frozen before training; no model shopping followed.</text>',
    ])
    return svg_document(1410, 420, "\n".join(parts), "Experiment Three 137-parameter architecture")


def scale_points(rows: list[dict[str, float]], key: str, x: float, y: float, width: float, height: float, ymin: float, ymax: float) -> str:
    maximum_epoch = max(row["epoch"] for row in rows)
    points = []
    for row in rows:
        px = x + width * (row["epoch"] - 1) / max(1, maximum_epoch - 1)
        py = y + height * (ymax - row[key]) / max(1e-12, ymax - ymin)
        points.append(f"{px:.2f},{py:.2f}")
    return " ".join(points)


def training_curves_svg(histories: dict[int, dict[str, object]], training_record: dict[str, object]) -> str:
    selected = {item["seed"]: item for item in training_record["seeds"]}
    parts = [
        '<text x="60" y="50" class="title">All three frozen training histories</text>',
        '<text x="60" y="78" class="sub">Event-class-balanced masked BCE • checkpoint chosen by minimum validation loss • no test feedback</text>',
    ]
    colors = {"train": "#197278", "validation": "#d95f32"}
    for panel, seed in enumerate(SEEDS):
        x, y, width, height = 110, 135 + panel * 245, 1180, 165
        rows = histories[seed]["rows"]
        values = [row[key] for row in rows for key in ("train_balanced_bce", "validation_balanced_bce")]
        ymin, ymax = min(values), max(values)
        pad = max(0.005, (ymax - ymin) * 0.12)
        ymin, ymax = ymin - pad, ymax + pad
        parts.append(f'<text x="60" y="{y-18}" class="label">Seed {seed}</text>')
        for tick in range(5):
            py = y + height * tick / 4
            value = ymax - (ymax - ymin) * tick / 4
            parts.append(f'<line x1="{x}" y1="{py:.1f}" x2="{x+width}" y2="{py:.1f}" class="grid"/>')
            parts.append(f'<text x="{x-12}" y="{py+5:.1f}" text-anchor="end" class="small">{value:.3f}</text>')
        parts.append(f'<line x1="{x}" y1="{y+height}" x2="{x+width}" y2="{y+height}" class="axis"/>')
        max_epoch = histories[seed]["epochs_completed"]
        for epoch in (1, max_epoch // 2, max_epoch):
            px = x + width * (epoch - 1) / max(1, max_epoch - 1)
            parts.append(f'<text x="{px:.1f}" y="{y+height+22}" text-anchor="middle" class="small">{epoch}</text>')
        for key, css in (("train_balanced_bce", "train"), ("validation_balanced_bce", "val")):
            pts = scale_points(rows, key, x, y, width, height, ymin, ymax)
            parts.append(f'<polyline points="{pts}" class="{css}"/>')
        chosen = selected[seed]["selected_epoch"]
        sx = x + width * (chosen - 1) / max(1, max_epoch - 1)
        parts.append(f'<line x1="{sx:.1f}" y1="{y}" x2="{sx:.1f}" y2="{y+height}" class="selected"/>')
        parts.append(f'<text x="{x+width+18}" y="{y+38}" class="small">selected epoch {chosen}</text>')
        parts.append(f'<text x="{x+width+18}" y="{y+62}" class="small">val BCE {selected[seed]["selected_validation_balanced_bce"]:.4f}</text>')
    parts.extend([
        '<line x1="1060" y1="875" x2="1110" y2="875" class="train"/><text x="1120" y="880" class="small">train</text>',
        '<line x1="1200" y1="875" x2="1250" y2="875" class="val"/><text x="1260" y="880" class="small">validation</text>',
        '<text x="60" y="920" class="small">Vertical dashed line: frozen validation-selected checkpoint. Early stopping completed at epochs 130 / 172 / 171.</text>',
    ])
    return svg_document(1500, 960, "\n".join(parts), "Training and validation curves for all seeds")


def comparative_svg(result: dict[str, object]) -> str:
    models = result["model_results"]
    decision = result["decision_evidence"]
    comparators = result["comparators"]
    rows = [
        ("Seed 20260725", models[0]["aggregate"]),
        ("Seed 20260726", models[1]["aggregate"]),
        ("Seed 20260727", models[2]["aggregate"]),
        ("3-seed median", {"event_class_macro_iou": decision["three_seed_median_event_class_macro_iou"], "worst_event_macro_dice": decision["three_seed_median_worst_event_macro_dice"]}),
        ("RBR", comparators["RBR"]),
        ("Exp 1 U-Net", comparators["canonical_experiment_one_unet"]),
        ("Constant background", comparators["constant_background"]),
        ("Constant burned", comparators["constant_burned"]),
    ]
    palette = ["#4c9f96", "#4c9f96", "#4c9f96", "#176b66", "#d95f32", "#87989d", "#b8a785", "#b8a785"]
    parts = [
        '<text x="60" y="50" class="title">The lifecycle passed; the comparison failed</text>',
        '<text x="60" y="80" class="sub">Frozen two-event sparse-core comparison. Every predeclared seed and control is shown.</text>',
    ]
    for chart, (metric, heading) in enumerate((("event_class_macro_iou", "Event-class macro IoU"), ("worst_event_macro_dice", "Worst-event macro Dice"))):
        x0 = 85 + chart * 740
        y0, chart_w, chart_h = 165, 620, 500
        parts.append(f'<text x="{x0}" y="130" class="metric">{heading}</text>')
        for tick in range(6):
            y = y0 + chart_h - chart_h * tick / 5
            parts.append(f'<line x1="{x0}" y1="{y}" x2="{x0+chart_w}" y2="{y}" class="grid"/>')
            parts.append(f'<text x="{x0-10}" y="{y+5}" text-anchor="end" class="small">{tick/5:.1f}</text>')
        bar_w, gap = 52, 23
        for index, (label, values) in enumerate(rows):
            value = values[metric]
            x = x0 + 18 + index * (bar_w + gap)
            h = value * chart_h
            parts.append(f'<rect x="{x}" y="{y0+chart_h-h:.2f}" width="{bar_w}" height="{h:.2f}" fill="{palette[index]}"/>')
            parts.append(f'<text x="{x+bar_w/2}" y="{y0+chart_h-h-8:.2f}" text-anchor="middle" class="small">{value:.3f}</text>')
            parts.append(f'<text transform="translate({x+bar_w/2},{y0+chart_h+18}) rotate(55)" class="small">{html.escape(label)}</text>')
    parts.extend([
        '<rect x="60" y="825" width="1380" height="106" rx="12" fill="#fff" stroke="#d2cbc0"/>',
        '<text x="85" y="857" class="label">Frozen decision</text>',
        '<text x="85" y="885" class="small">PASS required every seed nonconstant on both events and the three-seed median to beat the strongest constant on both measures.</text>',
        '<text x="85" y="911" class="small">Observed: one seed was constant on Windigo; median 0.220 IoU / 0.292 worst Dice vs constant 0.285 / 0.333 → comparative FAIL.</text>',
        '<text x="60" y="978" class="small">Thresholds: Experiment Three = 0.5 selected on validation only; RBR = historical fixed 0.0410432; U-Net = admitted historical predictions; constants are fixed definitions.</text>',
    ])
    return svg_document(1500, 1020, "\n".join(parts), "Experiment Three comparative summary")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--training-root", type=Path, required=True)
    args = parser.parse_args()
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    training_record = json.loads(TRAINING_RECORD.read_text(encoding="utf-8"))
    if result["dispositions"]["lifecycle_status"] != "PASS" or result["dispositions"]["comparative_status"] != "FAIL":
        raise ValueError("accepted dispositions changed")
    histories: dict[int, dict[str, object]] = {}
    history_sources = []
    for seed in SEEDS:
        path = args.training_root / f"seed-{seed}" / "training-history.json"
        history = json.loads(path.read_text(encoding="utf-8"))
        if history["epochs_completed"] != len(history["rows"]):
            raise ValueError(f"incomplete history for seed {seed}")
        histories[seed] = history
        history_sources.append({"seed": seed, "bytes": path.stat().st_size, "sha256": sha256(path)})
    outputs = {
        "architecture.svg": architecture_svg(),
        "training-curves.svg": training_curves_svg(histories, training_record),
        "comparative-summary.svg": comparative_svg(result),
    }
    for name, text in outputs.items():
        write_text(OUTPUT_DIR / name, text)
    public_docs = [
        ROOT / "docs/evidence/REVIEWER-GUIDE.md",
        ROOT / "docs/benchmark/BENCHMARK-CARD.md",
        ROOT / "docs/reproducibility/REPRODUCIBILITY.md",
        ROOT / "docs/model-card/MODEL-CARD.md",
        ROOT / "docs/limitations/LIMITATIONS.md",
        RESULT,
    ]
    artifacts = []
    for path in sorted([*OUTPUT_DIR.glob("*.svg"), *public_docs], key=lambda item: item.as_posix()):
        artifacts.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": sha256(path)})
    manifest = {
        "schema_version": "burnlens-exp3-public-evidence/v1",
        "manifest_id": "EXPERIMENT-THREE-PUBLIC-EVIDENCE-2026-001",
        "source_checkpoint": {"commit": "45b32c1cb782edc31ef8a4f49671b6a897c7d7bb", "tree": "91fb304d4cadc450ed997c0d3f68c995b5538cb4"},
        "dispositions": {"lifecycle_status": "PASS", "comparative_status": "FAIL"},
        "source_histories": history_sources,
        "artifacts": artifacts,
        "forbidden_bytes_included": 0,
        "public_package_scope": "repository-authored narrative, metrics, hashes, and numerical SVGs only",
        "controlled_only_surfaces": ["benchmark arrays", "source imagery", "labels", "historical comparator arrays", "model checkpoints", "predictions", "probabilities", "GeoTIFFs", "imagery-bearing comparison render", "runtime", "private review material"],
    }
    write_text(MANIFEST, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "artifacts": len(artifacts), "history_sources": history_sources, "manifest": MANIFEST.relative_to(ROOT).as_posix()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
