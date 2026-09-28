import importlib.util
import os

import streamlit as st
from streamlit_molstar import st_molstar_rcsb

# ---------------------------------------------------------------------------
# Load 02_mutation_engine.py (a normal import fails: filename starts with a digit)
# ---------------------------------------------------------------------------
_engine_path = os.path.join(os.path.dirname(__file__), "02_mutation_engine.py")
_spec = importlib.util.spec_from_file_location("mutation_engine", _engine_path)
mutation_engine = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mutation_engine)

fetch_sequence = mutation_engine.fetch_sequence
get_mutations = mutation_engine.get_mutations

st.set_page_config(page_title="FemTech Genomic Explorer", layout="wide")

if "fullscreen" not in st.session_state:
    st.session_state.fullscreen = False

# ---------------------------------------------------------------------------
# Data: targets, risk explanations per severity tier, legal notes
# ---------------------------------------------------------------------------
targets = {
    "1QKM": {"name": "Estrogen Receptor"},
    "1A28": {"name": "Progesterone Receptor"},
    "5IKQ": {"name": "COX-2 Enzyme"},
    "4BS0": {"name": "Aromatase (CYP19A1)"},
    "1Y6A": {"name": "TNF-alpha"},
}

target_risk_info = {
    "1QKM": {
        "no_risk": "No variation from the reference estrogen receptor sequence. Estrogen signaling is expected to function within its typical range.",
        "moderate_risk": "A small number of changes in the estrogen receptor sequence. May subtly alter hormone-binding affinity, potentially affecting how lesion tissue responds to estrogen.",
        "high_risk": "Substantial divergence from the reference estrogen receptor sequence. May significantly disrupt the ligand-binding domain, with possible impact on hormone sensitivity and lesion growth response.",
    },
    "1A28": {
        "no_risk": "No variation from the reference progesterone receptor sequence. Normal progesterone responsiveness is expected.",
        "moderate_risk": "A small number of changes in the progesterone receptor sequence. May contribute to partial progesterone resistance patterns seen in some endometriosis cases.",
        "high_risk": "Substantial divergence from the reference progesterone receptor sequence. May indicate significant progesterone resistance, a factor linked to reduced response to progestin-based therapy.",
    },
    "5IKQ": {
        "no_risk": "No variation from the reference COX-2 sequence. Prostaglandin production is expected to be typical.",
        "moderate_risk": "A small number of changes in the COX-2 sequence. May moderately affect prostaglandin production linked to inflammation and pain signaling.",
        "high_risk": "Substantial divergence from the reference COX-2 sequence. May significantly alter enzyme activity, with possible impact on inflammatory pain severity.",
    },
    "4BS0": {
        "no_risk": "No variation from the reference aromatase sequence. Local estrogen synthesis is expected to be typical.",
        "moderate_risk": "A small number of changes in the aromatase sequence. May moderately affect local estrogen production within lesion tissue.",
        "high_risk": "Substantial divergence from the reference aromatase sequence. May significantly increase local estrogen synthesis, independent of ovarian hormone levels.",
    },
    "1Y6A": {
        "no_risk": "No variation from the reference TNF-alpha sequence. Inflammatory signaling is expected to be typical.",
        "moderate_risk": "A small number of changes in the TNF-alpha sequence. May moderately affect inflammatory signaling linked to adhesion and tissue irritation.",
        "high_risk": "Substantial divergence from the reference TNF-alpha sequence. May significantly heighten inflammatory response, contributing to fibrosis and chronic adhesion formation.",
    },
}

target_legal_notes = {
    "1QKM": "Genetic Privacy & Insurance Law: sensitive information under the Privacy Act 1988 (Cth); subject to the FSC genetic testing moratorium in life insurance underwriting.",
    "1A28": "Genetic Relative Disclosure: s.95AA of the Privacy Act 1988 (Cth) governs disclosure to genetic relatives without consent.",
    "5IKQ": "Product Liability: COX-2 inhibitors carry significant tort history, notably the Vioxx litigation over undisclosed cardiovascular risk.",
    "4BS0": "Gene Patentability: naturally occurring sequences are not patentable subject matter per D'Arcy v Myriad Genetics Inc (2015).",
    "1Y6A": "Biologics & Patent Law: TNF-alpha inhibitor biologics are subject to extensive 'patent thicket' litigation delaying biosimilar competition.",
}


def get_severity(mutation_count):
    """0 -> no risk, 1-2 -> moderate risk, more than 2 -> high risk."""
    if mutation_count == 0:
        return "no_risk", "No Risk"
    elif 1 <= mutation_count <= 2:
        return "moderate_risk", "Moderate Risk"
    else:
        return "high_risk", "High Risk"


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown("## FEMTECH GENOMIC EXPLORER")
st.caption("*A non-invasive computational screening prototype for endometriosis-related protein targets.*")
st.warning(
    "**About this project:** This is a demonstration application built for a "
    "scholarship portfolio. It uses public structural data from the RCSB "
    "Protein Data Bank (rcsb.org) and sample sequences, not real patient "
    "data. It is not a diagnostic device and does not provide medical advice."
)
st.divider()

# ---------------------------------------------------------------------------
# Sidebar (hideable with the built-in collapse arrow)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader("Select Target")
    selected_target = st.radio(
        "Target",
        list(targets.keys()),
        format_func=lambda k: targets[k]["name"],
        label_visibility="collapsed",
    )
    st.divider()
    st.subheader("Enter Patient Sequence")
    patient_sequence = st.text_area("Paste amino acid sequence", height=150)
    run_analysis = st.button("Run Mutation Check")

# ---------------------------------------------------------------------------
# Main area: fullscreen focus mode OR normal 3-panel layout
# ---------------------------------------------------------------------------
if st.session_state.fullscreen:
    if st.button("◀ Exit Fullscreen"):
        st.session_state.fullscreen = False
        st.rerun()

    st.subheader(f"{targets[selected_target]['name']} — 3D Structure")
    st_molstar_rcsb(selected_target, key=f"molstar_full_{selected_target}")

else:
    col_viewer, col_data = st.columns([2, 1])

    # ---- Left: 3D viewer with expand button ----
    with col_viewer:
        header_col, btn_col = st.columns([4, 1])
        with header_col:
            st.subheader("3D Protein Structure")
        with btn_col:
            if st.button("⛶ Expand"):
                st.session_state.fullscreen = True
                st.rerun()

        st_molstar_rcsb(selected_target, key=f"molstar_{selected_target}")

    # ---- Right: results panel ----
    with col_data:
        mutation_score = 0
        mutation_positions = []

        if run_analysis and patient_sequence.strip():
            try:
                with st.spinner("Fetching reference sequence and comparing..."):
                    wild_type_seq = fetch_sequence(selected_target)
                    clean_sequence = patient_sequence.strip().upper()
                    mutations = get_mutations(wild_type_seq, clean_sequence)

                mutation_score = len(mutations)
                mutation_positions = [m["notation"] for m in mutations]

            except Exception as exc:
                st.error(f"Could not complete analysis: {exc}")

        st.markdown(f"**Mutation score:** {mutation_score}")
        st.markdown(
            f"**Positions log:** {', '.join(mutation_positions) if mutation_positions else '[]'}"
        )

        severity_key, severity_label = get_severity(mutation_score)
        risk_text = target_risk_info[selected_target][severity_key]

        severity_style = {
            "no_risk": (st.success, "🟢"),
            "moderate_risk": (st.warning, "🟠"),
            "high_risk": (st.error, "🔴"),
        }
        display_fn, icon = severity_style[severity_key]

        display_fn(f"**Predicted biological effects**\n\n{risk_text}")
        st.markdown(f"{icon} **Severity: {severity_label}**")

    # ---- Bottom: regulatory footnote ----
    st.divider()
    st.caption(f"**Regulatory framework:** {target_legal_notes[selected_target]}")