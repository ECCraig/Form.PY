import os
import json
import pandas as pd
import datetime as dt
import streamlit as st

# Start page
print('=' * 100)
print('Starting app')
st.set_page_config('POC Spend')
st.header('POC Spend')

# Create tabs
tab1, tab2, tab3 = st.tabs(['Input', 'Remove', 'Dashboard'])

# Tab 1: Input
with tab1:
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
    input_contract_value = st.number_input('Total Contract Value', min_value=0, step=1)
    input_number_of_payments = st.number_input('Number of payments to be submitted', 1, 60, step=1)

    # Create input payments
    col1, col2 = st.columns(2)
    for i in range(1, input_number_of_payments+1):
        with col1:
            st.date_input(f'Payment date {i}', key=f'date{i}')
        with col2:
            st.number_input(f'Payment Amount {i}', key=f'amount{i}', min_value=0, step=1)

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
        current_time = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
        json_object = json.dumps(entered_data, indent=4)
        with open(f'./inputdata/{current_time}_{input_owner}.json','w') as f:
            f.write(json_object)

        # Confirm success back to user
        entered_data_pretty = pd.Series(entered_data).to_frame().T
        st.write(f'Successfully submitted:')
        st.dataframe(entered_data_pretty, hide_index=True)

# Tab 2: Remove
with tab2:

    # Add user selection
    st.subheader('Remove a submitted entry')
    filenames = os.listdir('./inputdata')
    names = [i.split('_')[2].replace('.json','') for i in filenames]
    selected_user = st.selectbox('Select name', names, index=None)
    if selected_user:
        selected_filenames = pd.DataFrame([[i, False] for i in filenames if selected_user in i], columns=['Filename', 'Remove'])
        df_filenames = st.data_editor(selected_filenames, hide_index=True)
    
    # Add button to remove selected filenames
    button = st.button('Remove selected rows')
    if button:
        files_to_remove = df_filenames[df_filenames['Remove'] == True]['Filename'].tolist()
        for filename in files_to_remove:
            print(f'Removing filename: {filename}')
            os.remove(f'./inputdata/{filename}')

# Tab 3: Show data
with tab3:

    # Load all json files into single dataframe
    filenames = os.listdir('./inputdata')
    dataframes = []
    if len(filenames) == 0:
        st.info('Er zijn nog geen bestanden geupload')
    else:
        for filename in filenames:
            with open(f'./inputdata/{filename}') as f:
                json_obj = json.load(f)
                metadata_columns = [c for c in json_obj if c != 'payments']
                df_tmp = pd.json_normalize(json_obj, record_path='payments', meta=metadata_columns)
                dataframes.append(df_tmp)
        df = pd.concat(dataframes)

        # Finalize columns
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['amount'] = pd.to_numeric(df['amount'])
        final_columns = metadata_columns + ['date', 'amount']
        df = df[final_columns]

        # Display line chart: amount per month within calendar year
        df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
        df_month = df.groupby(['month']).agg({'amount': sum}).reset_index().sort_values('month', ascending=True)
        df_month['month_int'] = df_month['month'].dt.month.astype(int)
        df_month['year_int'] = df_month['month'].dt.year
        df_pivoted = df_month.pivot(index='month_int', columns=['year_int'], values='amount')
        df_pivoted = df_pivoted.fillna(0)
        st.subheader('Spend')
        st.line_chart(df_pivoted)

        # Display dataframe
        st.subheader('All data')
        st.dataframe(df, hide_index=True)
