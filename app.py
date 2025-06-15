import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page config ---
st.set_page_config(page_title="Customer Insights Dashboard", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    return pd.read_csv("Banking Data Set - Marketing.csv")

df = load_data()

# --- Sidebar Navigation ---
pages = ["KPIs", "Customer Demographics", "Monthly Financial Behaviour", "Credit Payment & Loan Behaviour"]
selection = st.sidebar.radio("Navigation", pages)

# --- KPIs ---
if selection == "KPIs":
    st.title("📊 Key Performance Indicators")
    # Compute all KPIs
    total_customers = df['Customer_ID'].nunique()
    total_months = df['Month'].nunique()
    avg_bank_accounts = round(df['Num_Bank_Accounts'].mean())
    average_age = round(df['Age'].mean())
    most_common_age_category = df['Age_Category'].value_counts().idxmax()
    avg_annual_income = round(df['Annual_Income'].mean(), 1)
    on_time_payment_percentage = round((df['Delay_from_due_date'] == 0).sum() * 100.0 / len(df), 2)
    avg_credit_history = round(df['Credit_History_Age_Months'].mean())
    total_loans = df.groupby('Customer_ID')['Num_of_Loan'].max().sum()
    avg_emi = round(df['Total_EMI_per_month'].mean(), 2)
    max_debt = df['Outstanding_Debt'].max()
    avg_interest_rate = round(df['Interest_Rate'].mean(), 2)
    avg_delayed_payments = round(df['Num_of_Delayed_Payment'].mean())
    max_loans_by_customer = df['Num_of_Loan'].max()

    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Months", total_months)
    col3.metric("Avg Bank Accounts", avg_bank_accounts)
    col4.metric("Avg Age", average_age)

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Common Age Category", most_common_age_category)
    col6.metric("Avg Annual Income", f"₹{avg_annual_income:,.0f}")
    col7.metric("% On-Time Payments", f"{on_time_payment_percentage}%")
    col8.metric("Avg Credit History", f"{avg_credit_history} months")

    col9, col10, col11, col12 = st.columns(4)
    col9.metric("Total Loans (Unique)", total_loans)
    col10.metric("Avg EMI", f"₹{avg_emi:,.2f}")
    col11.metric("Max Outstanding Debt", f"₹{max_debt:,.0f}")
    col12.metric("Avg Interest Rate", f"{avg_interest_rate}%")

    col13, col14 = st.columns(2)
    col13.metric("Avg Delayed Payments", avg_delayed_payments)
    col14.metric("Max Loans by 1 Customer", max_loans_by_customer)

# --- Customer Demographics ---
elif selection == "Customer Demographics":
    st.title("👥 Customer Demographics")

    st.subheader("Total Customers by Age Category")
    age_counts = df.groupby('Age_Category')['Customer_ID'].nunique().sort_values(ascending=False)
    fig, ax = plt.subplots()
    bars = ax.bar(age_counts.index, age_counts.values, color='dodgerblue')
    for bar in bars:
        val = bar.get_height()
        label = f'{val/1000:.1f}K' if val >= 1000 else str(int(val))
        ax.text(bar.get_x() + bar.get_width()/2, val + 50, label, ha='center', fontsize=10, fontweight='bold')
    ax.set_title('Total Customers by Age Category')
    ax.set_xlabel('Age Category')
    ax.set_ylabel('Total Customers')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)

    st.subheader("Total Unique Customers by Credit Score")
    credit_score_counts = df.groupby('Credit_Score')['Customer_ID'].nunique().reset_index(name='Customer_Count')
    credit_score_counts = credit_score_counts.sort_values(by='Credit_Score')
    fig, ax = plt.subplots()
    ax.plot(credit_score_counts['Credit_Score'], credit_score_counts['Customer_Count'],
            color='dodgerblue', marker='o', linewidth=2)
    ax.fill_between(credit_score_counts['Credit_Score'], credit_score_counts['Customer_Count'],
                    color='dodgerblue', alpha=0.2)
    for x, y in zip(credit_score_counts['Credit_Score'], credit_score_counts['Customer_Count']):
        label = f'{y/1000:.1f}K' if y >= 1000 else str(int(y))
        ax.text(x, y + 200, label, ha='center', fontsize=9)
    ax.set_title("Total Unique Customers by Credit Score")
    ax.set_xlabel("Credit Score")
    ax.set_ylabel("Customer Count")
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    st.subheader("Customer Count by Category")
    counts = df.groupby('Customer_Category')['Customer_ID'].nunique().sort_values(ascending=False)
    fig, ax = plt.subplots()
    wedges, _, autotexts = ax.pie(counts, labels=None,
                                  colors=['deepskyblue', 'navy', 'darkorange', 'purple', 'deeppink'],
                                  autopct=lambda p: f'{p:.1f}%' if p >= 3 else '',
                                  startangle=90, pctdistance=0.75)
    for t in autotexts:
        t.set(color='white', fontsize=10, fontweight='bold')
    ax.legend(wedges, counts.index, title="Customer Category", loc="center left", bbox_to_anchor=(1, 0.5))
    ax.set_title("Count of Customers by Category")
    st.pyplot(fig)

    st.subheader("Top 10 Customers by Max Annual Income")
    top10 = df.groupby('Customer_ID')['Annual_Income'].max().nlargest(10)
    fig, ax = plt.subplots()
    top10.plot(kind='bar', color='#ff7f50', ax=ax)
    ax.set_title('Top 10 Customers by Max Annual Income', pad=20)
    ax.set_xlabel('Customer ID')
    ax.set_ylabel('Max Annual Income')
    ax.set_xticklabels(top10.index, rotation=45, ha='right')
    for i, v in enumerate(top10):
        ax.text(i, v + 5000, f'{int(v):,}', ha='center', fontsize=9, rotation=45)
    ax.spines['top'].set_visible(False)
    ax.set_ylim(0, top10.max() + 20000)
    st.pyplot(fig)

# --- Monthly Financial Behaviour ---
elif selection == "Monthly Financial Behaviour":
    st.title("🗖️ Monthly Financial Behaviour")
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August']

    st.subheader("Average Monthly Balance")
    avg_bal = df.groupby('Month')['Monthly_Balance'].mean().reindex(month_order)
    fig, ax = plt.subplots()
    ax.plot(avg_bal.index, avg_bal, color='#3399ff', marker='o')
    ax.set_title('Average of Monthly_Balance by Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Average of Monthly_Balance')
    for i, val in enumerate(avg_bal):
        ax.text(i, val + 0.2, f'{val:.1f}', ha='center')
    st.pyplot(fig)

    st.subheader("Average Monthly Investment")
    avg_invest = df.groupby('Month')['Amount_invested_monthly'].mean().reindex(month_order)
    fig, ax = plt.subplots()
    bars = ax.bar(avg_invest.index, avg_invest, color='#3399ff')
    ax.set(title='Average of Amount Invested Monthly by Month', xlabel='Month', ylabel='Avg Investment')
    for i, val in enumerate(avg_invest):
        ax.text(i, val + 5, f'{int(val)}', ha='center')
    st.pyplot(fig)

    st.subheader("Average Credit Utilization Ratio")
    avg_ratio = df.groupby('Month')['Credit_Utilization_Ratio'].mean().reindex(month_order)
    fig, ax = plt.subplots()
    ax.plot(avg_ratio.index, avg_ratio, color='#3399ff', marker='o')
    ax.fill_between(avg_ratio.index, avg_ratio, color='#add8ff', alpha=0.5)
    ax.set(title='Avg Credit Utilization Ratio by Month', xlabel='Month', ylabel='Avg Utilization')
    for i, val in enumerate(avg_ratio):
        ax.text(i, val + 0.05, f'{val:.3f}', ha='center')
    st.pyplot(fig)

    st.subheader("Average Delayed Payments")
    avg_delay = df.groupby('Month')['Num_of_Delayed_Payment'].mean().reindex(month_order)
    fig, ax = plt.subplots()
    ax.plot(avg_delay.index, avg_delay, color='royalblue', marker='o')
    ax.fill_between(avg_delay.index, avg_delay, color='lightblue', alpha=0.5)
    ax.set(title='Avg Delayed Payments by Month', xlabel='Month', ylabel='Avg Delays')
    for i, val in enumerate(avg_delay):
        ax.text(i, val + 0.01, f'{val:.2f}', ha='center')
    st.pyplot(fig)

# --- Credit Payment & Loan Behaviour ---
elif selection == "Credit Payment & Loan Behaviour":
    st.title("💳 Credit & Loan Behaviour")

    st.subheader("Customer Count by Num of Loan")
    loan_filtered = df['Num_of_Loan'].dropna()
    loan_counts = loan_filtered.value_counts().sort_index()
    fig, ax = plt.subplots()
    bars = ax.bar(loan_counts.index.astype(str), loan_counts.values, color='dodgerblue')
    ax.set(title='Total Customers by Num of Loan', xlabel='Num_of_Loan', ylabel='Total Customers')
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 30, str(int(height)), ha='center')
    st.pyplot(fig)

    st.subheader("Credit Mix Distribution")
    credit_mix = df.groupby('Credit_Mix')['Customer_ID'].nunique()
    fig, ax = plt.subplots()
    ax.pie(credit_mix.values, labels=credit_mix.index, autopct='%1.2f%%',
           colors=['deepskyblue', 'lightsalmon', 'skyblue'], startangle=140)
    ax.set_title('Total Customers by Credit Mix')
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("Avg Credit History Months by Age Category")
    age_credit = df.groupby('Age_Category')['Credit_History_Age_Months'].mean().round(0).sort_values(ascending=False)
    fig, ax = plt.subplots()
    ax.plot(age_credit.index, age_credit.values, marker='o', color='royalblue')
    ax.set(title='Avg Credit History Months by Age Category', xlabel='Age Category', ylabel='Avg Months')
    for i, val in enumerate(age_credit.values):
        ax.text(i, val + 5, int(val), ha='center')
    st.pyplot(fig)

    st.subheader("Customer Count by Payment Value")
    payment_value = df.groupby('Payment_Value')['Customer_ID'].nunique()
    fig, ax = plt.subplots()
    ax.pie(payment_value.values, labels=payment_value.index, autopct='%1.2f%%',
           colors=['lightskyblue', 'plum', 'lightsalmon'], startangle=140)
    ax.set_title('Total Customers by Payment Value')
    ax.axis('equal')
    st.pyplot(fig)
