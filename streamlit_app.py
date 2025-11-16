import streamlit as st
from llm_interface import generate_tests_from_code
import tempfile, os, subprocess

st.set_page_config(page_title="LLM Unit Test Generator", layout="centered")
st.title("AI-Based Unit Test Generator (LLM Powered)")
st.write("Paste Python code or upload a file. The AI will generate pytest unit tests.")

code_input = st.text_area("Paste Python code:", height=260)
uploaded_file = st.file_uploader("Or upload a .py file", type=["py"])

if uploaded_file is not None:
    code_input = uploaded_file.read().decode("utf-8")

col1, col2 = st.columns(2)
with col1:
    backend = st.selectbox("Choose LLM Backend", ["openai (api)", "local (transformers)"])
with col2:
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3)

max_tokens = st.slider("Max Tokens", 128, 2000, 800)

# --- GENERATE BUTTON ---
if st.button("Generate Unit Tests"):
    if not code_input.strip():
        st.error("Please paste python code first!")
    else:
        st.info("Generating tests using AI model...")

        # ⭐ Updated SMART prompt
        prompt = f"""
You are an AI unit test generator. Generate high-quality pytest test cases 
for the following Python code.

IMPORTANT REQUIREMENTS:
- Automatically detect ALL FUNCTIONS and ALL CLASSES from the code.
- Add correct import line at the top, like:
  from code_under_test import <all functions/classes>
- Tests must be executable with pytest.
- Include edge cases, exceptions, boundary values, negative tests.
- ONLY output raw Python test code.
- DO NOT include markdown.
- DO NOT include ```python or ``` anywhere.
- DO NOT include explanations.

CODE UNDER TEST:
{code_input}
"""

        try:
            tests = generate_tests_from_code(
                prompt,
                backend=backend,
                temperature=float(temperature),
                max_tokens=int(max_tokens),
            )
        except Exception as e:
            st.error(f"LLM Error: {e}")
            tests = None

        if tests:
            st.success("Tests generated successfully!")
            st.code(tests, language="python")

            # SAVE & RUN TESTS
            tmpdir = tempfile.mkdtemp()
            code_path = os.path.join(tmpdir, "code_under_test.py")
            test_path = os.path.join(tmpdir, "test_generated.py")

            with open(code_path, "w") as f:
                f.write(code_input)

            with open(test_path, "w") as f:
                f.write(tests)

            st.subheader("Running Tests (pytest)...")
            try:
                result = subprocess.run(
                    ["pytest", "-q", test_path],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=25
                )
                output = result.stdout + "\n" + result.stderr
                st.text_area("Pytest Output:", output, height=300)
            except Exception as e:
                st.error(f"Pytest execution failed: {e}")

            st.download_button(
                label="Download Generated Test File",
                data=tests,
                file_name="test_generated.py",
                mime="text/x-python"
            )
