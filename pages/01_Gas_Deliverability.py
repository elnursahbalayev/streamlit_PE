import pandas as pd
import streamlit as st
from functions.gas_deliverability import Radius_of_investigation, Flow_after_flow
import numpy as np

requirement = st.selectbox('What do you want to calculate?', ['Radius of investigation', 'Flow After Flow test',
                                                              'Isochronal test', 'Modified Isochronal test'])

if requirement == 'Radius of investigation':
    if 'rinv_data' not in st.session_state:
        st.session_state['rinv_data'] = [0.0,0.0,0.0,0.0,0.0,0.0]

    st.write('Please input the necessary data below')
    k = st.number_input('Permeability k(mD)', value=st.session_state['rinv_data'][0], format='%f')
    pr = st.number_input('Average reservoir pressure (psia)', value=st.session_state['rinv_data'][1], format='%f')
    fi = st.number_input('Porosity', value=st.session_state['rinv_data'][2], format='%f')
    mu = st.number_input('Viscosity (cP)', value=st.session_state['rinv_data'][3], format='%f')
    re = st.number_input('Reservoir boundary (ft)', value=st.session_state['rinv_data'][4], format='%f')
    t = st.number_input('Time passed (hr)', value=st.session_state['rinv_data'][5], format='%f')

    st.session_state['rinv_data'] = [k, pr, fi, mu, re, t]

    if 0 not in (k, pr, fi, mu, re, t):
        ts = Radius_of_investigation.calculate_stabilization_time(k, pr, fi, mu, re, t)
        rinv = Radius_of_investigation.calculate_radius_of_investigation(k, pr, t, fi, mu, ts, re)

        st.latex(r't_s = \frac{1000 \cdot \phi \cdot \mu \cdot r_e^2}{k \cdot p_R}')
        st.latex(f't_s = \\frac{{1000 \\cdot {fi} \\cdot {mu} \\cdot {re}^2}}{{{k} \\cdot {pr}}}')
        st.latex(f't_s = {np.round(ts,3)} \\text{{ hours}}')
        st.write('\n')

        st.latex(r'r_\text{inv} = 0.032 \sqrt{\frac{k \cdot p_R \cdot t}{\phi \cdot \mu_g}}')
        st.latex(f'r_\\text{{inv}} = 0.032 \\sqrt{{\\frac{{{k} \\cdot {pr} \\cdot {t}}}{{{fi} \\cdot {mu}}}}}')
        st.latex(f'r_\\text{{inv}} = {np.round(rinv,2)} \\text{{ ft}}')

elif requirement == 'Flow After Flow test':
        num_of_tests = int(st.number_input('How many tests were conducted?', format='%i', value=0))
        q_values = [st.number_input(f'Q{i+1} (mscf)') for i in range(num_of_tests)]
        pwf_values = [st.number_input(f'Pwf{i+1} (psia)') for i in range(num_of_tests)]
        pr = st.number_input('Initial Reservoir pressure (psia)', format='%f')
        values_df = {'Qsc (Mscf/D)':q_values, 'Pwf (psia)':pwf_values}
        values_df = pd.DataFrame(values_df)

        values_df = Flow_after_flow.pressure_difference_squared(values_df, pr)
        st.write(values_df)
        if len(values_df) == num_of_tests and len(values_df) != 0:
            c_plot = Flow_after_flow.plot_log_log_of_C(values_df, pr)
            st.plotly_chart(c_plot)

            n = Flow_after_flow.find_n(values_df)
            st.latex( )

elif requirement == 'Isochronal test':
    st.write('isoch')

elif requirement == 'Modified Isochronal test':
    st.write('modified')