import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import math

# Page configuration
st.set_page_config(
    page_title="Real Estate Deal Evaluation Platform",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f2937;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .scenario-card {
        border: 2px solid #e5e7eb;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: #f9fafb;
    }
    .highlight-positive {
        color: #10b981;
        font-weight: bold;
    }
    .highlight-negative {
        color: #ef4444;
        font-weight: bold;
    }
    .section-header {
        font-size: 1.5rem;
        color: #374151;
        font-weight: 600;
        margin: 1rem 0;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class RealEstateCalculator:
    def __init__(self):
        self.scenarios = [
            {"name": "Scenario 1", "down_payment_pct": 30, "loan_term": 25, "balloon_term": 5},
            {"name": "Scenario 2", "down_payment_pct": 30, "loan_term": 20, "balloon_term": None},
            {"name": "Scenario 3", "down_payment_pct": 35, "loan_term": 25, "balloon_term": 5},
            {"name": "Scenario 4", "down_payment_pct": 35, "loan_term": 20, "balloon_term": None}
        ]
    
    def calculate_mortgage_payment(self, loan_amount, annual_rate, years):
        """Calculate monthly mortgage payment"""
        if annual_rate == 0:
            return loan_amount / (years * 12)
        
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        return payment
    
    def calculate_scenario_metrics(self, inputs, scenario):
        """Calculate all financial metrics for a scenario"""
        purchase_price = inputs['purchase_price']
        down_payment = purchase_price * (scenario['down_payment_pct'] / 100)
        loan_amount = purchase_price - down_payment
        
        # Monthly payment calculation
        monthly_payment = self.calculate_mortgage_payment(
            loan_amount, inputs['interest_rate'], scenario['loan_term']
        )
        annual_debt_service = monthly_payment * 12
        
        # Income calculations
        gross_rent_income = inputs['monthly_rent'] * 12
        vacancy_loss = gross_rent_income * (inputs['vacancy_rate'] / 100)
        effective_gross_income = gross_rent_income - vacancy_loss + inputs['other_income']
        
        # Operating expenses
        total_operating_expenses = (
            inputs['property_taxes'] + inputs['insurance'] + 
            inputs['repairs_maintenance'] + inputs['property_management'] + 
            inputs['utilities'] + inputs['cam_charges']
        )
        
        # Key metrics
        noi = effective_gross_income - total_operating_expenses
        cash_flow = noi - annual_debt_service
        total_cash_invested = down_payment + inputs['closing_costs']
        cash_on_cash_return = (cash_flow / total_cash_invested) * 100 if total_cash_invested > 0 else 0
        cap_rate = (noi / purchase_price) * 100
        dscr = noi / annual_debt_service if annual_debt_service > 0 else 0
        
        return {
            'down_payment': down_payment,
            'loan_amount': loan_amount,
            'monthly_payment': monthly_payment,
            'annual_debt_service': annual_debt_service,
            'gross_rent_income': gross_rent_income,
            'effective_gross_income': effective_gross_income,
            'total_operating_expenses': total_operating_expenses,
            'noi': noi,
            'cash_flow': cash_flow,
            'total_cash_invested': total_cash_invested,
            'cash_on_cash_return': cash_on_cash_return,
            'cap_rate': cap_rate,
            'dscr': dscr
        }
    
    def generate_amortization_schedule(self, loan_amount, annual_rate, years, num_payments_to_show=60):
        """Generate amortization schedule"""
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        monthly_payment = self.calculate_mortgage_payment(loan_amount, annual_rate, years)
        
        schedule = []
        balance = loan_amount
        
        for payment_num in range(1, min(num_payments_to_show + 1, num_payments + 1)):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            balance -= principal_payment
            
            schedule.append({
                'Payment': payment_num,
                'Date': datetime.now() + timedelta(days=30 * payment_num),
                'Payment Amount': monthly_payment,
                'Principal': principal_payment,
                'Interest': interest_payment,
                'Balance': max(0, balance)
            })
        
        return pd.DataFrame(schedule)

def main():
    st.markdown('<h1 class="main-header">🏢 Real Estate Deal Evaluation Platform</h1>', unsafe_allow_html=True)
    
    # Initialize calculator
    calc = RealEstateCalculator()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Dashboard", "ROI Calculator", "Deal Analysis", "Market Intelligence", "Document Center", "Collaboration"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "ROI Calculator":
        show_roi_calculator(calc)
    elif page == "Deal Analysis":
        show_deal_analysis(calc)
    elif page == "Market Intelligence":
        show_market_intelligence()
    elif page == "Document Center":
        show_document_center()
    elif page == "Collaboration":
        show_collaboration()

def show_dashboard():
    st.markdown('<div class="section-header">📊 Portfolio Dashboard</div>', unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>$14.6M</h3>
            <p>Total Portfolio Value</p>
            <small>+12% from last quarter</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>8</h3>
            <p>Active Deals</p>
            <small>3 pending analysis</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>8.3%</h3>
            <p>Average ROI</p>
            <small>Above market average</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>Low</h3>
            <p>Risk Score</p>
            <small>Well diversified</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent deals
    st.markdown('<div class="section-header">🏠 Recent Deals</div>', unsafe_allow_html=True)
    
    deals_data = {
        'Property': ['Sunset Apartments', 'Downtown Office Complex', 'Industrial Warehouse'],
        'Location': ['Austin, TX', 'Denver, CO', 'Phoenix, AZ'],
        'Type': ['Multifamily', 'Office', 'Industrial'],
        'Price': ['$2.45M', '$8.95M', '$3.20M'],
        'ROI': ['8.5%', '7.3%', '9.1%'],
        'Status': ['Analyzing', 'Pending', 'Completed']
    }
    
    df_deals = pd.DataFrame(deals_data)
    st.dataframe(df_deals, use_container_width=True)
    
    # Portfolio performance chart
    st.markdown('<div class="section-header">📈 Portfolio Performance</div>', unsafe_allow_html=True)
    
    # Sample data for chart
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    portfolio_value = [12.5, 13.1, 13.8, 14.2, 14.0, 14.6]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=months, y=portfolio_value,
        mode='lines+markers',
        name='Portfolio Value (M)',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Portfolio Value Over Time',
        xaxis_title='Month',
        yaxis_title='Value (Millions $)',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_roi_calculator(calc):
    st.markdown('<div class="section-header">🧮 ROI Calculator</div>', unsafe_allow_html=True)
    
    # Input form
    with st.expander("🏢 Property Details & Assumptions", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("💰 Purchase Information")
            purchase_price = st.number_input("Purchase Price ($)", value=2475000, step=1000, format="%d")
            interest_rate = st.number_input("Interest Rate (%)", value=6.75, step=0.01, format="%.2f")
            closing_costs = st.number_input("Closing Costs ($)", value=24750, step=100, format="%d")
        
        with col2:
            st.subheader("🏠 Income Information")
            monthly_rent = st.number_input("Monthly Rent Income ($)", value=17956, step=100, format="%d")
            vacancy_rate = st.number_input("Vacancy Rate (%)", value=5.0, step=0.1, format="%.1f")
            other_income = st.number_input("Other Income (Annual $)", value=1200, step=100, format="%d")
        
        with col3:
            st.subheader("🔧 Operating Expenses")
            property_taxes = st.number_input("Property Taxes ($)", value=9900, step=100, format="%d")
            insurance = st.number_input("Insurance ($)", value=4950, step=100, format="%d")
            repairs_maintenance = st.number_input("Repairs & Maintenance ($)", value=8250, step=100, format="%d")
            property_management = st.number_input("Property Management ($)", value=6600, step=100, format="%d")
            utilities = st.number_input("Utilities ($)", value=2200, step=100, format="%d")
            
            use_cam = st.checkbox("Include CAM Charges")
            cam_charges = st.number_input("CAM Charges ($)", value=0, step=100, format="%d") if use_cam else 0
    
    # Additional parameters
    col1, col2 = st.columns(2)
    with col1:
        appreciation_rate = st.number_input("Appreciation Rate (%)", value=3.0, step=0.1, format="%.1f")
    with col2:
        rent_increase_rate = st.number_input("Annual Rent Increase (%)", value=2.5, step=0.1, format="%.1f")
    
    # Prepare inputs
    inputs = {
        'purchase_price': purchase_price,
        'interest_rate': interest_rate,
        'closing_costs': closing_costs,
        'monthly_rent': monthly_rent,
        'vacancy_rate': vacancy_rate,
        'other_income': other_income,
        'property_taxes': property_taxes,
        'insurance': insurance,
        'repairs_maintenance': repairs_maintenance,
        'property_management': property_management,
        'utilities': utilities,
        'cam_charges': cam_charges
    }
    
    # Calculate scenarios
    st.markdown('<div class="section-header">📊 4-Scenario Analysis</div>', unsafe_allow_html=True)
    
    # Create comparison table
    results = []
    for scenario in calc.scenarios:
        metrics = calc.calculate_scenario_metrics(inputs, scenario)
        results.append({
            'Scenario': scenario['name'],
            'Down Payment %': f"{scenario['down_payment_pct']}%",
            'Down Payment $': f"${metrics['down_payment']:,.0f}",
            'Loan Amount': f"${metrics['loan_amount']:,.0f}",
            'Loan Term': f"{scenario['loan_term']} years",
            'Balloon': f"{scenario['balloon_term']} years" if scenario['balloon_term'] else "None",
            'NOI': f"${metrics['noi']:,.0f}",
            'Debt Service': f"${metrics['annual_debt_service']:,.0f}",
            'Cash Flow': f"${metrics['cash_flow']:,.0f}",
            'CoC Return': f"{metrics['cash_on_cash_return']:.2f}%",
            'Cap Rate': f"{metrics['cap_rate']:.2f}%",
            'DSCR': f"{metrics['dscr']:.2f}"
        })
    
    df_results = pd.DataFrame(results)
    st.dataframe(df_results, use_container_width=True)
    
    # Scenario cards
    st.markdown('<div class="section-header">📈 Scenario Summary</div>', unsafe_allow_html=True)
    
    cols = st.columns(4)
    for i, scenario in enumerate(calc.scenarios):
        metrics = calc.calculate_scenario_metrics(inputs, scenario)
        
        with cols[i]:
            cash_flow_color = "highlight-positive" if metrics['cash_flow'] > 0 else "highlight-negative"
            
            st.markdown(f"""
            <div class="scenario-card">
                <h4>{scenario['name']}</h4>
                <p><strong>Down Payment:</strong> {scenario['down_payment_pct']}%</p>
                <p><strong>Cash Flow:</strong> <span class="{cash_flow_color}">${metrics['cash_flow']:,.0f}</span></p>
                <p><strong>CoC Return:</strong> {metrics['cash_on_cash_return']:.2f}%</p>
                <p><strong>DSCR:</strong> {metrics['dscr']:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Visualization
    st.markdown('<div class="section-header">🎯 Performance Comparison</div>', unsafe_allow_html=True)
    
    # Extract data for charts
    scenario_names = [s['name'] for s in calc.scenarios]
    cash_flows = [calc.calculate_scenario_metrics(inputs, s)['cash_flow'] for s in calc.scenarios]
    coc_returns = [calc.calculate_scenario_metrics(inputs, s)['cash_on_cash_return'] for s in calc.scenarios]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cash_flow = px.bar(
            x=scenario_names, y=cash_flows,
            title="Annual Cash Flow by Scenario",
            labels={'x': 'Scenario', 'y': 'Cash Flow ($)'},
            color=cash_flows,
            color_continuous_scale='RdYlGn'
        )
        fig_cash_flow.update_layout(template='plotly_white')
        st.plotly_chart(fig_cash_flow, use_container_width=True)
    
    with col2:
        fig_coc = px.bar(
            x=scenario_names, y=coc_returns,
            title="Cash-on-Cash Return by Scenario",
            labels={'x': 'Scenario', 'y': 'CoC Return (%)'},
            color=coc_returns,
            color_continuous_scale='Viridis'
        )
        fig_coc.update_layout(template='plotly_white')
        st.plotly_chart(fig_coc, use_container_width=True)

def show_deal_analysis(calc):
    st.markdown('<div class="section-header">📋 Deal Analysis Tools</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Amortization Schedule", "Rent Roll Tracker", "Expense Log", "Market Comparables"])
    
    with tabs[0]:
        st.subheader("📅 Amortization Schedule")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            loan_amount = st.number_input("Loan Amount", value=1732500, step=1000)
        with col2:
            annual_rate = st.number_input("Interest Rate (%)", value=6.75, step=0.01)
        with col3:
            loan_years = st.number_input("Loan Term (years)", value=25, step=1)
        
        num_payments = st.slider("Number of payments to show", 12, 360, 60)
        
        if st.button("Generate Schedule"):
            schedule_df = calc.generate_amortization_schedule(loan_amount, annual_rate, loan_years, num_payments)
            
            # Format the dataframe
            schedule_df['Date'] = schedule_df['Date'].dt.strftime('%Y-%m-%d')
            schedule_df['Payment Amount'] = schedule_df['Payment Amount'].apply(lambda x: f"${x:,.2f}")
            schedule_df['Principal'] = schedule_df['Principal'].apply(lambda x: f"${x:,.2f}")
            schedule_df['Interest'] = schedule_df['Interest'].apply(lambda x: f"${x:,.2f}")
            schedule_df['Balance'] = schedule_df['Balance'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(schedule_df, use_container_width=True)
            
            # Download option
            csv = schedule_df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="amortization_schedule.csv",
                mime="text/csv"
            )
    
    with tabs[1]:
        st.subheader("🏠 Rent Roll Tracker")
        
        # Sample rent roll data
        rent_roll_data = {
            'Suite': ['101', '105', '107', '109'],
            'Tenant': ['Geek Out, Inc.', 'JXWX Enterprises', 'Brandon A. Mantilla', 'Jory International'],
            'Square Feet': [4021, 1800, 1021, 1200],
            'Rate/SF': [19.74, 26.00, 22.00, 19.38],
            'Monthly Rent': [6614, 3900, 1872, 1938],
            'Lease Start': ['2023-01-01', '2023-03-01', '2023-02-15', '2023-04-01'],
            'Lease End': ['2025-12-31', '2026-02-28', '2025-02-14', '2026-03-31'],
            'Status': ['Active', 'Active', 'Active', 'Active']
        }
        
        df_rent_roll = pd.DataFrame(rent_roll_data)
        st.dataframe(df_rent_roll, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Units", len(df_rent_roll))
        with col2:
            st.metric("Total Monthly Rent", f"${df_rent_roll['Monthly Rent'].sum():,.0f}")
        with col3:
            st.metric("Average Rate/SF", f"${df_rent_roll['Rate/SF'].mean():.2f}")
    
    with tabs[2]:
        st.subheader("💰 Expense Log")
        
        # Add new expense
        with st.expander("Add New Expense"):
            col1, col2, col3 = st.columns(3)
            with col1:
                expense_date = st.date_input("Date")
                expense_category = st.selectbox("Category", 
                    ["Repairs & Maintenance", "Property Management", "Insurance", 
                     "Property Taxes", "Utilities", "Legal", "Other"])
            with col2:
                expense_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
                expense_description = st.text_input("Description")
            with col3:
                vendor = st.text_input("Vendor/Payee")
                if st.button("Add Expense"):
                    st.success("Expense added successfully!")
        
        # Sample expense data
        expense_data = {
            'Date': ['2024-01-15', '2024-01-20', '2024-02-01', '2024-02-15'],
            'Category': ['Repairs & Maintenance', 'Property Management', 'Insurance', 'Utilities'],
            'Amount': [1250.00, 550.00, 412.50, 183.75],
            'Description': ['HVAC Repair Unit 105', 'Monthly Management Fee', 'Quarterly Insurance Premium', 'Electric Bill'],
            'Vendor': ['ABC HVAC Services', 'Premier Property Mgmt', 'State Farm Insurance', 'Texas Electric']
        }
        
        df_expenses = pd.DataFrame(expense_data)
        st.dataframe(df_expenses, use_container_width=True)
        
        # Expense summary chart
        expense_by_category = df_expenses.groupby('Category')['Amount'].sum()
        fig_expenses = px.pie(
            values=expense_by_category.values,
            names=expense_by_category.index,
            title="Expenses by Category"
        )
        st.plotly_chart(fig_expenses, use_container_width=True)
    
    with tabs[3]:
        st.subheader("🏘️ Market Comparables")
        
        # Sample comparable properties
        comps_data = {
            'Property': ['Oak Street Apartments', 'Riverside Complex', 'Metro Gardens', 'Sunset Plaza'],
            'Distance': ['0.3 miles', '0.7 miles', '1.2 miles', '1.5 miles'],
            'Units': [124, 96, 156, 88],
            'Sale Price': [2800000, 2100000, 3400000, 1950000],
            'Price/SF': [290, 275, 295, 285],
            'Cap Rate': [6.2, 6.8, 5.9, 7.1],
            'Sale Date': ['2024-01-15', '2023-11-30', '2024-02-20', '2023-12-10']
        }
        
        df_comps = pd.DataFrame(comps_data)
        
        # Format the dataframe
        df_comps['Sale Price'] = df_comps['Sale Price'].apply(lambda x: f"${x:,.0f}")
        df_comps['Price/SF'] = df_comps['Price/SF'].apply(lambda x: f"${x}")
        df_comps['Cap Rate'] = df_comps['Cap Rate'].apply(lambda x: f"{x}%")
        
        st.dataframe(df_comps, use_container_width=True)
        
        # Market analysis
        st.subheader("Market Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            avg_price_sf = np.mean([290, 275, 295, 285])
            st.metric("Average Price/SF", f"${avg_price_sf:.0f}")
            
        with col2:
            avg_cap_rate = np.mean([6.2, 6.8, 5.9, 7.1])
            st.metric("Average Cap Rate", f"{avg_cap_rate:.1f}%")

def show_market_intelligence():
    st.markdown('<div class="section-header">🌍 Market Intelligence</div>', unsafe_allow_html=True)
    
    # Market selection
    col1, col2 = st.columns(2)
    with col1:
        market = st.selectbox("Select Market", ["Austin, TX", "Denver, CO", "Phoenix, AZ", "Dallas, TX"])
    with col2:
        property_type = st.selectbox("Property Type", ["All Types", "Multifamily", "Office", "Industrial", "Retail"])
    
    # Market metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Cap Rate", "6.4%", "0.3%")
    with col2:
        st.metric("Median Price/SF", "$285", "8%")
    with col3:
        st.metric("Days on Market", "87", "-12")
    
    # Market trends chart
    st.subheader("Market Trends")
    
    # Sample trend data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    cap_rates = [6.1, 6.2, 6.3, 6.4, 6.3, 6.4]
    prices = [275, 278, 282, 285, 284, 285]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=cap_rates,
        mode='lines+markers',
        name='Cap Rate (%)',
        yaxis='y',
        line=dict(color='#ef4444')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=prices,
        mode='lines+markers',
        name='Price/SF ($)',
        yaxis='y2',
        line=dict(color='#3b82f6')
    ))
    
    fig.update_layout(
        title='Market Trends Over Time',
        xaxis_title='Month',
        yaxis=dict(title='Cap Rate (%)', side='left'),
        yaxis2=dict(title='Price/SF ($)', side='right', overlaying='y'),
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Market insights
    st.subheader("AI Market Insights")
    
    insights = [
        {"type": "positive", "title": "Strong Rental Demand", 
         "description": "Occupancy rates at 95%+ across multifamily properties"},
        {"type": "info", "title": "New Construction Activity", 
         "description": "18 new projects announced in Q1, focusing on mixed-use"},
        {"type": "warning", "title": "Interest Rate Impact", 
         "description": "Rising rates affecting buyer activity, creating opportunities"}
    ]
    
    for insight in insights:
        if insight["type"] == "positive":
            st.success(f"**{insight['title']}**: {insight['description']}")
        elif insight["type"] == "warning":
            st.warning(f"**{insight['title']}**: {insight['description']}")
        else:
            st.info(f"**{insight['title']}**: {insight['description']}")

def show_document_center():
    st.markdown('<div class="section-header">📄 Document Center</div>', unsafe_allow_html=True)
    
    # File upload
    st.subheader("Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose files", 
        accept_multiple_files=True,
        type=['pdf', 'doc', 'docx', 'xlsx', 'xls']
    )
    
    if uploaded_files:
        st.success(f"Uploaded {len(uploaded_files)} file(s)")
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size} bytes)")
    
    # Document list
    st.subheader("Document Library")
    
    # Sample documents
    docs_data = {
        'Document': [
            'Purchase Agreement - Sunset Apartments.pdf',
            'LOI - Downtown Office Complex.pdf',
            'Partnership Agreement - Phoenix Warehouse.pdf',
            'Inspection Report - Sunset Apartments.pdf'
        ],
        'Type': ['Contract', 'LOI', 'Partnership', 'Report'],
        'Upload Date': ['2024-01-15', '2024-01-14', '2024-01-12', '2024-01-16'],
        'Size': ['2.4 MB', '1.8 MB', '3.1 MB', '5.2 MB'],
        'AI Status': ['✅ Reviewed', '⚠️ Issues Found', '🔄 Processing', '✅ Reviewed']
    }
    
    df_docs = pd.DataFrame(docs_data)
    st.dataframe(df_docs, use_container_width=True)
    
    # AI insights
    st.subheader("AI Document Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.error("**High Risk Clause Detected**  \nUncapped indemnity clause found in Downtown Office LOI (Section 12.3). Consider limiting liability to purchase price.")
    
    with col2:
        st.warning("**Missing Standard Clause**  \nEnvironmental contingency clause not present. Recommend adding Phase I ESA requirement.")
    
    st.success("**Compliance Check**  \nAll required disclosure statements present and properly formatted.")

def show_collaboration():
    st.markdown('<div class="section-header">👥 Collaboration Hub</div>', unsafe_allow_html=True)
    
    # Active collaborations
    st.subheader("Active Deal Collaborations")
    
    # Sample collaboration data
    collab_data = {
        'Deal': ['Sunset Apartments', 'Downtown Office Complex', 'Industrial Warehouse'],
        'Partners': ['3 partners', '2 partners', '4 partners'],
        'Status': ['Active', 'Pending Signatures', 'Under Review'],
        'Last Activity': ['2 hours ago', '1 day ago', '3 hours ago']
    }
    
    df_collab = pd.DataFrame(collab_data)
    st.dataframe(df_collab, use_container_width=True)
    
    # Partner management
    st.subheader("Invite New Partner")
    
    col1, col2 = st.columns(2)
    with col1:
        partner_email = st.text_input("Partner Email")
        partner_role = st.selectbox("Role", ["Investor", "Lender", "Broker", "Attorney", "Accountant"])
    
    with col2:
        deal_access = st.multiselect("Grant Access to Deals", 
            ["Sunset Apartments", "Downtown Office Complex", "Industrial Warehouse"])
        
        if st.button("Send Invitation"):
            st.success(f"Invitation sent to {partner_email}")
    
    # Recent messages
    st.subheader("Recent Messages")
    
    messages = [
        {"sender": "Mike Partners", "time": "2 hours ago", 
         "message": "The appraisal came back higher than expected. Looking good!"},
        {"sender": "Sarah Kim", "time": "4 hours ago", 
         "message": "Contract review complete. Found a few items to discuss."},
        {"sender": "Robert Lee", "time": "1 day ago", 
         "message": "Can we schedule a call to discuss financing terms?"}
    ]
    
    for msg in messages:
        with st.chat_message("user"):
            st.write(f"**{msg['sender']}** - {msg['time']}")
            st.write(msg['message'])
    
    # Message input
    if prompt := st.chat_input("Type a message..."):
        with st.chat_message("assistant"):
            st.write(f"**You** - just now")
            st.write(prompt)

if __name__ == "__main__":
    main()
