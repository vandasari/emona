import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import datetime
from datetime import timedelta
from streamlit_extras.metric_cards import style_metric_cards


def plot_metric(label, value, prefix="", suffix="", show_graph=False, color_graph=""):
    fig = go.Figure()
    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={"prefix": prefix, "suffix": suffix, "font.size": 28},
            title={
                "text": label,
                "font": {"size": 24},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=random.sample(range(1, 101), 30),
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={"color": color_graph},
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)

    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        plot_bgcolor="white",
        height=100,
    )

    st.plotly_chart(fig, use_container_width=True)


# ##--- Title ---
# st.set_page_config(
#     page_title="Energy Monitoring & Analysis",
#     page_icon=":control_knobs:",
#     layout="wide",
# )

st.header(":control_knobs: PT Central Panganpertiwi", anchor=False)
st.markdown(
    "<style>div.block-container(padding-top:2rem;)</style>", unsafe_allow_html=True
)

current = datetime.datetime.now()
current_date = current.strftime("%d-%m-%Y")
current_day = current.strftime("%A")
current_time = current.strftime("%H:%M:%S")

##--- 4 column
col01, col02, col03 = st.columns(3, gap="large")

with col01:
    st.success(f"☀️ {current_day}")

with col02:
    st.info(f"🗓️ {current_date}")

with col03:
    st.warning(f"⏰ {current_time}")


st.write("\n")

left, middle, right = st.columns(3, gap="small", border=True)

with left:
    plot_metric(
        "Biaya per kWh",
        1440,
        prefix="Rp",
        suffix="",
        show_graph=True,
        color_graph="rgba(203, 195, 227, .5)",
    )

with middle:
    plot_metric(
        "Total Konsumsi",
        163027,
        prefix="",
        suffix="W",
        show_graph=True,
        color_graph="rgba(253, 237, 236, 1)",
    )

with right:
    plot_metric(
        "Total Biaya",
        1630270,
        prefix="Rp",
        suffix="",
        show_graph=True,
        color_graph="rgba(242, 244, 244, 1)",
        # color_graph="rgba(234, 236, 238, 1)",
        # color_graph="rgba(255, 43, 43, 0.1)",
    )

st.markdown("---")

st.write("\n")

##############################

st.subheader("Jumlah Mesin", anchor=False)

col11, col12, col13 = st.columns(3, border=True)

with col11:
    # st.metric(label="Total Mesin", value=300)
    # st.caption("Jumlah total semua mesin, beroperasi dan tidak beroperasi.")
    st.markdown("#### Total Semua Mesin:")
    st.markdown("### 300")
    machines = pd.DataFrame(
        [
            {"Machine": "Hammer Mill", "Total": 8},
            {"Machine": "Automizer Fulveizer", "Total": 2},
            {"Machine": "Extruder", "Total": 6},
            {"Machine": "Pellet Mill", "Total": 3},
            {"Machine": "Blower - Bag Filter", "Total": 3},
            {"Machine": "Mixer Dry", "Total": 1},
            {"Machine": "Blower", "Total": 7},
            {"Machine": "Mixer Wet Floating", "Total": 2},
            {"Machine": "Mixer Wet Sinking", "Total": 1},
        ]
    )

    with st.expander("Lihat semua mesin"):
        st.dataframe(machines, hide_index=True)

with col12:
    # st.metric(label="Mesin Beroperasi", value=295)
    # st.caption("Jumlah mesin yang beroperasi.")
    st.markdown("#### Mesin Yang Beroperasi:")
    st.markdown("### 295")
    operating_machines = pd.DataFrame(
        [
            {"Machine": "Hammer Mill", "Operating": 6},
            {"Machine": "Automizer Fulveizer", "Operating": 1},
            {"Machine": "Extruder", "Operating": 6},
            {"Machine": "Pellet Mill", "Operating": 3},
            {"Machine": "Blower - Bag Filter", "Operating": 3},
            {"Machine": "Mixer Dry", "Operating": 1},
            {"Machine": "Blower", "Operating": 7},
            {"Machine": "Mixer Wet Floating", "Operating": 2},
            {"Machine": "Mixer Wet Sinking", "Operating": 1},
        ]
    )

    with st.expander("Lihat mesin yang beroperasi"):
        st.dataframe(operating_machines, hide_index=True)

with col13:
    # st.metric(label="Mesin Tidak Beroperasi", value=5)
    # st.caption("Jumlah mesin yang tidak beroperasi.")
    st.markdown("#### Mesin Tidak Beroperasi:")
    st.markdown("### 5")
    non_operating_machines = pd.DataFrame(
        [
            {"Machine": "Hammer Mill", "Non-Op": 2},
            {"Machine": "Automizer Fulveizer", "Non-Op": 1},
            {"Machine": "Extruder", "Non-Op": 0},
            {"Machine": "Pellet Mill", "Non-Op": 0},
            {"Machine": "Blower - Bag Filter", "Non-Op": 0},
            {"Machine": "Mixer Dry", "Non-Op": 0},
            {"Machine": "Blower", "Non-Op": 0},
            {"Machine": "Mixer Wet Floating", "Non-Op": 0},
            {"Machine": "Mixer Wet Sinking", "Non-Op": 0},
        ]
    )

    with st.expander("Lihat mesin tidak beroperasi"):
        st.dataframe(non_operating_machines, hide_index=True)

st.markdown("---")
st.write("\n")

##############################

st.subheader("Konsumsi Listrik", anchor=False)
st.write(
    """ 
    Konsumsi harian listrik real-time yang dibandingkan dengan konsumsi hari sebelumnya pada saat yang sama.
    """
)

col21, col22, col23 = st.columns((3))


# with col11:
#     st.markdown(
#         "<div style='text-align:center'>Consumption (Wh/day)</div>",
#         unsafe_allow_html=True,
#     )
#     st.write("23.9k")


with col21:
    st.metric(label="Konsumsi Harian - Motor (kWh)", value="23.9k", delta="-1.2k")
    style_metric_cards(border_left_color="#003366")


with col22:
    st.metric(label="Konsumsi Harian - Kompresor (kWh)", value="46.1k", delta="4.5k")
    style_metric_cards(border_left_color="#003366")

with col23:
    st.metric(
        label="Konsumsi Harian Total (kWh/month)",
        value="50",
        delta="-0.5k",
        border=True,
    )
    style_metric_cards(border_left_color="#003366")

st.markdown("---")


data = pd.read_csv("data/powerconsumption.csv")

##--- Convert Datetime column to just date
data["Date"] = pd.to_datetime(data["Datetime"]).dt.date
max_date = data["Date"].max()
min_date = data["Date"].min()

default_start_date = min_date
default_end_date = max_date

# date_left, date_right = st.columns(2, gap="large")

# with date_left:
#     start_date = st.date_input(
#         "Start date",
#         default_start_date,
#         min_value=data["Date"].min(),
#         max_value=max_date,
#     )

# with date_right:
#     end_date = st.date_input(
#         "End date",
#         default_end_date,
#         min_value=data["Date"].min(),
#         max_value=max_date,
#     )

selected_date = st.slider(
    "Geser slider untuk memilih rentang tanggal",
    min_value=default_start_date,
    max_value=default_end_date,
    value=(default_start_date, default_end_date),
    step=timedelta(days=1),
)

df_display = data.set_index("Date")

mask = (df_display.index >= selected_date[0]) & (df_display.index <= selected_date[1])

filtered_data = df_display.loc[mask]
x_obj = filtered_data["Datetime"]
y_obj = filtered_data["PowerConsumption_Zone1"]

line_chart = px.line(x=x_obj, y=y_obj)
st.plotly_chart(line_chart)
