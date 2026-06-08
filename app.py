import streamlit as st
import pandas as pd
import joblib

model = joblib.load('inventory_model.pkl')
features = joblib.load('model_features.pkl')

st.title('FMCG Inventory Status Predictor')
st.write('Enter product details to predict inventory status and get business recommendations.')

st.subheader('Enter Product Details')

Days_Since_Last_Sale = st.number_input('Days Since Last Sale', min_value=0, value=30)
Current_Stock_Qty = st.number_input('Current Stock Quantity', min_value=0, value=100)
Reorder_Point = st.number_input('Reorder Point', min_value=0, value=50)
Lead_Time_Days = st.number_input('Lead Time Days', min_value=0, value=7)
Days_To_Expiry = st.number_input('Days To Expiry', min_value=0, value=90)
Total_Qty_Sold = st.number_input('Total Quantity Sold', min_value=0, value=500)
Total_Revenue_INR = st.number_input('Total Revenue (₹)', min_value=0, value=50000)
Total_Profit_INR = st.number_input('Total Profit (₹)', min_value=0, value=5000)
Avg_Unit_Sell_INR = st.number_input('Avg Unit Sell Price (₹)', min_value=0, value=200)
Avg_Unit_Cost_INR = st.number_input('Avg Unit Cost Price (₹)', min_value=0, value=150)
Return_Count = st.number_input('Return Count', min_value=0, value=2)

if st.button('Predict'):
    input_data = pd.DataFrame([[Days_Since_Last_Sale, Current_Stock_Qty, Reorder_Point,
                                 Lead_Time_Days, Total_Qty_Sold, Total_Revenue_INR,
                                 Total_Profit_INR, Avg_Unit_Sell_INR, Avg_Unit_Cost_INR,
                                 Return_Count, Days_To_Expiry]], columns=features)

    prediction = model.predict(input_data)[0]

    status_map = {0: 'Healthy', 1: 'Slow Moving', 2: 'Dead Stock'}
    status = status_map[prediction]

    risk_map = {
        'Healthy': 'Low',
        'Slow Moving': 'Medium',
        'Dead Stock': 'High'
    }

    recommendations = {
        'Healthy': 'Stock is performing well. Maintain current stock levels and monitor regularly.',
        'Slow Moving': 'Sales are slow. Run promotions, offer discounts or reduce reorder quantity.',
        'Dead Stock': 'No recent sales. Liquidate stock immediately, stop reordering and investigate root cause.'
    }

    risk = risk_map[status]

    st.subheader(f'Prediction: {status}')
    st.write(f'Risk Level: {risk}')
    st.info(f'Recommendation: {recommendations[status]}')