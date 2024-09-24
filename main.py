import streamlit as st # type: ignore
import pandas as pd 
import matplotlib.pyplot as plt 
import math

st.title("Demo Simple App")

# working in Streamlit with inout fields
st.write("### Input Data") ## this command creates an input field for user to interact
col1, col2 = st.columns(2) ## used to split the context into columns
Property_value = col1.number_input("Property Value (₹)", min_value=0 , value=50000000) ## can set parameters as well for that particular tag
deposit = col1.number_input("Deposit (₹)", min_value=0 , value=10000000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=0 , value=15)
loan_term = col2.number_input("Loan Term (in Years)", min_value=0 , value=25)

# calculation of payments (backend logic: not specific to streamlit)
loan_amount = Property_value - deposit
monthly_interest_rate = (interest_rate / 100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

# Displaying the payments for users
total_payment = monthly_payment * number_of_payments
total_interest = total_payment - loan_amount

st.write("### Payments") ## Syntax for creating a heading on the page (here number '#' define how big or small the heading will appear where #=H1, ##=H2, etc.)
col1, col2, col3 = st.columns(3)
    ## metric tag is used to build a table like format
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total Repayments", value=f"${total_payment:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Create a data frame with payment schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(1 / 12) ## Calculation of year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principal_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

# Display the data frame as a chart
st.write("### Payment Schedule")
payment_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payment_df)