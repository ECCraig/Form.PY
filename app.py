import os
import json
import pandas as pd
import datetime as dt
import streamlit as st

# Start page_
print('=' * 100)
print('Starting app')
st.set_page_config('POC Spend')
col1, col2 = st.columns([5,1])
with col1:
    st.header('POC Spend')
with col2:
    st.image('centric_logo.png', use_column_width=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(['Input', 'Remove', 'Dashboard'])

# Tab 1: Input
with tab1:
    # Predefine selection options
    options_company = ['BAKER', 'BITLI', 'CITS', 'CFSS', 'CHOLD', 'GDA02', 'KRLSC', 'MISHO', 'PST', 'QMAGI', 'QMUZB']
    options_department = ['HR', 'Finance', 'IT', 'Operations', 'Facilities']
    options_division = ['DBS: Business Operations', 'PS: Professional Staffing', 'PSS: Public Sector Solutions', 'SC: Supply Chain Solutions', 'SE: Software Engineering']
    options_vendor = ['A&J IT-Solutions BV', 'Adesso Netherlands B.V.', 'ADF Recruitment', 'Advanced Programs Managed Services', 'Advantage IT-consulting B.V.', 'Adyen N.V.', 'AKAM Netherlands B.V.', 'Albron Nederland B.V.', 'Alphabet Nederland BV', 'ALSO Nederland B.V', 'Amelia NL B.V.', 'Andarr Technology Professionals', 'Antea Nederland B.V.', 'AnyLinQ BV', 'Arrow ECS B.V.', 'Arval B.V.', 'ARX Corporate Consultants B.V.', 'Atos Nederland B.V.', 'Avero Achmea Verzekeringen N.V.', 'Backoffice Groep B.V.', 'BakerWare B.V.', 'Base Logistics B.V.', 'Base Select B.V.', 'BBD Security & Facility B.V.', 'Bconsult B.V.', 'BCS HR Software B.V.', 'BeFrank PPI N.V.', 'BeGlobal B.V.', 'Blauwtand IT-Detachering B.V.', 'BlueMesa BV', 'BT Nederland N.V.', 'Canalize B.V.', 'CBE - Staffing', 'CBE - Supply Chain Solutions', 'CCV Nederland', 'Centric IT Solutions Lithuania UAB', 'Centric IT Solutions Romania', 'Centric IT Solutions Sweden AB', 'Centric MS BU 2501 Financial', 'Centric Netherlands BV', 'Cloudlr B.V.', 'CNL - DBS (Digital Business Sol.)', 'CodeBinder', 'Coffee Fresh Holland B.V.', 'cognition IT B.V.', 'COLT Technology Services BV', 'Commvault Systems International B.V', 'ConsultingExperts B.V.', 'Copaco Nederland B.V.', 'Crayon B.V.', 'Cyclomedia', 'D. Heemskerk (GoStart)', 'Dataiku B.V.', 'Decos Software Engineering BV', 'Dell  B.V.', 'Delphi Dreams VOF', 'DigiWyse B.V.', 'DitP Detachering IT Professionals', 'Doeleman Logistiek B.V.', 'dormakaba Nederland B.V.', 'DRAF Consultancy', 'Duranmatic B.V.', 'Dynamics ATS', 'Dynatos B.V.', 'EIC BV', 'Empiric Netherlands B.V.', 'EnablE-U B.V.', 'Eqeep Benelux B.V.', 'Equinix Netherlands BV', 'Escalar4Business', 'Eurodesk Business Furniture', 'Eurofiber Nederland BV', 'Evers Soerjatin N.V.', 'FinanceFactor B.V.', 'Flex Testing B.V.', 'Florent B.V.', 'Forma (Netherlands) IV B.V.', 'Fortra International Limited', 'Fujitsu Technology Solutions B.V.', 'G4S Security Services bv', 'Global Knowledge Netherlands B.V.', 'Goed IT-Services', 'Goudse Schadeverzekeringen N.V.', 'Greenchoice', 'Greenchoice Zakelijk NV', 'GTT Communications Netherlands B.V.', 'Heineken Sligro Sticht Derdengelden', 'Hero Interim Professionals B.V.', 'HET IT BV', 'Hewlett-Packard Nederland B.V.', 'HP France SAS', 'HP International Bank DAC', 'HP Nederland B.V.', 'Hulst Beveiligingstechniek B.V.', 'IBM NEDERLAND B.V.', 'ICBI B.V.', 'ICT Zaakwaarnemer B.V.', 'ICT4YOU B.V.', 'ICT-Solve BV', 'Igen B.V.', 'Ingram Micro B.V.', 'Innvolve Professional Services B.V.', 'Interconnect services bv', 'Intronics B.V.', 'InWork B.V.', 'IRIS Informatique Headquarters', 'ISS US Consultancy B.V.', 'ITHEC ICT B.V.', 'ITQ Consultancy B.V.', 'Itrix IT Solutions BV', 'IT-Strategy', 'IT-to-IT B.V.', 'ITvitae Detachering B.V.', 'Ivanti UK Limited', 'J.L. - Productions B.V.', 'Jan Bakker Consulting', 'Jarltech Europe GmbH', 'Jedalo ICT', 'JenJIT Managed Services B.V.', 'JNC Automatisering', 'Joulz Infradiensten B.V.', 'KaKeJo', 'Kaseya B.V.', 'KOK Schoonmaak', 'Koning & Hartman B.V.', 'KP 0180 Interne Automatisering', 'KP 2700 MS DataCenter Services', 'KPL 0181 BU IIT - BIM', 'KPL 2600 MS PUBLIC', 'KPL 2800 MS BUSINESS', 'KPL 3400 Interne Doorbelasting', 'KPL 4300  Interne Doorbelasting', 'KPMG Advisory N.V.', 'KPMG Audit', 'KPMG Meijburg & Co', 'KPN', 'Lagant Management Consultants', 'Larmag Real Estate 6 B.V.', 'LeasePlan Nederland N.V.', 'Lexmark International Netherlands', 'Lifecycle Technology Limited', 'Lindeberg Holding B.V.', 'Linkedin Ireland Unlimited Company', 'M7 EREIP III LUX MASTER S.A.R.L.', 'Maandag IT B.V.', 'Macee B.V.', 'Magenta Technology Consultants B.V.', 'MagicByte', 'Marathon Computers B.V.', 'Marsh B.V.', 'MB Management Professional BV', 'McEffem', 'MelFin Management B.V.', 'Mensys The Software Catalogue', 'Merlin Security Services', 'Micro Focus B.V.', 'Microsoft B.V.', 'Microsoft Ireland Operations Ltd', 'Molenaar & Plasman Solutions B.V.', 'Mous Management & Consultancy BV', 'MukiCo BV', 'Myleasecar B.V.', 'NCR Nederland B.V.', 'Network Team Leusden B.V.', 'NetworkPeople B.V.', 'Newspark B.V.', 'NexyZ B.V.', 'Nintex UK Ltd', 'NLmatch B.V.', 'nocolo - holding B.V.', 'NS Reizigers B.V.', 'NXTcom Nederland B.V.', 'OK Service Koeriersdienst B.V.', 'Oracle Nederland B.V leverancier', 'Ordina Nederland BV', 'Ormer ICT Staffing B.V.', 'Pan Oston', 'Partner Tech Europe GmbH', 'Peoples Republic B.V.', 'Peter Dijkman IT Consultancy BV', 'PJVD - Finance.com B.V.', 'POS Service GmbH', 'PPD Consultancy', 'Premium Business Consultants BV', 'Prianto GmbH', 'Progress Software B.V.', 'Prolocation', 'Protinus IT BV', 'Prowareness WeOn Group B.V.', 'Qconferencing B.V.', 'Q-Logic B.V.', 'Qmagic Uitzendbureau B.V.', 'QoppoConsult B.V.', 'Quality Projects B.V.', 'QuandaGo International B.V.', 'Querion IT', 'Qure - IT Solutions', 'R.H.M.J. Gerits h.o.d.n. IOPS4U', 'Rabobank FSC Centrale dbiteurenadm', 'Rabobank Ned. Creditcard', 'Randstad Uitzendbureau, Facturering', 'Reconi B.V.', 'Recruitment SolutionZ B.V.', 'Redcoat IT BV', 'Redkiwi', 'Redtail B.V.', 'Renewi Nederland B.V.', 'Retail Techwise', 'Retex SPA', 'Revality ICT Services B.V.', 'Roan Medische Advisering B.V.', 'RockxNL', 'Rolf Pronk Management', 'Routz network executives (SSC Plus)', 'RSM Netherlands Accountans N.V.', 'Rutgers & Posch N.V.', 'RuudB.IT', 'Safescan', 'Safewhere A/S', 'Sempre Solucions B.V.', 'SenTech Consultancy', 'Sequint', 'ServiceNow Nederland B.V.', 'ShareValue B.V.', 'Signetbreedband B.V.', 'SLTN BTS B.V.', 'SLTN IT Professionals BV', 'Software Foundry B.V.', 'Sopra Banking Software France', 'Sopra Banking Software Luxembourg', 'Speedliner Logistics B.V.', 'SPIE Building Solutions B.V.', 'Stibbe N.V.(Advocatuur)', 'Stratech Automatisering B.V.', 'Streetwise Solutions Holding B.V.', 'Studytube B.V.', 'Stuurman ICT Consulting', 'Su IT B.V.', 'T:MEBLOCKR B.V.', 'Tannenbaum Management B.V.', 'TD SYNNEX Netherlands B.V.', 'Telindus - ISIT B.V.', 'TEMEHA Consultancy', 'Temenos Headquarters SA', 'Temenos UK Ttd.', 'Tentoo Directors Cast & Crew B.V.', 'Terberg Business Lease Group B.V.', 'The NextGen B.V.', 'Thirdera NLD BV', 'Together Detachering BV', 'ToKalon', 'TOPdesk Nederland B.V.', 'Toshiba Global Commerce Solutions', 'TPS Interim Professionals B.V.', 'Turn To Tech', 'UPOS System Slovakia SRO', 'UWV VFV Verhaalsdebiteuren', 'VAANSTER IV B.V.', 'Valdevie B.V.', 'Van Kaam Advocaten', 'Van Mossel Leasing B.V.', 'Van Olphen Company B.V.', 'Van Wijngaarden ICT Services', 'VCK Travel B.V.', 'Venafi Inc.', 'Verhuisbedrijf Henneken BV', 'ViPcom B.V.', 'Virtu Secure Webservices BV', 'Vodafone Libertel BV', 'Volant Groep B.V.', 'VYZYR B.V.', 'Wakkie & Perrick B.V.', 'Wave Consulting', 'Wiconic (Search4Solutions B.V.)', 'Wielinga IT Services B.V.', 'Willis B.V.', 'Working Talent B.V.', 'Worldline Nederland', 'xxllnc Omgeving B.V.', 'Yacht B.V.', 'YC Professionals Talent Development', 'Your Professionals B.V.', 'Zebra Technologies Europe Ltd', 'ZETA IT B.V.', 'ZZZZZZKaba Nederland B.V.']
    options_content = ['Gifts', 'Hardware', 'Licences', 'Office Supplies', 'Personell', 'Services', 'Software']
    options_payment_patern = ['Once', 'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Yearly']


    # Create input metadata
    st.subheader('Basic information')

    col1, col2 = st.columns(2)
    with col1:
        st.date_input('Contract start date')
    with col2:
        st.date_input('Contract end date')

    input_owner = st.text_input('Contract owner')
    input_email_address = st.text_input('Email address owner')
    input_link_to_document = st.text_area('Links to documents')
    input_company = st.selectbox('Holding company', options_company, None)
    input_department = st.selectbox('Department', options_department, None)
    input_holding_division = st.selectbox('Holding division', options_division, None)
    # input_contract_code = st.text_input('Contract code')
    input_vendor = st.selectbox('Vendor', options_vendor, None)
    input_vendor_alt = st.text_input('Vendor (if not listed)')
    vendor = input_vendor or input_vendor_alt
    input_content = st.selectbox('Content categorie', options_content, None)
    input_content_description = st.text_area('Content description')
    
    st.subheader('Financial information')
    input_contract_payment_terms = st.number_input('Payment Terms (days)', min_value=0, step=1)
    input_contract_budget = st.number_input('Total Contract Budget', min_value=0, step=1)
    input_contract_spend = st.number_input('Total Contract Spend', min_value=0, step=1)
    input_contract_revenu = st.number_input('Total Contract Revenu', min_value=0, step=1)
    st.metric(label='Total Contract Margin', value=input_contract_revenu - input_contract_spend, delta=None)
    input_contract_payment_patern = st.selectbox('Payment Patern', options_payment_patern, None)
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
        df_month = df.groupby(['month']).agg({'amount': 'sum'}).reset_index().sort_values('month', ascending=True)
        df_month['month_int'] = df_month['month'].dt.month.astype(int)
        df_month['year_int'] = df_month['month'].dt.year
        df_pivoted = df_month.pivot(index='month_int', columns=['year_int'], values='amount')
        df_pivoted = df_pivoted.fillna(0)
        st.subheader('Spend')
        st.line_chart(df_pivoted, color=['#0DBB1E', '#AFF1B5'])

        # Display dataframe
        st.subheader('All data')
        st.dataframe(df, hide_index=True)
