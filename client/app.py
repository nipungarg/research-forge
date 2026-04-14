import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000"

st.title("🔍 Research Forge")

# ------------------------
# INPUT
# ------------------------
query = st.text_input("Enter your research question:")

if st.button("Start Research"):
    if not query:
        st.warning("Please enter a query")
    else:
        response = requests.post(
            f"{API_URL}/research/start",
            json={"query": query}
        )

        if response.status_code != 200:
            st.error("Failed to start job")
        else:
            job_id = response.json()["job_id"]
            st.session_state["job_id"] = job_id
            st.toast(f"Job started: {job_id}", icon="✅")


# ------------------------
# POLLING
# ------------------------
if "job_id" in st.session_state:
    job_id = st.session_state["job_id"]

    st.subheader("📊 Job Status")

    status_placeholder = st.empty()
    result_placeholder = st.empty()
    logs_placeholder = st.empty()

    while True:
        res = requests.get(f"{API_URL}/research/{job_id}")

        if res.status_code != 200:
            st.error("Error fetching job")
            break

        data = res.json()
        status = data["status"]

        status_placeholder.info(f"Status: {status}")

        # Fetch logs
        logs_res = requests.get(f"{API_URL}/research/{job_id}/logs")
        if logs_res.status_code == 200:
            logs = logs_res.json()["logs"]
            logs_placeholder.text("\n".join(logs[-10:]))

        if status == "completed":
            result = data["result"]

            result_placeholder.success("✅ Research Completed")
            st.markdown("### 📝 Final Answer")
            st.write(result["answer"])

            st.markdown("### 📈 Metrics")
            st.json({
                "iterations": result["iterations"],
                "llm_calls": result["llm_calls"]
            })

            break

        elif status == "failed":
            st.error("❌ Job Failed")
            break

        time.sleep(2)