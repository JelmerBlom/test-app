import streamlit as st

# Sidebar for inputs
st.sidebar.title('Solar Panel and Battery Inputs')

# Common Costs for Both Methods
st.sidebar.header('Kosten Thuisbatterij')
battery_cost = st.sidebar.number_input('Inkoopkosten thuisbatterij (€)', value=7511.00, step=100.0)
inverter_cost = st.sidebar.number_input('Inkoopkosten omvormer (€)', value=840.00, step=10.0)
installation_cost = st.sidebar.number_input('Installatiekosten (€)', value=700.00, step=10.0)
vat_return = st.sidebar.number_input('BTW terugvangen 21% (€)', value=1900.71, step=10.0)
battery_lifespan = st.sidebar.number_input('Looptijd (in jaren)', value=15, step=1)

# Cost calculations
total_cost = battery_cost + inverter_cost + installation_cost - vat_return
annual_cost = total_cost / battery_lifespan

# Static Savings Calculations
st.sidebar.header('Static Savings (Self-consumption)')
battery_capacity = st.sidebar.number_input('Opslagcapaciteit van de batterij (in kWh)', value=15.0, step=1.0)
battery_efficiency = st.sidebar.number_input('Efficiëntie van de batterij', value=0.9, step=0.1)
effective_storage = battery_capacity * battery_efficiency

num_panels = st.sidebar.number_input('Aantal zonnepanelen', value=24, step=1)
daily_output_per_panel = st.sidebar.number_input('Gemiddelde opwekking per zonnepaneel per dag (in kWh)', value=0.85, step=0.1)
annual_output = num_panels * daily_output_per_panel * 365

annual_consumption = st.sidebar.number_input('Verbruik per jaar (in kWh)', value=17000, step=100)
price_per_kwh = st.sidebar.number_input('Prijs per kWh (€)', value=0.30, step=0.01)
self_consumption = st.sidebar.number_input('Zelf gebruik van het net (in kWh)', value=26.17534247, step=1.0)

daily_consumption = annual_consumption / 365
daily_grid_usage = daily_consumption - self_consumption
annual_grid_cost = daily_grid_usage * price_per_kwh * 365
annual_saving = daily_grid_usage * price_per_kwh * 365
payback_period_static = total_cost / annual_saving if annual_saving > 0 else None

# Dynamic Market Trading Calculations
st.sidebar.header('Dynamic Market Trading')
transactions_per_day = st.sidebar.number_input('Transacties per dag', value=1.5, step=0.1)
profit_per_kwh = st.sidebar.number_input('Winst per Kwh (€)', value=0.15, step=0.01)
kwh_traded_per_day = st.sidebar.number_input('Hoeveelheid kWh per dag verhandelen', value=20.25, step=1.0)

annual_traded_kwh = kwh_traded_per_day * 365
annual_profit_dynamic = annual_traded_kwh * profit_per_kwh
payback_period_dynamic = total_cost / annual_profit_dynamic if annual_profit_dynamic > 0 else None

# Main Content
st.title('Comparison of Savings Options')

# Payback Period Comparison with Conditional Formatting
st.subheader("Payback Period Comparison")
if payback_period_static and payback_period_dynamic:
    if payback_period_static < payback_period_dynamic:
        st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #e6ffe6;">
                <strong>Static Savings Payback Period (years):</strong> {payback_period_static:.2f}
            </div>
            <div style="padding: 10px; border-radius: 10px; background-color: #ffe6e6;">
                <strong>Dynamic Market Trading Payback Period (years):</strong> {payback_period_dynamic:.2f}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #ffe6e6;">
                <strong>Static Savings Payback Period (years):</strong> {payback_period_static:.2f}
            </div>
            <div style="padding: 10px; border-radius: 10px; background-color: #e6ffe6;">
                <strong>Dynamic Market Trading Payback Period (years):</strong> {payback_period_dynamic:.2f}
            </div>
            """, unsafe_allow_html=True)
else:
    st.write("Insufficient data to calculate payback periods.")

# Kosten Thuisbatterij Block
st.subheader("Kosten Thuisbatterij")
st.markdown(f"""
    <div style="padding: 20px; border: 2px solid #ddd; border-radius: 10px; background-color: #f9f9f9;">
        <p><strong>Netto Aanschafprijs (€):</strong> {total_cost:.2f} €</p>
        <p><strong>Totale kosten per jaar (€):</strong> {annual_cost:.2f} €</p>
    </div>
    """, unsafe_allow_html=True)

# Results for Both Options Block
st.subheader("Results for Both Options")
st.markdown("""
    <div style='padding: 20px; border: 2px solid #ddd; border-radius: 10px; background-color: #f9f9f9;'>
        <div style='margin-bottom: 10px;'>
            <h3>Static Savings (Self-consumption)</h3>
            <p><strong>Annual Savings (€):</strong> {:.2f}</p>
            <p><strong>Annual Grid Cost (€):</strong> {:.2f}</p>
            <p><strong>Effective Battery Storage Capacity (kWh):</strong> {:.2f}</p>
        </div>
        <div style='margin-top: 10px;'>
            <h3>Dynamic Market Trading</h3>
            <p><strong>Annual Profit from Trading (€):</strong> {:.2f}</p>
            <p><strong>kWh Traded per Year:</strong> {:.2f}</p>
        </div>
    </div>
    """.format(annual_saving, annual_grid_cost, effective_storage, annual_profit_dynamic, annual_traded_kwh),
    unsafe_allow_html=True)
