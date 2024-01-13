import json
import pandas as pd
import datetime as dt
import streamlit as st

# Start page
st.set_page_config('POC Spend')
st.header('POC Spend')

# Predefine selection options
options_company = ['C1', 'C2']
options_department = ['HR', 'Finance', 'IT', 'Operations', 'Facilities']
options_division = ['D1', 'D2']
options_vendor = ['v1','v2']

# Create input form
with st.form('input_form', clear_on_submit=True):
    input_owner = st.text_input('Owner')
    input_company = st.selectbox('Company', options_company, None)
    input_department = st.selectbox('Department', options_department, None)
    input_holding_division = st.selectbox('Holding division', options_division, None)
    input_contract_code = st.text_input('Contract code')
    input_vendor = st.selectbox('Vendor', options_vendor, None)
    input_vendor_alt = st.text_input('Vendor (if not listed)')
    vendor = input_vendor or input_vendor_alt
    

   # Submit button
    submitted = st.form_submit_button('Submit')
    if submitted:

        # Save input data to json file
        entered_data = {
            'owner': input_owner,
            'company': input_company,
            'department': input_department,
            'holding_division': input_holding_division,
            'contract_code': input_contract_code,
            'vendor': vendor
            }
        current_time = dt.datetime.utcnow().strftime('%Y%m%d%H%M%S')
        json_object = json.dumps(entered_data, indent=4)
        with open(f'./inputdata/{current_time}.json','w') as f:
            f.write(json_object)

        # Confirm success back to user
        entered_data_pretty = pd.Series(entered_data).to_frame().T
        st.write(f'Successfully submitted:')
        st.dataframe(entered_data_pretty, hide_index=True)
