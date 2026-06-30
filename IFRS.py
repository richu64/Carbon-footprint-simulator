import streamlit as st

# Set layout to wide to comfortably fit both "pages" side-by-side
st.set_page_config(layout="wide", page_title="IFRS 18 Transition Dashboard")

st.title("Financial Statement Transition Dashboard")
st.caption("Compare traditional Statement of Operations with the new IFRS 18 Statement of Financial Performance.")

st.markdown("---")

# Create two equal-width columns to simulate side-by-side pages
col1, col2 = st.columns(2)

# ==========================================
# PAGE 1: TRADITIONAL STATEMENT OF OPERATIONS
# ==========================================
with col1:
    st.header("📄 Page 1: Statement of Operations")
    st.subheader("User Input Fields")
    st.write("Enter your organization's financial data below:")
    
    # Input fields for standard financial items
    revenue = st.number_input("Revenue / Sales", value=500000, step=5000)
    cogs = st.number_input("Cost of Goods Sold (COGS)", value=200000, step=5000)
    sga = st.number_input("Selling, General & Administrative (SG&A)", value=80000, step=1000)
    
    st.markdown("---")
    st.write("*Other Income / Expenses & Financial Items:*")
    
    associates_income = st.number_input("Share of profit from integral associates/JV", value=15000, step=1000)
    interest_expense = st.number_input("Interest Expense on Bank Loans", value=12000, step=500)
    forex_gain = st.number_input("Foreign Exchange Gain/Loss on cash balances", value=3000, step=500)
    tax_expense = st.number_input("Income Tax Expense", value=35000, step=1000)

# ==========================================
# PAGE 2: IFRS 18 STATEMENT OF FINANCIAL PERFORMANCE
# ==========================================
with col2:
    st.header("📊 Page 2: Statement of Financial Performance")
    st.subheader("Rearranged according to IFRS 18")
    st.write("Real-time restructuring based on the new IFRS 18 categories:")

    # --- 1. Operating Category ---
    gross_profit = revenue - cogs
    # Under IFRS 18, operating category is the default residual category
    # Income/expenses from integral associates are typically presented here or right next to operating profit
    operating_profit = gross_profit - sga + associates_income 
    
    # --- 2. Investing Category ---
    # Includes income/expenses from assets that generate returns independently (like cash/forex on cash)
    investing_income = forex_gain 
    
    # --- 3. Financing Category ---
    # Includes transactions that involve solely the raising of finance
    financing_expenses = interest_expense
    
    # Calculations
    profit_before_tax = operating_profit + investing_income - financing_expenses
    net_income = profit_before_tax - tax_expense

    # Displaying the restructured layout
    st.markdown("### **1. Operating Category**")
    st.metric(label="Revenue", value=f"${revenue:,.2f}")
    st.text(f"Cost of Goods Sold: -${cogs:,.2f}")
    st.text(f"SG&A Expenses: -${sga:,.2f}")
    st.text(f"Share of Profit (Integral Associates): +${associates_income:,.2f}")
    
    # IFRS 18 mandatory subtotal
    st.success(f"**Operating Profit (Mandatory Subtotal): ${operating_profit:,.2f}**")
    
    st.markdown("### **2. Investing Category**")
    st.text(f"Net Foreign Exchange Gains on Cash: +${investing_income:,.2f}")
    
    st.markdown("### **3. Financing Category**")
    st.text(f"Interest Expense on Liabilities: -${financing_expenses:,.2f}")
    
    st.markdown("---")
    # Final Subtotals
    st.metric(label="Profit Before Tax", value=f"${profit_before_tax:,.2f}")
    st.text(f"Income Tax Expense: -${tax_expense:,.2f}")
    st.info(f"**Net Profit for the Period: ${net_income:,.2f}**")

# Optional: Add a subtle visual boundary between the two "pages"
st.markdown(
    """
    <style>
    div[data-testid="column"]:nth-of-type(1) {
        border-right: 2px solid #f0f2f6;
        padding-right: 20px;
    }
    div[data-testid="column"]:nth-of-type(2) {
        padding-left: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)