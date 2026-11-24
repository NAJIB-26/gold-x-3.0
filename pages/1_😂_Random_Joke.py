"""Random joke page backed by the Official Joke API."""

import requests
import streamlit as st


API_URL = "https://official-joke-api.appspot.com/random_joke"
REQUEST_TIMEOUT_SECONDS = 10

st.set_page_config(page_title="Random Joke Generator", page_icon="😂")
st.title("😂 Random Joke Generator")
st.write("Need a quick laugh? Fetch a random joke from an external API.")


def fetch_random_joke():
    """Fetch and validate one joke from the Official Joke API."""
    response = requests.get(API_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    joke = response.json()

    if not isinstance(joke, dict):
        raise ValueError("The joke service returned an unexpected response.")

    setup = joke.get("setup")
    punchline = joke.get("punchline")
    if not isinstance(setup, str) or not setup.strip():
        raise ValueError("The joke service did not return a setup.")
    if not isinstance(punchline, str) or not punchline.strip():
        raise ValueError("The joke service did not return a punchline.")

    return {"setup": setup.strip(), "punchline": punchline.strip()}


if "random_joke" not in st.session_state:
    st.session_state.random_joke = None

if st.button("Tell me a joke 🎲", type="primary"):
    try:
        with st.spinner("Finding a joke..."):
            st.session_state.random_joke = fetch_random_joke()
        st.session_state.joke_error = None
    except (requests.RequestException, ValueError) as error:
        st.session_state.random_joke = None
        st.session_state.joke_error = str(error)

if st.session_state.get("joke_error"):
    st.error(f"Couldn't fetch a joke right now: {st.session_state.joke_error}")
elif st.session_state.random_joke:
    joke = st.session_state.random_joke
    st.subheader(joke["setup"])
    with st.expander("Reveal the punchline"):
        st.write(joke["punchline"])
else:
    st.info("Click the button to get your first joke.")

st.caption("Jokes provided by the Official Joke API.")
