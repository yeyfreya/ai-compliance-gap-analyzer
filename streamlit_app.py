"""
AI Compliance Gap Analyzer — Streamlit UI
Live demo interface for the compliance analysis pipeline.
"""

import os
import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime

# Streamlit Cloud: inject secrets as env vars before importing agent modules,
# which create API clients at module level using os.getenv().
# Locally, .env is loaded by agent.py via dotenv — this block is a no-op.
_missing = []
for _key in ("ANTHROPIC_API_KEY", "TAVILY_API_KEY"):
    if _key not in os.environ:
        try:
            os.environ[_key] = st.secrets[_key]
        except (KeyError, FileNotFoundError):
            _missing.append(_key)

if _missing:
    st.error(
        f"Missing API keys: **{', '.join(_missing)}**. "
        "Add them in Streamlit Cloud → Settings → Secrets (TOML format), "
        "or in a local `.env` file."
    )
    st.code('ANTHROPIC_API_KEY = "<your-anthropic-key>"\nTAVILY_API_KEY = "<your-tavily-key>"', language="toml")
    st.stop()

from agent import (
    plan_searches,
    conduct_research,
    analyze_compliance,
    save_report,
    append_test_log,
    TEST_SCENARIOS,
)

VERSION = "v0.3"

st.set_page_config(
    page_title="AI Compliance Gap Analyzer",
    page_icon="🛡️",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .block-container { max-width: 960px; }

    /* Hero headline */
    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .hero-sub {
        font-size: 1.05rem;
        opacity: 0.75;
        margin-bottom: 1.5rem;
    }

    /* Metric cards row */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        flex: 1;
        padding: 0.85rem 1rem;
        border-radius: 10px;
        background: rgba(128,128,128,0.08);
        text-align: center;
    }
    .metric-card .label { font-size: 0.78rem; opacity: 0.6; }
    .metric-card .value { font-size: 1.3rem; font-weight: 600; }

    /* Sidebar polish */
    [data-testid="stSidebar"] { min-width: 340px; }

    /* Divider */
    hr { margin: 1.5rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Session-state defaults ────────────────────────────────────────────────────
for key in ("result", "report_md", "report_path"):
    if key not in st.session_state:
        st.session_state[key] = None


# ── Sidebar — inputs ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Configuration")

    scenario_options = {"— Custom —": None} | {
        f"{k.title()} — {v['use_case'][:40]}": k
        for k, v in TEST_SCENARIOS.items()
    }
    chosen_label = st.selectbox("Quick-start scenario", list(scenario_options.keys()))
    chosen_key = scenario_options[chosen_label]

    if chosen_key:
        s = TEST_SCENARIOS[chosen_key]
        use_case = st.text_area("Use case", value=s["use_case"], height=80)
        technology = st.text_input("Technology", value=s["technology"])
        industry = st.text_input("Industry", value=s["industry"])
    else:
        use_case = st.text_area(
            "Use case",
            placeholder="e.g. AI-powered resume screening tool",
            height=80,
        )
        technology = st.text_input(
            "Technology", placeholder="e.g. OpenAI GPT-4 API"
        )
        industry = st.text_input(
            "Industry", placeholder="e.g. Enterprise HR (US-based)"
        )

    st.divider()
    run_btn = st.button("Run Analysis", type="primary", use_container_width=True)

    st.divider()
    st.caption(
        f"{VERSION} · Built with Claude + Tavily · "
        "[GitHub](https://github.com/yeyfreya/ai-compliance-gap-analyzer)"
    )


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="hero-title">🛡️ AI Compliance Gap Analyzer</div>'
    '<div class="hero-sub">'
    "Enter an AI use case, technology, and industry — the agent researches "
    "regulations, identifies gaps, and generates a compliance report."
    "</div>",
    unsafe_allow_html=True,
)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    # Validate inputs
    missing = [
        name
        for name, val in [("Use case", use_case), ("Technology", technology), ("Industry", industry)]
        if not val or not val.strip()
    ]
    if missing:
        st.error(f"Please fill in: **{', '.join(missing)}**")
        st.stop()

    st.session_state.result = None
    st.session_state.report_md = None
    st.session_state.report_path = None

    total_start = time.time()

    status_area = st.container()
    timer_slot = st.empty()

    with status_area:
        with st.status("Running compliance analysis… (step 1/3)", expanded=True) as status:

            # Start the live JS timer below the status block
            with timer_slot.container():
                components.html(
                    """
                    <div style="display:flex; align-items:center; gap:0.6rem;
                                font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                                padding:0.25rem 0 0.5rem; color:#FAFAFA;">
                        <span style="font-size:1.1rem;">⏱️</span>
                        <span style="font-variant-numeric:tabular-nums; font-weight:600;"
                              id="elapsed">0:00</span>
                        <span style="opacity:0.55; font-size:0.88rem;">
                            · This usually takes 2–3 minutes
                        </span>
                    </div>
                    <script>
                        const start = Date.now();
                        const el = document.getElementById('elapsed');
                        setInterval(() => {
                            const sec = Math.floor((Date.now() - start) / 1000);
                            const m = Math.floor(sec / 60);
                            const s = sec % 60;
                            el.textContent = m + ':' + (s < 10 ? '0' : '') + s;
                        }, 1000);
                    </script>
                    """,
                    height=40,
                )

            # Step 1 — Plan searches
            st.write("📋 **Planning research strategy** — asking Claude what to investigate…")
            t0 = time.time()
            search_queries = plan_searches(use_case, technology, industry)
            time_planning = round(time.time() - t0, 1)
            st.write(f"✅ Planned **{len(search_queries)}** search queries ({time_planning}s)")

            status.update(label="Running compliance analysis… (step 2/3)")

            # Step 2 — Conduct research
            st.write("🔬 **Conducting research** — searching the web via Tavily…")
            t0 = time.time()
            research_findings = conduct_research(search_queries)
            time_research = round(time.time() - t0, 1)
            st.write(f"✅ Research complete ({time_research}s)")

            status.update(label="Running compliance analysis… (step 3/3)")

            # Step 3 — Analyze compliance (longest step: ~60-100s)
            st.write(
                "🧠 **Analyzing compliance gaps** — Claude is writing the report. "
                "This is the longest step…"
            )
            t0 = time.time()
            analysis = analyze_compliance(use_case, technology, industry, research_findings)
            time_analysis = round(time.time() - t0, 1)
            st.write(f"✅ Analysis complete ({time_analysis}s)")

            time_total = round(time.time() - total_start, 1)
            status.update(label=f"Analysis complete — {time_total}s", state="complete", expanded=False)

    # Replace the live timer with a static completion message
    mins, secs = divmod(int(time_total), 60)
    timer_slot.markdown(f"⏱️ Report generated in **{mins}:{secs:02d}**")

    timing = {
        "planning_sec": time_planning,
        "research_sec": time_research,
        "analysis_sec": time_analysis,
        "total_sec": time_total,
    }

    result = {
        "use_case": use_case,
        "technology": technology,
        "industry": industry,
        "search_queries": search_queries,
        "analysis": analysis,
        "timing": timing,
    }

    report_path = save_report(result, version=VERSION)
    append_test_log(result, version=VERSION, report_path=report_path)

    st.session_state.result = result
    st.session_state.report_path = report_path

    with open(report_path, "r", encoding="utf-8") as f:
        st.session_state.report_md = f.read()


# ── Display results ───────────────────────────────────────────────────────────
result = st.session_state.result
if result:
    timing = result["timing"]

    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-card">
                <div class="label">Total time</div>
                <div class="value">{timing['total_sec']}s</div>
            </div>
            <div class="metric-card">
                <div class="label">Planning</div>
                <div class="value">{timing['planning_sec']}s</div>
            </div>
            <div class="metric-card">
                <div class="label">Research</div>
                <div class="value">{timing['research_sec']}s</div>
            </div>
            <div class="metric-card">
                <div class="label">Analysis</div>
                <div class="value">{timing['analysis_sec']}s</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_report, tab_queries = st.tabs(["📄 Report", "🔍 Search Queries"])

    with tab_report:
        st.markdown(result["analysis"])

    with tab_queries:
        for i, q in enumerate(result["search_queries"], 1):
            st.markdown(f"**{i}.** {q}")

    st.divider()

    col_dl, col_path = st.columns([1, 3])
    with col_dl:
        st.download_button(
            "⬇️ Download Report (.md)",
            data=st.session_state.report_md,
            file_name=os.path.basename(st.session_state.report_path),
            mime="text/markdown",
        )
    with col_path:
        st.caption(f"Saved to `{st.session_state.report_path}`")

elif not run_btn:
    st.info(
        "Configure your analysis in the sidebar and click **Run Analysis** to start.",
        icon="👈",
    )
