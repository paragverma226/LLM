import streamlit as st
import requests

# ----------------------- App Configuration -----------------------
st.set_page_config(
    page_title="Smart Health Assistant",
    page_icon="🩺",
    layout="centered"
)

# ----------------------- Header -----------------------
st.markdown("""
    <h2 style='text-align: center; color: #2E86C1;'>🩺 Smart Health Appointment Assistant</h2>
    <p style='text-align: center; color: grey;'>Your AI-powered healthcare scheduler</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ----------------------- Input Form -----------------------
with st.form("appointment_form", clear_on_submit=False):
    patient_id = st.text_input("🆔 Patient ID", placeholder="Enter your unique patient ID")
    user_prompt = st.text_area(
        "💬 What would you like to do?",
        placeholder="E.g., Check if Dr. Smith is available tomorrow at 10 AM, or book an appointment for next Monday"
    )

    submit_btn = st.form_submit_button("📤 Submit Request")

# ----------------------- Handle Submission -----------------------
if submit_btn:
    if patient_id.strip() and user_prompt.strip():
        try:
            # Ensure patient ID is numeric
            patient_id_num = int(patient_id.strip())

            # Show loading indicator
            with st.spinner("⏳ Contacting the doctor assistant..."):
                response = requests.post(
                    url="http://127.0.0.1:8003/execute",
                    json={"messages": user_prompt, "id_number": patient_id_num},
                    verify=False
                )

            # Handle API Response
            if response.status_code == 200:
                response_data = response.json()
                assistant_reply = response_data.get("messages", "✅ Request completed, but no response returned.")

                st.success("🟢 Response received!")
                st.write(assistant_reply)

            else:
                st.error(f"❌ Server returned error {response.status_code}. Please try again later.")

        except ValueError:
            st.error("🚫 Please enter a valid numeric Patient ID.")
        except Exception as ex:
            st.error(f"⚠️ An unexpected error occurred: {ex}")

    else:
        st.warning("⚠️ Please provide both your Patient ID and request.")
