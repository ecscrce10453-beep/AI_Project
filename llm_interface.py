import os
from openai import OpenAI

# -------------------------------------------------
# MAIN FUNCTION (Streamlit calls THIS)
# -------------------------------------------------
def generate_tests_from_code(prompt, backend="local", temperature=0.3, max_tokens=800):
    backend = backend.lower().strip()

    if "openai" in backend:
        return _openai_generate(prompt, temperature, max_tokens)
    else:
        return _local_transformer_generate(prompt, temperature, max_tokens)


# -------------------------------------------------
# OPENAI BACKEND (New API)
# -------------------------------------------------
def _openai_generate(prompt, temperature, max_tokens):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY in environment to use OpenAI backend")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        # NEW SDK returns objects, not dicts
        return response.choices[0].message.content

    except Exception as e:
        raise RuntimeError(f"OpenAI Error: {e}")


# -------------------------------------------------
# LOCAL TRANSFORMER BACKEND
# -------------------------------------------------
def _local_transformer_generate(prompt, temperature, max_tokens):
    try:
        from transformers import pipeline
    except ImportError:
        raise RuntimeError(
            "Install transformers → pip install transformers torch"
        )

    model_name = os.getenv("LOCAL_LLM_MODEL", "gpt2")

    try:
        generator = pipeline("text-generation", model=model_name)
        output = generator(
            prompt,
            max_length=min(max_tokens, 1024),
            temperature=temperature,
            num_return_sequences=1
        )

        text = output[0]["generated_text"]

        # Remove prompt echo
        if text.startswith(prompt):
            text = text[len(prompt):]

        return text.strip()

    except Exception as e:
        raise RuntimeError(f"Local LLM Error: {e}")