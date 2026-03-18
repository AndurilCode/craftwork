#!/usr/bin/env python3
"""Generate a self-contained HTML review page for context eval results.

Reads the workspace directory, discovers with_harness and without_harness runs,
embeds outputs and grading data into a single HTML file. Supports both server
mode (with live feedback saving) and static mode (feedback downloads as JSON).

Usage:
    # Server mode (opens in browser, saves feedback to workspace)
    python generate_viewer.py <workspace>/iteration-N --harness-name "my-harness"

    # Static mode (writes standalone HTML, feedback downloads as file)
    python generate_viewer.py <workspace>/iteration-N --harness-name "my-harness" --static report.html

    # With benchmark data
    python generate_viewer.py <workspace>/iteration-N --harness-name "my-harness" --benchmark benchmark.json

    # With previous iteration for comparison
    python generate_viewer.py <workspace>/iteration-N --harness-name "my-harness" --previous-workspace <workspace>/iteration-<N-1>
"""

import argparse
import base64
import json
import mimetypes
import os
import signal
import sys
import webbrowser
from functools import partial
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

TEXT_EXTENSIONS = {
    ".txt", ".md", ".json", ".csv", ".py", ".js", ".ts", ".tsx", ".jsx",
    ".yaml", ".yml", ".xml", ".html", ".css", ".sh", ".sql", ".toml",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
METADATA_FILES = {"transcript.md", "user_notes.md", "metrics.json"}


def read_file_content(path: Path) -> dict:
    """Read a file and return its content with type info."""
    ext = path.suffix.lower()
    name = path.name

    if ext in TEXT_EXTENSIONS:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            return {"name": name, "type": "text", "content": text, "ext": ext}
        except Exception:
            return {"name": name, "type": "error", "content": f"Could not read {name}"}

    if ext in IMAGE_EXTENSIONS:
        try:
            data = base64.b64encode(path.read_bytes()).decode("ascii")
            mime = mimetypes.guess_type(str(path))[0] or "image/png"
            return {"name": name, "type": "image", "content": f"data:{mime};base64,{data}"}
        except Exception:
            return {"name": name, "type": "error", "content": f"Could not read {name}"}

    return {"name": name, "type": "binary", "content": f"[Binary file: {name}, {path.stat().st_size} bytes]"}


def discover_evals(workspace: Path) -> list[dict]:
    """Discover eval directories and their with/without harness runs."""
    evals = []

    for eval_dir in sorted(workspace.iterdir()):
        if not eval_dir.is_dir() or eval_dir.name.startswith("."):
            continue

        with_dir = eval_dir / "with_harness" / "outputs"
        without_dir = eval_dir / "without_harness" / "outputs"

        if not with_dir.exists() and not without_dir.exists():
            continue

        # Load metadata
        meta_path = eval_dir / "eval_metadata.json"
        meta = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
            except Exception:
                pass

        # Load grading
        grading_path = eval_dir / "grading.json"
        grading = {}
        if grading_path.exists():
            try:
                grading = json.loads(grading_path.read_text())
            except Exception:
                pass

        # Read outputs
        with_files = []
        if with_dir.exists():
            for f in sorted(with_dir.iterdir()):
                if f.is_file() and f.name not in METADATA_FILES:
                    with_files.append(read_file_content(f))

        without_files = []
        if without_dir.exists():
            for f in sorted(without_dir.iterdir()):
                if f.is_file() and f.name not in METADATA_FILES:
                    without_files.append(read_file_content(f))

        evals.append({
            "id": meta.get("eval_id", len(evals)),
            "name": meta.get("eval_name", eval_dir.name),
            "prompt": meta.get("prompt", ""),
            "with_harness_outputs": with_files,
            "without_harness_outputs": without_files,
            "grading": grading,
            "assertions": meta.get("assertions", []),
        })

    return evals


def load_benchmark(path: Path) -> dict | None:
    """Load benchmark.json if it exists."""
    if path and path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return None
    return None


def load_previous(workspace: Path) -> list[dict] | None:
    """Load previous iteration feedback and outputs."""
    if not workspace or not workspace.exists():
        return None

    feedback_path = workspace / "feedback.json"
    if feedback_path.exists():
        try:
            return json.loads(feedback_path.read_text()).get("reviews", [])
        except Exception:
            pass
    return None


def generate_html(
    evals: list[dict],
    harness_name: str,
    benchmark: dict | None = None,
    previous_feedback: list[dict] | None = None,
    static: bool = False,
) -> str:
    """Generate the self-contained HTML viewer."""

    evals_json = json.dumps(evals, indent=2)
    benchmark_json = json.dumps(benchmark, indent=2) if benchmark else "null"
    previous_json = json.dumps(previous_feedback, indent=2) if previous_feedback else "null"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Context Eval: {harness_name}</title>
<style>
:root {{
  --bg: #0f1117;
  --surface: #1a1d27;
  --surface2: #242836;
  --border: #2e3348;
  --text: #e2e4ed;
  --text-dim: #8b8fa3;
  --accent: #6c8aff;
  --green: #34d399;
  --red: #f87171;
  --yellow: #fbbf24;
  --orange: #fb923c;
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
.header {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; }}
.header h1 {{ font-size: 18px; font-weight: 600; }}
.header .harness-name {{ color: var(--accent); }}
.tabs {{ display: flex; gap: 0; background: var(--surface); border-bottom: 1px solid var(--border); padding: 0 24px; }}
.tab {{ padding: 12px 20px; cursor: pointer; border-bottom: 2px solid transparent; color: var(--text-dim); font-size: 14px; }}
.tab.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.tab:hover {{ color: var(--text); }}
.panel {{ display: none; padding: 24px; max-width: 1200px; margin: 0 auto; }}
.panel.active {{ display: block; }}
.eval-nav {{ display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }}
.eval-nav button {{ background: var(--surface2); border: 1px solid var(--border); color: var(--text); padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 13px; }}
.eval-nav button:hover {{ background: var(--border); }}
.eval-nav .counter {{ color: var(--text-dim); font-size: 14px; }}
.eval-title {{ font-size: 16px; font-weight: 600; margin-bottom: 4px; }}
.prompt {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 20px; font-size: 14px; line-height: 1.6; white-space: pre-wrap; }}
.comparison {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
.output-panel {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }}
.output-panel .panel-header {{ padding: 12px 16px; border-bottom: 1px solid var(--border); font-size: 13px; font-weight: 600; display: flex; justify-content: space-between; }}
.output-panel .panel-header.with {{ color: var(--accent); }}
.output-panel .panel-header.without {{ color: var(--text-dim); }}
.output-content {{ padding: 16px; max-height: 600px; overflow-y: auto; }}
.output-content pre {{ font-size: 13px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }}
.output-content img {{ max-width: 100%; border-radius: 4px; }}
.grading {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 20px; }}
.grading h3 {{ font-size: 14px; margin-bottom: 12px; }}
.assertion {{ display: grid; grid-template-columns: auto 80px 80px 120px 1fr; gap: 8px; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13px; }}
.assertion:last-child {{ border-bottom: none; }}
.assertion .text {{ grid-column: 1; }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; text-align: center; }}
.badge.pass {{ background: rgba(52,211,153,0.15); color: var(--green); }}
.badge.fail {{ background: rgba(248,113,113,0.15); color: var(--red); }}
.badge.disc {{ background: rgba(108,138,255,0.15); color: var(--accent); }}
.badge.nondisc {{ background: rgba(139,143,163,0.15); color: var(--text-dim); }}
.badge.inverse {{ background: rgba(251,146,60,0.15); color: var(--orange); }}
.feedback-box {{ margin-bottom: 20px; }}
.feedback-box label {{ display: block; font-size: 13px; color: var(--text-dim); margin-bottom: 6px; }}
.feedback-box textarea {{ width: 100%; min-height: 80px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; color: var(--text); padding: 12px; font-size: 14px; font-family: inherit; resize: vertical; }}
.previous-feedback {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 12px; margin-bottom: 16px; font-size: 13px; color: var(--text-dim); }}
.previous-feedback summary {{ cursor: pointer; font-weight: 600; }}
.submit-btn {{ background: var(--accent); color: white; border: none; padding: 12px 24px; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 600; }}
.submit-btn:hover {{ opacity: 0.9; }}

/* Benchmark tab */
.stat-cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }}
.stat-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
.stat-card .label {{ font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }}
.stat-card .value {{ font-size: 28px; font-weight: 700; }}
.stat-card .delta {{ font-size: 14px; margin-top: 4px; }}
.stat-card .delta.positive {{ color: var(--green); }}
.stat-card .delta.negative {{ color: var(--red); }}
.stat-card .delta.neutral {{ color: var(--text-dim); }}
.verdict {{ display: inline-block; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 14px; }}
.verdict.EFFECTIVE {{ background: rgba(52,211,153,0.15); color: var(--green); }}
.verdict.MARGINAL {{ background: rgba(251,191,36,0.15); color: var(--yellow); }}
.verdict.INEFFECTIVE {{ background: rgba(139,143,163,0.15); color: var(--text-dim); }}
.verdict.HARMFUL {{ background: rgba(248,113,113,0.15); color: var(--red); }}
.notes {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 16px; }}
.notes li {{ margin-bottom: 8px; font-size: 14px; line-height: 1.5; color: var(--text-dim); }}

/* Diagnosis tab */
.diagnosis-section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 20px; margin-bottom: 16px; }}
.diagnosis-section h3 {{ font-size: 15px; margin-bottom: 12px; }}
.tag {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; margin: 2px; background: var(--surface2); border: 1px solid var(--border); }}

@media (max-width: 768px) {{
  .comparison {{ grid-template-columns: 1fr; }}
  .assertion {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>

<div class="header">
  <h1>Context Eval: <span class="harness-name">{harness_name}</span></h1>
  <button class="submit-btn" onclick="submitFeedback()">Submit All Reviews</button>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab('outputs')">Outputs</div>
  <div class="tab" onclick="switchTab('benchmark')">Benchmark</div>
  <div class="tab" onclick="switchTab('diagnosis')">Diagnosis</div>
</div>

<div id="outputs-panel" class="panel active"></div>
<div id="benchmark-panel" class="panel"></div>
<div id="diagnosis-panel" class="panel"></div>

<script>
const EVALS = {evals_json};
const BENCHMARK = {benchmark_json};
const PREVIOUS = {previous_json};
const IS_STATIC = {'true' if static else 'false'};
let currentIdx = 0;
let feedbackData = {{}};

// Initialize feedback from previous
if (PREVIOUS) {{
  PREVIOUS.forEach(r => {{ feedbackData[r.run_id] = r.feedback || ''; }});
}}

function switchTab(tab) {{
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  event.target.classList.add('active');
  document.getElementById(tab + '-panel').classList.add('active');
}}

function renderFile(file) {{
  if (file.type === 'text') {{
    const lang = file.ext === '.json' ? 'json' : file.ext === '.py' ? 'python' : '';
    return `<div style="margin-bottom:12px"><div style="font-size:12px;color:var(--text-dim);margin-bottom:4px">${{file.name}}</div><pre>${{escapeHtml(file.content)}}</pre></div>`;
  }}
  if (file.type === 'image') {{
    return `<div style="margin-bottom:12px"><div style="font-size:12px;color:var(--text-dim);margin-bottom:4px">${{file.name}}</div><img src="${{file.content}}" /></div>`;
  }}
  return `<div style="margin-bottom:12px;color:var(--text-dim)">${{file.content}}</div>`;
}}

function escapeHtml(str) {{
  return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

function renderEval(idx) {{
  currentIdx = idx;
  const ev = EVALS[idx];
  const g = ev.grading || {{}};
  const assertions = g.assertions || [];

  let html = `
    <div class="eval-nav">
      <button onclick="renderEval(${{Math.max(0,idx-1)}})">&larr; Prev</button>
      <span class="counter">${{idx+1}} / ${{EVALS.length}}</span>
      <button onclick="renderEval(${{Math.min(EVALS.length-1,idx+1)}})">Next &rarr;</button>
    </div>
    <div class="eval-title">${{ev.name}}</div>
    <div class="prompt">${{escapeHtml(ev.prompt)}}</div>
    <div class="comparison">
      <div class="output-panel">
        <div class="panel-header with">With Harness</div>
        <div class="output-content">
          ${{ev.with_harness_outputs.map(renderFile).join('') || '<div style="color:var(--text-dim)">No outputs</div>'}}
        </div>
      </div>
      <div class="output-panel">
        <div class="panel-header without">Without Harness (Baseline)</div>
        <div class="output-content">
          ${{ev.without_harness_outputs.map(renderFile).join('') || '<div style="color:var(--text-dim)">No outputs</div>'}}
        </div>
      </div>
    </div>`;

  if (assertions.length > 0) {{
    html += `<div class="grading"><h3>Assertion Grading</h3>
      <div class="assertion" style="font-weight:600;color:var(--text-dim)">
        <div>Assertion</div><div>With</div><div>Without</div><div>Discrimination</div><div>Evidence</div>
      </div>`;
    assertions.forEach(a => {{
      const wh = a.with_harness || {{}};
      const woh = a.without_harness || {{}};
      const disc = a.discrimination || 'unknown';
      const discClass = disc === 'discriminating' ? 'disc' : disc === 'inverse' ? 'inverse' : 'nondisc';
      html += `<div class="assertion">
        <div class="text">${{escapeHtml(a.text)}}</div>
        <div><span class="badge ${{wh.passed ? 'pass' : 'fail'}}">${{wh.passed ? 'PASS' : 'FAIL'}}</span></div>
        <div><span class="badge ${{woh.passed ? 'pass' : 'fail'}}">${{woh.passed ? 'PASS' : 'FAIL'}}</span></div>
        <div><span class="badge ${{discClass}}">${{disc.replace(/_/g,' ')}}</span></div>
        <div style="font-size:12px;color:var(--text-dim)">${{escapeHtml((wh.evidence||'').substring(0,120))}}</div>
      </div>`;
    }});
    html += `</div>`;
  }}

  // Behavioral observations
  const obs = g.behavioral_observations;
  if (obs) {{
    html += `<details style="margin-bottom:20px"><summary style="cursor:pointer;font-size:14px;font-weight:600;color:var(--text-dim)">Behavioral Observations</summary>
      <div style="background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:16px;margin-top:8px;font-size:13px;line-height:1.6">
        ${{obs.approach_difference ? `<p><strong>Approach:</strong> ${{escapeHtml(obs.approach_difference)}}</p>` : ''}}
        ${{obs.precision_difference ? `<p><strong>Precision:</strong> ${{escapeHtml(obs.precision_difference)}}</p>` : ''}}
        ${{obs.efficiency_difference ? `<p><strong>Efficiency:</strong> ${{escapeHtml(obs.efficiency_difference)}}</p>` : ''}}
      </div>
    </details>`;
  }}

  // Previous feedback
  const prevKey = ev.name + '-with_harness';
  if (feedbackData[prevKey]) {{
    html += `<details class="previous-feedback"><summary>Previous Feedback</summary><p style="margin-top:8px">${{escapeHtml(feedbackData[prevKey])}}</p></details>`;
  }}

  // Feedback textarea
  html += `<div class="feedback-box">
    <label>Your feedback for this eval:</label>
    <textarea id="feedback-${{idx}}" oninput="saveFeedback(${{idx}})">${{escapeHtml(feedbackData[ev.name] || '')}}</textarea>
  </div>`;

  document.getElementById('outputs-panel').innerHTML = html;
}}

function saveFeedback(idx) {{
  const ev = EVALS[idx];
  feedbackData[ev.name] = document.getElementById('feedback-' + idx).value;
}}

function submitFeedback() {{
  const reviews = EVALS.map(ev => ({{
    run_id: ev.name + '-with_harness',
    eval_name: ev.name,
    feedback: feedbackData[ev.name] || '',
    timestamp: new Date().toISOString()
  }}));
  const data = JSON.stringify({{ reviews, status: 'complete' }}, null, 2);

  if (IS_STATIC) {{
    const blob = new Blob([data], {{ type: 'application/json' }});
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'feedback.json';
    a.click();
  }} else {{
    fetch('/feedback', {{ method: 'POST', body: data, headers: {{ 'Content-Type': 'application/json' }} }})
      .then(() => alert('Feedback saved!'))
      .catch(e => alert('Error saving: ' + e));
  }}
}}

function renderBenchmark() {{
  const panel = document.getElementById('benchmark-panel');
  if (!BENCHMARK) {{
    panel.innerHTML = '<div style="color:var(--text-dim);padding:40px;text-align:center">No benchmark data. Run generate_report.py to generate it.</div>';
    return;
  }}

  const r = BENCHMARK.results || {{}};
  const wh = r.with_harness || {{}};
  const woh = r.without_harness || {{}};
  const d = r.delta || {{}};
  const diag = BENCHMARK.diagnosis || {{}};

  let html = `<div class="stat-cards">
    <div class="stat-card">
      <div class="label">Verdict</div>
      <div class="value"><span class="verdict ${{diag.verdict || ''}}">${{diag.verdict || 'N/A'}}</span></div>
    </div>
    <div class="stat-card">
      <div class="label">With Harness Pass Rate</div>
      <div class="value">${{((wh.pass_rate||{{}}).mean*100||0).toFixed(0)}}%</div>
      <div class="delta neutral">±${{((wh.pass_rate||{{}}).stddev*100||0).toFixed(0)}}%</div>
    </div>
    <div class="stat-card">
      <div class="label">Without Harness Pass Rate</div>
      <div class="value">${{((woh.pass_rate||{{}}).mean*100||0).toFixed(0)}}%</div>
      <div class="delta neutral">±${{((woh.pass_rate||{{}}).stddev*100||0).toFixed(0)}}%</div>
    </div>
    <div class="stat-card">
      <div class="label">Benefit Delta</div>
      <div class="value">${{d.pass_rate || 'N/A'}}</div>
      <div class="delta ${{parseFloat(d.pass_rate)>0?'positive':parseFloat(d.pass_rate)<0?'negative':'neutral'}}">${{d.benefit_per_kilotoken ? d.benefit_per_kilotoken + '/kT' : ''}}</div>
    </div>
    <div class="stat-card">
      <div class="label">Harness Token Cost</div>
      <div class="value">${{(BENCHMARK.metadata||{{}}).harness_token_cost || 'N/A'}}</div>
    </div>
  </div>`;

  // Per-eval breakdown
  const breakdown = BENCHMARK.per_eval_breakdown || [];
  if (breakdown.length > 0) {{
    html += `<div class="grading"><h3>Per-Eval Breakdown</h3>`;
    breakdown.forEach(e => {{
      const pct = (e.benefit * 100).toFixed(0);
      const cls = e.benefit > 0 ? 'pass' : e.benefit < 0 ? 'fail' : 'nondisc';
      html += `<div style="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border)">
        <span>${{e.eval_name}}</span>
        <span><span class="badge ${{cls}}">${{pct > 0 ? '+' : ''}}${{pct}}%</span>
        <span style="font-size:12px;color:var(--text-dim);margin-left:8px">${{(e.with_harness_pass_rate*100).toFixed(0)}}% vs ${{(e.without_harness_pass_rate*100).toFixed(0)}}%</span></span>
      </div>`;
    }});
    html += `</div>`;
  }}

  panel.innerHTML = html;
}}

function renderDiagnosis() {{
  const panel = document.getElementById('diagnosis-panel');
  if (!BENCHMARK || !BENCHMARK.diagnosis) {{
    panel.innerHTML = '<div style="color:var(--text-dim);padding:40px;text-align:center">No diagnosis data available.</div>';
    return;
  }}

  const d = BENCHMARK.diagnosis;
  let html = `
    <div class="diagnosis-section">
      <h3>Verdict: <span class="verdict ${{d.verdict}}">${{d.verdict}}</span></h3>
      <p style="margin-top:12px;line-height:1.6">${{escapeHtml(d.reasoning || '')}}</p>
    </div>`;

  if (d.highest_impact_areas && d.highest_impact_areas.length > 0) {{
    html += `<div class="diagnosis-section"><h3>Highest Impact Areas</h3>
      <div style="margin-top:8px">${{d.highest_impact_areas.map(a => `<span class="tag">${{escapeHtml(a)}}</span>`).join('')}}</div></div>`;
  }}

  if (d.wasted_context && d.wasted_context.length > 0) {{
    html += `<div class="diagnosis-section"><h3>Wasted Context (candidates for pruning)</h3>
      <div style="margin-top:8px">${{d.wasted_context.map(a => `<span class="tag" style="border-color:var(--red)">${{escapeHtml(a)}}</span>`).join('')}}</div></div>`;
  }}

  if (d.non_discriminating_assertions && d.non_discriminating_assertions.length > 0) {{
    html += `<div class="diagnosis-section"><h3>Non-Discriminating Assertions</h3>
      <p style="font-size:13px;color:var(--text-dim);margin-bottom:8px">These assertions pass (or fail) equally with and without the harness — they don't measure harness value.</p>
      <ul style="list-style:none">${{d.non_discriminating_assertions.map(a => `<li style="padding:4px 0;font-size:13px">• ${{escapeHtml(a)}}</li>`).join('')}}</ul></div>`;
  }}

  if (d.recommendations && d.recommendations.length > 0) {{
    html += `<div class="diagnosis-section"><h3>Recommendations</h3>
      <ul style="list-style:none">${{d.recommendations.map(r => `<li style="padding:6px 0;font-size:14px;border-bottom:1px solid var(--border)">→ ${{escapeHtml(r)}}</li>`).join('')}}</ul></div>`;
  }}

  panel.innerHTML = html;
}}

// Keyboard nav
document.addEventListener('keydown', e => {{
  if (e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowLeft') renderEval(Math.max(0, currentIdx - 1));
  if (e.key === 'ArrowRight') renderEval(Math.min(EVALS.length - 1, currentIdx + 1));
}});

// Init
if (EVALS.length > 0) renderEval(0);
renderBenchmark();
renderDiagnosis();
</script>
</body>
</html>"""


class FeedbackHandler(BaseHTTPRequestHandler):
    """HTTP handler that serves the HTML and accepts feedback POSTs."""

    def __init__(self, html: str, workspace: Path, *args, **kwargs):
        self.html = html
        self.workspace = workspace
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self.html.encode("utf-8"))

    def do_POST(self):
        if self.path == "/feedback":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            feedback_path = self.workspace / "feedback.json"
            feedback_path.write_bytes(data)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"saved"}')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress request logging


def serve(html: str, workspace: Path, port: int = 8347):
    """Serve the viewer and open in browser."""
    handler = partial(FeedbackHandler, html, workspace)
    server = HTTPServer(("localhost", port), handler)
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))

    url = f"http://localhost:{port}"
    print(f"Context Eval Viewer: {url}", file=sys.stderr)
    print(f"Feedback saves to: {workspace / 'feedback.json'}", file=sys.stderr)
    print("Press Ctrl+C to stop.", file=sys.stderr)

    webbrowser.open(url)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Generate context eval viewer")
    parser.add_argument("workspace", help="Path to iteration workspace directory")
    parser.add_argument("--harness-name", default="harness", help="Name of the harness")
    parser.add_argument("--benchmark", default=None, help="Path to context_eval_report.json or benchmark.json")
    parser.add_argument("--previous-workspace", default=None, help="Path to previous iteration workspace")
    parser.add_argument("--static", default=None, help="Write standalone HTML to this path instead of starting a server")
    parser.add_argument("--port", type=int, default=8347, help="Port for server mode")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"Error: {workspace} does not exist", file=sys.stderr)
        sys.exit(1)

    evals = discover_evals(workspace)
    if not evals:
        print(f"Warning: No eval results found in {workspace}", file=sys.stderr)

    benchmark = load_benchmark(Path(args.benchmark)) if args.benchmark else None
    # Also try loading from workspace
    if not benchmark:
        for name in ["context_eval_report.json", "benchmark.json"]:
            p = workspace / name
            if p.exists():
                benchmark = load_benchmark(p)
                break

    previous = load_previous(Path(args.previous_workspace)) if args.previous_workspace else None

    is_static = args.static is not None
    html = generate_html(evals, args.harness_name, benchmark, previous, static=is_static)

    if is_static:
        Path(args.static).write_text(html, encoding="utf-8")
        print(f"Static viewer written to: {args.static}", file=sys.stderr)
    else:
        serve(html, workspace, args.port)


if __name__ == "__main__":
    main()
