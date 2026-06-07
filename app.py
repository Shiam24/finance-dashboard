import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
import datetime

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Finance X SaaS", layout="wide")

# ================= LOGIN SYSTEM =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>💰 Finance X Login</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "shiam" and password == "shiam123":
            st.session_state.logged_in = True
            st.success("Login Success 🚀")
            st.rerun()
        else:
            st.error("Invalid Credentials")

    st.stop()

# ================= PREMIUM UI =================
st.markdown("""
<style>
body {
    background-color: #0a0f1c;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #00ffd5;
}

div[data-testid="metric-container"] {
    background: #1f2937;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("💰 Finance X SaaS Dashboard")

# ================= LIVE CLOCK =================
now = datetime.datetime.now()
st.sidebar.markdown("### ⏱ Live Time")
st.sidebar.write(now.strftime("%H:%M:%S"))
st.sidebar.write(now.strftime("%d-%m-%Y"))

# ================= LOAD DATA =================
df = pd.read_csv("transactions.csv")

# ================= FILTER =================
st.sidebar.header("🔎 Filters")

filter_type = st.sidebar.selectbox("Type", ["All", "income", "expense"])

if filter_type != "All":
    df = df[df["type"] == filter_type]

# ================= ADD TRANSACTION =================
st.sidebar.header("➕ Add Transaction")

date = st.sidebar.date_input("Date")
t_type = st.sidebar.selectbox("Type", ["income", "expense"])
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount", min_value=0.0)
note = st.sidebar.text_input("Note")

if st.sidebar.button("Add Transaction"):
    new_row = pd.DataFrame([[date, t_type, category, amount, note]],
                           columns=["date","type","category","amount","note"])

    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv("transactions.csv", index=False)

    st.success("Transaction Added Successfully ✅")

# ================= CALCULATIONS =================
income = df[df["type"] == "income"]["amount"].sum()
expense = df[df["type"] == "expense"]["amount"].sum()
savings = income - expense

# ================= KPI CARDS =================
st.markdown("## 📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Income", f"₹{income}")
col2.metric("💸 Expense", f"₹{expense}")
col3.metric("📊 Savings", f"₹{savings}")

st.markdown("---")

# ================= SMART INSIGHTS =================
st.subheader("🧠 Smart Insights")

if expense > income:
    st.error("⚠️ You are spending more than earning!")
elif savings > income * 0.5:
    st.success("🔥 Excellent savings habit!")
else:
    st.info("💡 Try to reduce expenses for better savings")

# ================= TABLE =================
st.subheader("📄 Transactions Data")
st.dataframe(df)

# ================= PIE CHART =================
st.subheader("📊 Expense Breakdown")

expense_df = df[df["type"] == "expense"]
category = expense_df.groupby("category")["amount"].sum()

fig1, ax1 = plt.subplots()
ax1.pie(category, labels=category.index, autopct="%1.1f%%")
st.pyplot(fig1)

# ================= BAR CHART =================
st.subheader("📊 Category Spending")

fig2, ax2 = plt.subplots()
ax2.bar(category.index, category.values)
st.pyplot(fig2)

# ================= PDF REPORT =================
def generate_pdf(data):
    file = "finance_report.pdf"
    c = canvas.Canvas(file)

    c.drawString(100, 800, "Finance X SaaS Report")

    y = 750
    for i, row in data.iterrows():
        c.drawString(100, y, str(row.values))
        y -= 20

    c.save()
    return file

st.markdown("---")

if st.button("📤 Download PDF Report"):
    file = generate_pdf(df)
    with open(file, "rb") as f:
        st.download_button("Download Report", f, file_name=file)