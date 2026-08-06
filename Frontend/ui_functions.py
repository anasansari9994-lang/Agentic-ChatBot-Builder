import streamlit as st
from auth.auth_manager import Authentication

def render_auth_page():
    st.markdown("<h1 style='text-align: center;'>⚡ Autonomous AI Research Platform</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Advanced Multi-Agent Knowledge Extraction Node</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        tab_login , tab_sign_up = st.tabs(["Login", "Sign up"])

        with tab_login:
            email = st.text_input("Email", key="auth_email")
            password = st.text_input("Password", type="password", key="auth_pass")
            login_disable = not (email and password)
            if st.button("Autnetication" , type="primary" , use_container_width=True , disabled=login_disable):
                with st.spinner("Verifying credentials..."):
                    res = Authentication.log_in(email , password)
                    if res["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user_email = email
                        st.session_state.user_uuid = res["user_uuid"]
                        st.success("JWT Token Verified. Initializing Platform Workspace...")
                        st.rerun()
                    else:
                        st.error(f"Access Denied: {res['error']}")

        with tab_sign_up:
            new_name = st.text_input("Full Name", key = "sign_name")
            new_email = st.text_input("email", key="sign_email")
            new_password = st.text_input("Password", type="password", key="sign_pass")

            if st.button("Register Workplaces" , use_container_width=True):
                if new_name and new_email and new_password:
                    try:
                        res = Authentication.sign_up(email=new_email , password=new_password , full_name=new_name)
                        st.success("Account compiled! Verification email sent please verify")
                    except Exception as e:
                        st.error(f"Compilation Error: {e}")

                else:
                    st.warning("All environment registry inputs are mandatory.")