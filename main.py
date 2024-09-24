import streamlit as st
import pandas as pd

st.set_page_config(page_title='House Program Calculator', page_icon='🏡', layout='wide')

st.title('House Program Calculator')
st.info('Use real data to determine real pricing.')


checks_file = st.file_uploader('**Dispatch Activities**','CSV')


st.header('Dates')

l, r = st.columns(2)

start = l.date_input('Start Date')
end   = r.date_input('End Date')

st.header('Requirements')

l, m, r = st.columns(3)

l.subheader('Metrics')
m.subheader('Expenses')
r.subheader('Calculation')

percentage_of_revenue = l.number_input('Percentage of Revenue of Business Line (%)', min_value=0.0, value=26.6, help='Quickbooks, P&L (Percent of Income)')
cost_of_software_per_month = l.number_input('Cost of Software Per Month ($)', min_value=0.0, value=6677.0, help='Quickbooks, P&L (Outside Services)')
number_of_b2b_bikes = l.number_input('Number of B2B Bikes (#)', min_value=0.0, value=4762.0, help='Partner Program Register > BIKE, # OF BIKES')
number_of_b2b_garts = l.number_input('Number of B2B Garts (#)', min_value=0.0, value=139.0, help='Partner Program Register > GART, # OF GARTS')
number_of_b2b_stops = l.number_input('Number of B2B Stops (#)', min_value=0.0, value=0.0, help='integraRental')

cost_of_labor = m.number_input('Cost of Labor ($)', min_value=0.0, value=313201.0, help='Labor Report, from Stephen & Andre')
cost_of_auto_insurance = m.number_input('Cost of Auto Insurance ($)', min_value=0.0, value=80390.0, help='Quickbooks, P&L (Insurance Expense, Auto)')
cost_of_gas = m.number_input('Cost of Gas ($)', min_value=0.0, value=177000.0, help='Quickbooks, P&L (Vehicle Expense, Fuel)')
cost_of_vehicles = m.number_input('Cost of Vehicles ($)', min_value=0.0, value=182000.0, help='Lease Spreadsheet, from Stephen & Andre')
cost_of_vehicle_maintenance = m.number_input('Cost of Vehicle Maintenance ($)', min_value=0.0, value=90000.0, help='Quickbooks, P&L (Vehicle Expense, Licenses & Permits + Repairs & Maintenance)')
percentage_of_employee_benefits = m.number_input('Percentage of Revenue to Employee Benefits (%)', min_value=0.0, value=15.0, help='Percentage of Cost of Labor')
interest_rate_of_unit = m.number_input('Financing Interest Rate on Unit (%)', min_value=0.0, value=18.0, help='')
cost_of_unit = m.number_input('Cost of Unit ($)', min_value=0.0, value=480.0, help='')

cost_of_employee_benefits = r.number_input('Cost of Employee Benefits ($)', min_value=0.0, value=(cost_of_labor * (percentage_of_employee_benefits/100)), help='cost_of_labor * percentage_of_employee_benefits', disabled=True)
number_of_b2b_units = r.number_input('Number of B2B Units (#)', min_value=0.0, value=(number_of_b2b_bikes + number_of_b2b_garts), help='b2b_bikes + b2b_garts', disabled=True)
cost_of_software = r.number_input('Cost of Software ($)', min_value=0.0, value=((cost_of_software_per_month * 12) / number_of_b2b_units), help='(software_per_month * 12) / b2b_units', disabled=True)

cost_per_stop = st.number_input('Cost Per Stop ($)', min_value=0.0, value=7.0, help='What is the cost associated to each time we do a stop?')
cost_per_bike = st.number_input('Cost Per Asset ($)', min_value=0.0, value=0.0, help='What is the cost to aquire a singular asset?')
cost_to_repair = st.number_input('Cost Of Maintenance ($)', min_value=0.0, value=0.0, help='What is the average cost in parts per asset?')


if checks_file is not None:

    df = pd.read_csv(checks_file, index_col = False)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df[(df['Date'] >= start) & (df['Date'] <= end)]
    pivot = df.groupby('Location')['Activity'].count()

    average_stops_per_property = pivot.mean()

    l, r = st.columns(2)

    l.metric('Average Checks Per Property', round(average_stops_per_property))
    r.metric('Cost of Checks Per Property', round(average_stops_per_property * cost_per_stop, 2))

    st.divider()

    with st.expander('To-Do Items'):
        st.info('We need to also acknowlege each property has a delivery stop and a pickup stop.')
        st.info('We should consider total stops per house program property (replacements, swaps, fix, etc.)')