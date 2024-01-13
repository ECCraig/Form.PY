import json
import pandas as pd
import datetime as dt
import streamlit as st

# Start page
print('=' * 100)
print('Starting app')
st.set_page_config('POC Spend')
st.header('POC Spend')

# Predefine selection options
options_company = ['C1', 'C2']
options_department = ['HR', 'Finance', 'IT', 'Operations', 'Facilities']
options_division = ['D1', 'D2']
options_vendor = ['v1','v2']

# Create input metadata
input_owner = st.text_input('Owner')
input_company = st.selectbox('Company', options_company, None)
input_department = st.selectbox('Department', options_department, None)
input_holding_division = st.selectbox('Holding division', options_division, None)
input_contract_code = st.text_input('Contract code')
input_vendor = st.selectbox('Vendor', options_vendor, None)
input_vendor_alt = st.text_input('Vendor (if not listed)')
vendor = input_vendor or input_vendor_alt
input_contract_value = st.number_input('Total Contract Value')
input_number_of_payments = st.number_input('Number of payments to be submitted', 1, 60, step=1)

# Create input payments
col1, col2 = st.columns(2)
for i in range(1, input_number_of_payments+1):
    with col1:
        st.date_input(f'Payment date {i}', key=f'date{i}')
    with col2:
        st.number_input(f'Payment Amount {i}', key=f'amount{i}')

# Submit button
submitted = st.button('Submit')
if submitted:

    # Extract all payments from streamlit session state
    all_dates = [v for k,v in st.session_state.items() if 'date' in k]
    all_amounts = [v for k,v in st.session_state.items() if 'amount' in k]
    all_payments = [{'date': str(date), 'amount': str(amount)} for date, amount in zip(all_dates, all_amounts)]

    # Save input data to json file
    entered_data = {
        'owner': input_owner,
        'company': input_company,
        'department': input_department,
        'holding_division': input_holding_division,
        'contract_code': input_contract_code,
        'vendor': vendor,
        'payments': all_payments
        }
    current_time = dt.datetime.now().strftime('%Y%m%d%H%M%S')
    json_object = json.dumps(entered_data, indent=4)
    with open(f'./inputdata/{current_time}.json','w') as f:
        f.write(json_object)

    # Confirm success back to user
    entered_data_pretty = pd.Series(entered_data).to_frame().T
    st.write(f'Successfully submitted:')
    st.dataframe(entered_data_pretty, hide_index=True)
