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

percentage_of_revenue = l.number_input('Percentage of Revenue for B2B (%)', min_value=0.0, value=26.8, help='Quickbooks, P&L (Percent of Income)')
percentage_of_employee_benefits = l.number_input('Percentage of Labor to Employee Benefits (%)', min_value=0.0, value=15.0, help='Percentage of Cost of Labor')
interest_rate_of_unit = l.number_input('Financing Interest Rate on Unit (%)', min_value=0.0, value=18.0, help='')
number_of_years_to_payoff = l.number_input('Number of Years to Pay Off Unit (#)', min_value=0.0, value=3.0, help='')
percentage_of_profit_margin = l.number_input('Percentage of Profit Margin (%)', min_value=0.0, value=20.0, help='')
number_of_units_per_property = l.number_input('Average Number of Units Per Property (#)', min_value=0.0, value=4.340929809, help='=AVERAGE(PPR > BIKE, # OF BIKES)')

cost_of_labor = m.number_input('Cost of Labor for B2B ($)', min_value=0.0, value=313201.0, help='Labor Report, from Stephen & Andre')
cost_of_auto_insurance = m.number_input('Cost of Auto Insurance ($)', min_value=0.0, value=75000.0, help='Quickbooks, P&L (Insurance Expense, Auto)')
cost_of_gas = m.number_input('Cost of Gas ($)', min_value=0.0, value=147134.0, help='Quickbooks, P&L (Vehicle Expense, Fuel)')
cost_of_vehicles = m.number_input('Cost of Vehicles ($)', min_value=0.0, value=319531.0, help='Lease Spreadsheet, from Stephen & Andre')
cost_of_vehicle_maintenance = m.number_input('Cost of Vehicle Maintenance ($)', min_value=0.0, value=90000.0, help='Quickbooks, P&L (Vehicle Expense, Licenses & Permits + Repairs & Maintenance)')
cost_of_software_per_month = m.number_input('Cost of Software Per Month ($)', min_value=0.0, value=6677.0, help='Quickbooks, P&L (Outside Services)')
cost_of_unit = m.number_input('Cost per Unit ($)', min_value=0.0, value=400.0, help='')
cost_of_unit_initialization = m.number_input('Cost per Unit Initialization ($)', min_value=0.0, value=80.0, help='Build + Lock + Lock Bracket')

cost_to_repair = r.number_input('Annual Cost of Maintenance Per Unit ($)', min_value=0.0, value=5.22, help='360 Blue Part Cost Per Property / Number of Average House Bikes Per Property', disabled=True)
cost_of_unit_per_year = r.number_input('Annual Cost of Unit ($)', value=(((cost_of_unit * (1 + interest_rate_of_unit / 100)) + cost_of_unit_initialization)/ number_of_years_to_payoff), help='(cost_of_unit * (1 + interest_rate_of_unit / 100)) + cost_of_unit_initialization) / number_of_years_to_payoff', disabled=True)

cost_of_b2b_auto_insurance = cost_of_auto_insurance * (percentage_of_revenue / 100)
cost_of_b2b_gas = cost_of_gas * (percentage_of_revenue / 100)
cost_of_b2b_vehicles = cost_of_vehicles * (percentage_of_revenue / 100)
cost_of_b2b_vehicle_maintenance = cost_of_vehicle_maintenance * (percentage_of_revenue / 100)
cost_of_b2b_software = (cost_of_software_per_month * 12) * (percentage_of_revenue / 100)

annual_b2b_expenses = r.number_input('Annual B2B Expenses ($)', value=(cost_of_labor + cost_of_b2b_auto_insurance + cost_of_b2b_gas + cost_of_b2b_vehicles + cost_of_b2b_vehicle_maintenance + cost_of_b2b_software), help='(cost_of_unit * (1 + interest_rate_of_unit / 100)) + cost_of_unit_initialization) / number_of_years_to_payoff', disabled=True)




if checks_file is not None:

    st.header('Results')

    df = pd.read_csv(checks_file, index_col = False)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df[(df['Date'] >= start) & (df['Date'] <= end)]

    activities_not_at_the_pointe = df[~(df.Location.str.contains('Pointe', na=False) | df.Location.str.contains('10711', na=False))]
    bike_checks = activities_not_at_the_pointe[activities_not_at_the_pointe.Activity.str.contains('BIKE CHECK')]
    bike_check_order_numbers = bike_checks.Order.unique()
    activites_with_a_bike_check = df[df.Order.isin(bike_check_order_numbers)]
    activites_without_gart = activites_with_a_bike_check[~activites_with_a_bike_check.Activity.str.contains('GART')]

    customers = activites_without_gart.Customer.unique()

    with st.expander('**Channel Partners**'):
        customer_option = st.multiselect('Under consideration', options=customers, default=customers)

    activites_final = activites_without_gart[activites_without_gart.Customer.isin(customer_option)]

    pivot_master = activites_without_gart.groupby('Location')['Activity'].count()
    pivot = activites_final.groupby('Location')['Activity'].count()

    number_of_b2b_stops = l.number_input('Number of Stops (#)', min_value=0.0, value=float(pivot_master.sum()), help='integraRental') # TODO
    cost_per_stop = r.number_input('Cost Per Stop ($)', min_value=0.0, value=annual_b2b_expenses / number_of_b2b_stops, help='What is the cost associated to each time we do a stop?', disabled=True)

    minimum_stops_at_a_property = pivot.min()
    average_stops_per_property  = pivot.mean()
    maximum_stops_at_a_property = pivot.max()

    with st.expander('**Math**'):
        l, m, r = st.columns(3)
        l.subheader('MIN')
        m.subheader('AVG')
        r.subheader('MAX')

        with st.container(border=True):
            st.write('**Counts**')
            l, m, r = st.columns(3)
            l.metric('Minimum Stops at a Property', round(minimum_stops_at_a_property))
            m.metric('Average Stops Per Property', round(average_stops_per_property))
            r.metric('Max Stops at a Property', round(maximum_stops_at_a_property))


        with st.container(border=True):
            st.write('**Per Property**')
            l, m, r = st.columns(3)
            l.metric('Cost of Minimum Stops at a Property', round(minimum_stops_at_a_property * cost_per_stop, 2))
            m.metric('Cost of Average Stops Per Property', round(average_stops_per_property * cost_per_stop, 2))
            r.metric('Cost of Max Stops at a Property', round(maximum_stops_at_a_property * cost_per_stop, 2))


        with st.container(border=True):
            st.write('**Per Average Units**')
            l, m, r = st.columns(3)
            l.metric('Cost of Minimum Stops at a Property Per Unit', round(minimum_stops_at_a_property * cost_per_stop / number_of_units_per_property, 2))
            m.metric('Cost of Average Stops Per Property Per Unit', round(average_stops_per_property * cost_per_stop / number_of_units_per_property, 2))
            r.metric('Cost of Max Stops at a Property Per Unit', round(maximum_stops_at_a_property * cost_per_stop / number_of_units_per_property, 2))

            l.metric('Annual Cost of Unit', round(cost_of_unit_per_year, 2))
            m.metric('Annual Cost of Unit', round(cost_of_unit_per_year, 2))
            r.metric('Annual Cost of Unit', round(cost_of_unit_per_year, 2))

            l.metric('Annual Cost of Maintenance Per Unit', round(cost_to_repair, 2))
            m.metric('Annual Cost of Maintenance Per Unit', round(cost_to_repair, 2))
            r.metric('Annual Cost of Maintenance Per Unit', round(cost_to_repair, 2))


    with st.container(border=True):
        st.write('**Cost Per Unit on House Program**')
        include_profit_margin = st.toggle('Include profit margin?', value=False)

        cost_per_unit_minimum_stops = minimum_stops_at_a_property * cost_per_stop / number_of_units_per_property + cost_of_unit_per_year + cost_to_repair
        cost_per_unit_average_stops = average_stops_per_property  * cost_per_stop / number_of_units_per_property + cost_of_unit_per_year + cost_to_repair
        cost_per_unit_maximum_stops = maximum_stops_at_a_property * cost_per_stop / number_of_units_per_property + cost_of_unit_per_year + cost_to_repair

        if include_profit_margin:
            cost_per_unit_minimum_stops = cost_per_unit_minimum_stops / (1 - (percentage_of_profit_margin / 100))
            cost_per_unit_average_stops = cost_per_unit_average_stops / (1 - (percentage_of_profit_margin / 100))
            cost_per_unit_maximum_stops = cost_per_unit_maximum_stops / (1 - (percentage_of_profit_margin / 100))

        st.write('**Per Year**')
        l, m, r = st.columns(3)
        l.metric('Based on Minimum Stops', round(cost_per_unit_minimum_stops,2))
        m.metric('Based on Average Stops', round(cost_per_unit_average_stops,2))
        r.metric('Based on Maximum Stops', round(cost_per_unit_maximum_stops,2))

        st.write('**Per Month**')
        l, m, r = st.columns(3)
        l.metric('Based on Minimum Stops', round(cost_per_unit_minimum_stops / 12, 2))
        m.metric('Based on Average Stops', round(cost_per_unit_average_stops / 12, 2))
        r.metric('Based on Maximum Stops', round(cost_per_unit_maximum_stops / 12, 2))

    st.divider()

    with st.expander('Notable Data Points'):
        st.info('Removed properties from The Pointe, where there was a delivery and pickup with each stay. We no longer do this. These properties are not considered.')