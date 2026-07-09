#!/usr/bin/env python3
"""Generate an ecommerce image/detail-page diagnosis HTML report for Codex."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


GRADE_CONFIG = {
    "S": {"label": "优秀", "color": "#1f6b2a", "bg": "#e8f4df"},
    "A": {"label": "良好", "color": "#0f5f9f", "bg": "#e7f1fb"},
    "B": {"label": "及格", "color": "#9a620b", "bg": "#fff0d8"},
    "C": {"label": "待改进", "color": "#a13b1f", "bg": "#fde9e1"},
    "D": {"label": "急需重做", "color": "#9b1c1c", "bg": "#fde8e8"},
}

DIMENSION_NAMES = {
    "clarity": "视觉清晰度",
    "info_delivery": "信息传达",
    "differentiation": "差异化竞争力",
    "trust": "信任感建立",
    "compliance": "平台合规性",
    "first_screen": "首屏冲击力",
    "info_structure": "信息结构",
    "scene": "场景化呈现",
    "trust_proof": "信任背书",
    "conversion": "转化促进",
    "visual_conversion_readiness": "视觉转化准备度",
    "review_voc_alignment": "评价/VOC匹配度",
    "competitor_differentiation": "竞品差异化",
    "trust_and_proof": "信任与证明完整度",
    "compliance_expectation_control": "合规与预期控制",
}


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def as_number(value: Any, default: float = 0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def grade_for(score: float) -> str:
    if score >= 85:
        return "S"
    if score >= 70:
        return "A"
    if score >= 55:
        return "B"
    if score >= 40:
        return "C"
    return "D"


def slugify(value: str) -> str:
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "_", value.strip(), flags=re.UNICODE)
    slug = re.sub(r"_+", "_", slug).strip("_")
    return slug or "ecommerce_diagnosis_report"


def default_output_path(input_path: Path, data: dict[str, Any]) -> Path:
    product_name = str(data.get("product_name") or input_path.stem)
    return Path.cwd() / "outputs" / f"{slugify(product_name)}_diagnosis.html"


def list_items(items: Any, empty: str = "暂无") -> str:
    if not items:
        return f"<p class='muted'>{esc(empty)}</p>"
    if isinstance(items, str):
        items = [items]
    return "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def tags(items: Any, kind: str) -> str:
    if not items:
        return "<span class='muted small'>暂无</span>"
    if isinstance(items, str):
        items = [items]
    return "".join(f"<span class='tag {kind}'>{esc(item)}</span>" for item in items)


def score_bar(score: Any, max_score: Any) -> str:
    score_num = as_number(score)
    max_num = as_number(max_score, 100)
    pct = 0 if max_num <= 0 else max(0, min(100, round(score_num / max_num * 100)))
    return f"<div class='bar'><span style='width:{pct}%'></span></div>"


def render_dimension(name: str, data: dict[str, Any]) -> str:
    label = DIMENSION_NAMES.get(name, name)
    score = data.get("score", 0)
    max_score = data.get("max", 100)
    reason = data.get("reason")
    return f"""
      <article class="metric">
        <div class="metric-head"><strong>{esc(label)}</strong><span>{esc(score)}/{esc(max_score)}</span></div>
        {score_bar(score, max_score)}
        {f"<p class='reason'>{esc(reason)}</p>" if reason else ""}
        <div class="label">发现问题</div>
        <div>{tags(data.get("issues", []), "bad")}</div>
        <div class="label">优化建议</div>
        <div>{tags(data.get("suggestions", []), "good")}</div>
      </article>
    """


def render_section_dimensions(title: str, block: dict[str, Any], ordered_keys: list[str]) -> str:
    cards = [render_dimension(key, block[key]) for key in ordered_keys if isinstance(block.get(key), dict)]
    if not cards:
        return ""
    return f"<section class='panel'><h2>{esc(title)}</h2><div class='grid'>{''.join(cards)}</div></section>"


def render_findings(findings: Any) -> str:
    if not findings:
        return list_items([], "暂无核心发现")
    if isinstance(findings, str):
        findings = [findings]
    rows = []
    for item in findings:
        if isinstance(item, dict):
            title = item.get("title") or item.get("finding") or item.get("issue") or "核心发现"
            body = []
            for key, label in [("evidence", "证据"), ("impact", "影响"), ("fix", "建议")]:
                if item.get(key):
                    body.append(f"<p><strong>{label}：</strong>{esc(item[key])}</p>")
            rows.append(f"<article class='finding'><h3>{esc(title)}</h3>{''.join(body)}</article>")
        else:
            rows.append(f"<article class='finding'><p>{esc(item)}</p></article>")
    return "".join(rows)


def render_priority(priority: dict[str, Any]) -> str:
    labels = {"P0": "立即修复", "P1": "本周优化", "P2": "下次迭代"}
    parts = []
    for level in ["P0", "P1", "P2"]:
        parts.append(f"<h3>{level} {labels[level]}</h3>")
        items = priority.get(level, [])
        if not items:
            parts.append(f"<p class='muted'>暂无 {level} 项</p>")
            continue
        if isinstance(items, str):
            items = [items]
        parts.extend(f"<div class='priority {level.lower()}'>{esc(item)}</div>" for item in items)
    return "".join(parts)


def render_evidence_overview(data: dict[str, Any]) -> str:
    evidence = data.get("evidence_overview") or {}
    if not isinstance(evidence, dict):
        return f"<p>{esc(evidence)}</p>" if evidence else "<p class='muted'>未提供材料概览。</p>"
    used = evidence.get("used") or []
    missing = evidence.get("missing") or []
    notes = evidence.get("notes")
    return f"""
      <div class="two-col">
        <div><h3>已使用材料</h3>{list_items(used, "未标注")}</div>
        <div><h3>关键缺失数据</h3>{list_items(missing, "暂无")}</div>
      </div>
      {f"<p class='muted'>{esc(notes)}</p>" if notes else ""}
    """


def render_copy(data: dict[str, Any]) -> str:
    hierarchy = data.get("copy_hierarchy") or data.get("revised_copy_hierarchy")
    if not hierarchy:
        return ""
    if isinstance(hierarchy, dict):
        rows = "".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in hierarchy.items())
        content = f"<table>{rows}</table>"
    else:
        content = list_items(hierarchy)
    return f"<section class='panel'><h2>建议文案层级</h2>{content}</section>"


def build_html(data: dict[str, Any]) -> str:
    product_name = data.get("product_name", "电商诊断报告")
    platform = data.get("platform")
    report_date = data.get("diagnosis_date") or date.today().isoformat()
    score = round(as_number(data.get("overall_score", data.get("score", 0))))
    grade = data.get("overall_grade") or grade_for(score)
    grade_config = GRADE_CONFIG.get(str(grade), GRADE_CONFIG[grade_for(score)])
    conclusion = data.get("conclusion") or data.get("summary") or "请结合评分、核心发现和优先行动进行优化。"
    main_image = data.get("main_image") if isinstance(data.get("main_image"), dict) else {}
    weighted = data.get("evidence_weighted_score") if isinstance(data.get("evidence_weighted_score"), dict) else {}

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(product_name)} - 电商诊断报告</title>
  <style>
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Microsoft YaHei", Arial, sans-serif; color: #222; background: #f6f4ef; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 28px 18px 48px; }}
    h1 {{ margin: 0 0 8px; font-size: 26px; }}
    h2 {{ margin: 0 0 16px; font-size: 18px; border-left: 4px solid #1769d2; padding-left: 10px; }}
    h3 {{ margin: 14px 0 8px; font-size: 15px; }}
    p, li, td, th {{ line-height: 1.65; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th, td {{ border-bottom: 1px solid #eee8dc; padding: 10px; text-align: left; vertical-align: top; }}
    th {{ width: 180px; color: #555; background: #faf8f2; }}
    .top {{ display: grid; grid-template-columns: 1fr 260px; gap: 16px; align-items: stretch; }}
    .panel {{ background: #fff; border: 1px solid #ddd7c9; border-radius: 10px; padding: 18px; margin: 16px 0; }}
    .score-card {{ display: flex; align-items: center; justify-content: center; flex-direction: column; background: {grade_config["bg"]}; }}
    .score-card strong {{ font-size: 58px; line-height: 1; color: {grade_config["color"]}; }}
    .grade {{ margin-top: 8px; padding: 4px 12px; border-radius: 999px; background: {grade_config["color"]}; color: #fff; font-size: 14px; }}
    .meta {{ color: #666; font-size: 13px; }}
    .grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
    .two-col {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    .metric, .finding {{ border: 1px solid #e2dccf; border-radius: 8px; padding: 14px; background: #fff; }}
    .metric-head {{ display: flex; justify-content: space-between; gap: 10px; margin-bottom: 10px; }}
    .bar {{ height: 8px; background: #eee8dc; border-radius: 999px; overflow: hidden; margin-bottom: 12px; }}
    .bar span {{ display: block; height: 100%; background: #1769d2; }}
    .label {{ margin-top: 10px; margin-bottom: 4px; color: #777; font-size: 12px; }}
    .tag {{ display: inline-block; margin: 3px 4px 3px 0; padding: 3px 8px; border-radius: 4px; font-size: 13px; }}
    .bad {{ background: #fde8e3; color: #9b321a; }}
    .good {{ background: #e8f4df; color: #2f6817; }}
    .priority {{ margin: 8px 0; padding: 10px 12px; border-radius: 8px; }}
    .p0 {{ background: #fde8e8; }}
    .p1 {{ background: #fff0d8; }}
    .p2 {{ background: #e8f1fc; }}
    .muted {{ color: #777; }}
    .small {{ font-size: 12px; }}
    .reason {{ color: #555; margin: 0 0 8px; }}
    @media (max-width: 780px) {{ .top, .grid, .two-col {{ grid-template-columns: 1fr; }} .score-card strong {{ font-size: 44px; }} }}
  </style>
</head>
<body>
  <main>
    <section class="top">
      <div class="panel">
        <h1>{esc(product_name)}</h1>
        <p class="meta">诊断日期：{esc(report_date)}{f" · 平台：{esc(platform)}" if platform else ""}</p>
        <p>{esc(conclusion)}</p>
      </div>
      <div class="panel score-card">
        <strong>{esc(score)}</strong>
        <span class="grade">{esc(grade)} 级 / {esc(grade_config["label"])}</span>
      </div>
    </section>
    <section class="panel"><h2>证据概览</h2>{render_evidence_overview(data)}</section>
    <section class="panel"><h2>核心发现</h2>{render_findings(data.get("key_findings", []))}</section>
    <section class="panel"><h2>优先改进行动</h2>{render_priority(data.get("priority_actions", {}) if isinstance(data.get("priority_actions"), dict) else {})}</section>
    {render_section_dimensions("证据加权评分", weighted, ["visual_conversion_readiness", "review_voc_alignment", "competitor_differentiation", "trust_and_proof", "compliance_expectation_control"])}
    {render_section_dimensions("主图详细诊断", main_image, ["clarity", "info_delivery", "differentiation", "trust", "compliance"])}
    {render_copy(data)}
  </main>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate ecommerce diagnosis HTML report for Codex.")
    parser.add_argument("diagnosis_json_file", help="Path to diagnosis JSON.")
    parser.add_argument("output_html_file", nargs="?", help="Optional output HTML path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.diagnosis_json_file).expanduser().resolve()
    with input_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    output_path = Path(args.output_html_file).expanduser().resolve() if args.output_html_file else default_output_path(input_path, data)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_html(data), encoding="utf-8")
    print(str(output_path))


if __name__ == "__main__":
    main()
