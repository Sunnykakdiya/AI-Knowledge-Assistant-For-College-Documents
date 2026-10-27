
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="College Knowledge Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 College Knowledge Assistant")
st.caption("Upload college documents and ask questions about their contents.")

# Check whether the backend is running.
try:
    response = requests.get(f"{API_URL}/health", timeout=5)
    if response.ok:
        st.success("Backend connected")
    else:
        st.warning("Backend responded with an unexpected status.")
except requests.RequestException:
    st.error("Backend is not running. Start FastAPI in another CMD window.")

st.header("1. Upload a college PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"],
)

if st.button("Upload and process PDF", disabled=uploaded_file is None):
    try:
        with st.spinner("Extracting text, creating embeddings, and saving chunks..."):
            response = requests.post(
                f"{API_URL}/api/v1/documents/upload",
                files={
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "application/pdf",
                    )
                },
                timeout=300,
            )

        if response.ok:
            result = response.json()
            st.success(result.get("message", "PDF processed successfully."))
            st.write("Chunks inserted:", result.get("chunks_inserted", 0))
        else:
            st.error(f"Upload failed ({response.status_code}).")
            st.code(response.text)

    except requests.RequestException as error:
        st.error(f"Could not upload the PDF: {error}")

st.divider()
st.header("2. Ask a question")

question = st.text_input(
    "Your question",
    placeholder="Example: What attendance is required for examinations?",
)

top_k = st.slider(
    "Number of document passages to retrieve",
    min_value=1,
    max_value=10,
    value=3,
)

if st.button("Ask", type="primary", disabled=not question.strip()):
    try:
        with st.spinner("Searching documents and generating an answer..."):
            response = requests.post(
                f"{API_URL}/api/v1/ask",
                json={"question": question, "top_k": top_k},
                timeout=600,
            )

        if response.ok:
            result = response.json()

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")
            sources = result.get("sources", [])

            if not sources:
                st.info("No document passages were returned.")

            for index, source in enumerate(sources, start=1):
                page = source.get("page_number")
                page_text = f", page {page}" if page is not None else ""

                with st.expander(
                    f"Source {index}: {source['document_name']}{page_text}"
                ):
                    st.write(source["text"])
                    st.caption(
                        f"Similarity score: {source['similarity']:.3f}"
                    )
        else:
            st.error(f"Question failed ({response.status_code}).")
            st.code(response.text)

    except requests.RequestException as error:
        st.error(f"Could not contact the backend: {error}")
