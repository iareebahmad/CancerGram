import streamlit as st
from supabase import create_client, Client

########################
# Page configuration
########################
st.set_page_config(page_title="CancerGram by Dr. Shifa Shah",layout="centered")

########################
# Supabase configuration
########################
SUPABASE_URL = "https://onybgfedxcquhuypmmds.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9ueWJnZmVkeGNxdWh1eXBtbWRzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTQ3MzI4MTIsImV4cCI6MjA3MDMwODgxMn0.NQ1e34MOXr2Oh-L7Btm21lIHC3lueASGIyg6_PCsro0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

#######################
# Session State
#######################
if "user" not in st.session_state:
    st.session_state.user = None


########################
# Login Function
########################
def show_login():
    st.subheader("Already a User? Log in Here")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pwd")

    if st.button("Login"):
        try:
            # Sign in using Supabase Auth
            auth_response = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if auth_response.user:
                user_id = auth_response.user.id

                # Update last_login timestamp in profiles table
                try:
                    supabase.table("profiles").update({
                        "last_login": "now()"
                    }).eq("id", user_id).execute()
                except Exception as update_err:
                    st.warning(f"Logged in but could not update last_login: {update_err}")

                # Store user in session
                st.session_state.user = auth_response.user
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid login credentials")

        except Exception as e:
            st.error(f"Error: {e}")



########################
# Register Function
########################
def show_register():
    st.subheader("New User? Register Here")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_pwd")
    confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        try:
            # Sign up with Supabase Auth
            auth_response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if auth_response.user:
                user_id = auth_response.user.id

                # Insert into profiles table in Supabase
                try:
                    supabase.table("profiles").insert({
                        "id": user_id,
                        "email": email
                    }).execute()
                except Exception as insert_err:
                    st.warning(f"User registered but could not insert into profiles: {insert_err}")

                st.success("Account created! Please verify your account using the link sent to your email.")
            else:
                st.error("Could not register. Try again.")

        except Exception as e:
            st.error(f"Error: {e}")


########################
# Main App
########################
def main_app():
    st.text("Advanced Cancer Detection using Cutting Edge AI for Better Accuracy")

    st.subheader("Upload Your Data for Analysis")

    # Genomic Expression CSV
    genomic_csv = st.file_uploader(
        "Upload Genomic Expression Data (CSV)",
        type=["csv"],
        key="genomic_csv"
    )

    # Clinical Data CSV
    clinical_csv = st.file_uploader(
        "Upload Clinical Data (CSV)",
        type=["csv"],
        key="clinical_csv"
    )

    # Image Data
    image_file = st.file_uploader(
        "Upload Image Data & Scans (JPG/JPEG/PNG)",
        type=["jpg", "jpeg", "png"],
        key="image_data"
    )

    # Optional: Display confirmation
    if st.button("Submit Data"):
        if not genomic_csv or not clinical_csv or not image_file:
            st.error("Please upload all required files before submitting.")
        else:
            st.success("Files uploaded successfully! Processing will start shortly.")
            # Processing logic can be added here

    # Sidebar post login
    with st.sidebar:
        st.subheader("CancerGram")
        if st.session_state.user:
            st.markdown(
                f"""
                <p style="color:#B57EDC; 
                          font-family: 'Trebuchet MS', sans-serif; 
                          font-size: 16px;">
                    Logged in as: {st.session_state.user.email}
                </p>
                """,
                unsafe_allow_html=True
            )
            if st.button("Logout"):
                st.session_state.user = None
                st.rerun()


########################
# App Flow
########################
st.title("CancerGram")

if st.session_state.user:
    main_app()
else:
    with st.sidebar:
        st.subheader("CancerGram")
        st.info("Please log in or register to continue.")

    login_tab_obj, register_tab_obj = st.tabs(["Login", "Register"])
    with login_tab_obj:
        show_login()
    with register_tab_obj:
        show_register()

########################
# Footer
########################

st.markdown("---")
st.markdown(
        '<p style="text-align:center;">Made by Dr. Shifa Shah</p>',
        unsafe_allow_html=True
    )