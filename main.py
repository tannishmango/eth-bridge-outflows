import streamlit as st
import os

#  python3.10 -m streamlit run main.py


def set_rpc_url(rpc_url: str):
    os.environ.setdefault('RPC_URL', rpc_url)

new_rpc_url = st.text_input(
    "Set your rpc url:",
    key='rpc'
)

st.button(
    'Add rpc',
    key='button_add_rpc',
    on_click=set_rpc_url,
    args=(new_rpc_url, )
)


def set_etherscan(etherscan_key: str):
    os.environ.setdefault('ETHERSCAN', etherscan_key)

new_etherscan_key = st.text_input(
    "Set your etherscan api key:",
    key='etherscan'
)

st.button(
    'Add etherscan api',
    key='button_add_etherscan',
    on_click=set_etherscan,
    args=(new_etherscan_key, )
)


def fetch_data(start_date):
    start_date = str(start_date)
    from data_fetch import get_bridge_data
    data = get_bridge_data(start_date)
    sub_df = data.drop(["amount","timestamp"],axis=1)
    sub_df["amount_usd"] = sub_df["amount_usd"].apply(lambda x: float(x))
    st.dataframe(sub_df)

start_date = st.date_input(
    "Select the start date you want to get data from:",
    key="date"
)

st.button(
    'Add start date',
    key='button_add_start_date',
    on_click=fetch_data,
    args=(start_date, )
)

