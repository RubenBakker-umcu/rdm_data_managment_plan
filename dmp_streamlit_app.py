```python
# dmp_streamlit_app.py
import streamlit as st
from io import BytesIO
from datetime import datetime

# PDF generation with ReportLab (no extra pip deps needed on Streamlit Cloud)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

st.set_page_config(page_title="DMP Assignment", layout="centered")
st.title("Data Management Plan (DMP)")

st.markdown("""
Please read the briefing on Brightspace carefully and complete each section below.
Word limits are enforced. When all sections are finished, use **Download PDF** to get your submission file for upload to Brightspace.

This Streamlit app is new to the course team. Feedback on your experience is appreciated.
""")

st.markdown("""
#### Important notes
- There is **no autosave**. Draft your answers first in a text editor or document tool.
- This is a **fictional scenario**: you are not required to actually run the analyses.
- Practical data exercises will take place mainly on **CoCalc**, not here.
""")

# ---------- Helpers ----------
def word_count(text: str) -> int:
    return len(text.split())

def text_section(label: str, max_words: int):
    text = st.text_area(label, height=150)
    wc = word_count(text)
    st.caption(f"Word count: {wc} / {max_words}")
    ok = wc <= max_words
    if not ok:
        st.warning("Word limit exceeded. Please shorten your response.")
    return text, ok

def build_pdf_bytes(sections: dict) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )
    styles = getSampleStyleSheet()
    heading = styles["Heading1"]
    subhead = styles["Heading3"]
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        leading=14,
        spaceAfter=6,
    )

    story = []
    story.append(Paragraph("Data Management Plan Submission", heading))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 12))

    for title, content in sections.items():
        story.append(Paragraph(title, subhead))
        txt = (content or "").strip() or "[No response provided]"
        story.append(Paragraph(txt, body))
        story.append(Spacer(1, 10))

    doc.build(story)
    return buf.getvalue()

# ---------- Form ----------
with st.form("dmp_form", clear_on_submit=False):
    sections = {}
    oks = []

    st.subheader("1. Data Description (max 150 words)")
    st.write("Describe the type of data you will collect, the format, and approximate volume.")
    sections["Data Description"], ok1 = text_section("Data Description", 150); oks.append(ok1)

    st.subheader("2. Storage and Backup (max 150 words)")
    st.write("Where will you store your data, how often will it be backed up, and by whom?")
    sections["Storage and Backup"], ok2 = text_section("Storage and Backup", 150); oks.append(ok2)

    st.subheader("3. Access and Security (max 150 words)")
    st.write("Who can access which parts of the data, under what conditions? How will sensitive data be protected?")
    sections["Access and Security"], ok3 = text_section("Access and Security", 150); oks.append(ok3)

    st.subheader("4. Long-term Preservation (max 150 words)")
    st.write("What data will be preserved after the project, for how long, and where will it be stored?")
    sections["Long-term Preservation"], ok4 = text_section("Long-term Preservation", 150); oks.append(ok4)

    st.subheader("5. Roles and Responsibilities (max 150 words)")
    st.write("What will be your role and those of the other team members? Refer to the team section above.")
    sections["Roles and Responsibilities"], ok5 = text_section("Roles and Responsibilities", 150); oks.append(ok5)

    st.subheader("6. Rank the following topics from easiest to hardest")
    st.write("Data Description, Storage and Backup, Access and Security, Long-term Preservation, Roles and Responsibilities")
    sections["Topic Ranking"] = st.text_input("Write the topics in order: easiest → hardest")
    oks.append(True)  # no limit

    st.subheader("7. What was the hardest topic to plan for, and why? (max 50 words)")
    sections["Hardest Topic Reflection"], ok7 = text_section("Hardest Topic Reflection", 50); oks.append(ok7)

    st.subheader("8. What was the easiest topic to plan for, and why? (max 50 words)")
    sections["Easiest Topic Reflection"], ok8 = text_section("Easiest Topic Reflection", 50); oks.append(ok8)

    st.subheader("9. What would you ask a peer reviewer advice on, and why? (max 50 words)")
    sections["Peer Review Question"], ok9 = text_section("Peer Review Question", 50); oks.append(ok9)

    st.subheader("10. Have you used generative AI or LLM tools for this assignment? If so, how? (max 50 words)")
    sections["LLM Acknowledgement"], ok10 = text_section("LLM Acknowledgement", 50); oks.append(ok10)

    within_limits = all(oks)
    submitted = st.form_submit_button("Prepare PDF")

if submitted:
    if not within_limits:
        st.error("One or more sections exceed the word limit. Please revise your answers before exporting.")
    else:
        pdf_bytes = build_pdf_bytes(sections)
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="dmp_submission.pdf",
            mime="application/pdf"
        )
```
