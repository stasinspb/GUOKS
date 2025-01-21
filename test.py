import streamlit as st
import os
st.write(os.listdir())
# Initialize session state
st.session_state.text = st.session_state.get('text', 'original')

if st.button("show"):
    # Allow the user to modify the text
    st.text_input("Edit Text", key='text')        # <--- set using the key kwarg

# Display the modified text
st.markdown(st.session_state.text)

if st.button("show again"):
    # Display the modified text
    st.markdown(st.session_state.text)
