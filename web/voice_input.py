import requests
import streamlit as st


def voice_to_chat(backend_url, timeout, fetch_ekm_data, ekm_model):

    audio = st.audio_input("🎤 Record voice")

    if audio is None:
        return

    audio_bytes = audio.getvalue()

    # prevent repeated processing of same recording
    if st.session_state.get("last_audio") == audio_bytes:
        return

    st.session_state.last_audio = audio_bytes

    files = {
        "file": ("audio.wav", audio_bytes, "audio/wav")
    }

    r = requests.post(
        f"{backend_url}/voice",
        files=files,
        timeout=timeout
    )

    if r.status_code != 200:
        return

    transcript = r.json()["text"]

    st.session_state.messages.append(
        {"role": "user", "content": transcript}
    )

    reply = fetch_ekm_data(
        backend_url,
        timeout,
        ekm_model,
        st.session_state.messages
    )

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()