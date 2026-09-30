import os
import requests
import streamlit as st

from dotenv import load_dotenv

from backend.app.services.document_formatter import (
    create_docx,
    create_pdf,
    create_txt
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------
# CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        color: #666666;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .disclaimer {
        background-color: #fff4d6;
        border-left: 5px solid #e0a800;
        padding: 15px;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Header
# -----------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="disclaimer">
    <b>Important:</b> LegalEase generates AI-assisted draft documents.
    Always review generated content with a qualified legal professional
    before using it for an actual legal matter.
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("⚖️ LegalEase")

st.sidebar.markdown(
    """
    ### Features

    • AI legal document generation  
    • Editable document preview  
    • TXT export  
    • DOCX export  
    • PDF export  
    • Multiple document types  
    • FastAPI backend  
    • Gemini AI integration
    """
)


# -----------------------------
# Input section
# -----------------------------

st.header("Create a Legal Document")


document_types = [
    "Employment Contract",
    "Non-Disclosure Agreement",
    "Residential Lease Agreement",
    "Freelance Agreement",
    "Service Agreement",
    "Partnership Agreement",
    "Consulting Agreement",
    "Custom Legal Document"
]


document_type = st.selectbox(
    "Document Type",
    document_types
)


if document_type == "Custom Legal Document":

    custom_type = st.text_input(
        "Enter document type"
    )

    if custom_type.strip():

        document_type = custom_type.strip()


parties = st.text_area(
    "Parties Involved",
    placeholder=(
        "Example:\n"
        "Employer: ABC Technologies Pvt Ltd\n"
        "Employee: John Doe"
    ),
    height=130
)


effective_date = st.text_input(
    "Effective Date",
    placeholder="Example: 1 October 2026"
)


st.subheader("Terms and Conditions")


terms_text = st.text_area(
    "Enter important terms",
    placeholder=(
        "Enter one term per line.\n\n"
        "Example:\n"
        "Employee will work remotely.\n"
        "Monthly salary is ₹50,000.\n"
        "Notice period is 30 days.\n"
        "Confidential information must not be disclosed."
    ),
    height=180
)


additional_instructions = st.text_area(
    "Additional Instructions",
    placeholder=(
        "Optional instructions for the AI.\n"
        "Example: Make the document professional "
        "and include a signature section."
    ),
    height=120
)


terms = [
    term.strip()
    for term in terms_text.splitlines()
    if term.strip()
]


# -----------------------------
# Generate
# -----------------------------

generate_button = st.button(
    "🚀 Generate Document",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

        st.stop()

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "effective_date": effective_date,
        "additional_instructions": additional_instructions
    }

    with st.spinner(
        "Generating your legal document..."
    ):

        try:

            response = requests.post(
                f"{BACKEND_URL}/api/generate",
                json=payload,
                timeout=120
            )

            if response.status_code == 200:

                result = response.json()

                st.session_state["document"] = (
                    result["content"]
                )

                st.session_state["document_type"] = (
                    document_type
                )

                st.success(
                    "Document generated successfully!"
                )

            else:

                try:
                    error_message = response.json().get(
                        "detail",
                        response.text
                    )
                except Exception:
                    error_message = response.text

                st.error(
                    f"Backend error: {error_message}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the backend server is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. "
                "Please try again."
            )

        except Exception as exc:

            st.error(
                f"Unexpected error: {exc}"
            )


# -----------------------------
# Preview
# -----------------------------

if "document" in st.session_state:

    st.divider()

    st.header("📄 Document Preview")

    st.info(
        "You can edit the generated document before downloading it."
    )

    edited_document = st.text_area(
        "Edit Document",
        value=st.session_state["document"],
        height=600
    )

    st.session_state["document"] = edited_document

    document_type = st.session_state.get(
        "document_type",
        "Legal Document"
    )


    # -----------------------------
    # Downloads
    # -----------------------------

    st.subheader("Download Document")

    col1, col2, col3 = st.columns(3)


    txt_data = create_txt(
        edited_document
    )

    docx_data = create_docx(
        edited_document,
        document_type
    )

    pdf_data = create_pdf(
        edited_document,
        document_type
    )


    with col1:

        st.download_button(
            label="⬇️ Download TXT",
            data=txt_data,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True
        )


    with col2:

        st.download_button(
            label="⬇️ Download DOCX",
            data=docx_data,
            file_name="legalease_document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True
        )


    with col3:

        st.download_button(
            label="⬇️ Download PDF",
            data=pdf_data,
            file_name="legalease_document.pdf",
            mime="application/pdf",
            use_container_width=True
        )


    st.divider()

    st.caption(
        "LegalEase • AI-Powered Legal Document Generator"
    )