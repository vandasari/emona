import streamlit as st
import pytz
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import datetime
import locale
from datetime import timedelta
from streamlit_extras.metric_cards import style_metric_cards

# from visualization import plot_metric
# import visualization

st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 2rem;
        margin-top: -2rem;
    }
    .sub-header {
        font-size: 1.75rem;
        font-weight: bold;
        color: #0D47A1;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Title and intro
st.markdown(
    '<div class="main-header">PT Central Panganpertiwi</div>',
    unsafe_allow_html=True,
)

# st.header(":control_knobs: PT Central Panganpertiwi", anchor=False)
# st.markdown(
#     "<style>div.block-container(padding-top:2rem;)</style>", unsafe_allow_html=True
# )


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

#####---------- Times dan Dates ----------#####

jakarta_tz = pytz.timezone("Asia/Jakarta")
current = datetime.datetime.now(jakarta_tz)
current_date = current.strftime("%d-%m-%Y")
# current_day = current.strftime("%A")
current_weekday = current.weekday()
current_time = current.strftime("%H:%M:%S")

if current_weekday == 0:
    current_day = "Senin"
elif current_weekday == 1:
    current_day = "Selasa"
elif current_weekday == 2:
    current_day = "Rabu"
elif current_weekday == 3:
    current_day = "Kamis"
elif current_weekday == 4:
    current_day = "Jumat"
elif current_weekday == 5:
    current_day = "Sabtu"
else:
    current_day = "Minggu"

datetime_left, datetime_middle, datetime_right = st.columns(3, gap="large")

with datetime_left:
    st.success(f"☀️ {current_day}")

with datetime_middle:
    st.info(f"🗓️ {current_date}")

with datetime_right:
    st.warning(f"⏰ {current_time}")


st.write("\n")

#####---------- Biaya per kWh, Total Pemakaian, Estimasi Total Biaya ----------#####

total_left, total_middle, total_right = st.columns(3, gap="small", border=True)

with total_left:
    plot_metric(
        "Biaya per kWh",
        1440,
        prefix="Rp ",
        suffix="",
        show_graph=True,
        color_graph="rgba(203, 195, 227, .5)",
    )

with total_middle:
    plot_metric(
        "Total Pemakaian",
        163027,
        prefix="",
        suffix="Wh",
        show_graph=True,
        color_graph="rgba(253, 237, 236, 1)",
    )

with total_right:
    plot_metric(
        "Estimasi Total Biaya",
        74877321,
        prefix="Rp ",
        suffix="",
        show_graph=True,
        color_graph="rgba(242, 244, 244, 1)",
        # color_graph="rgba(234, 236, 238, 1)",
        # color_graph="rgba(255, 43, 43, 0.1)",
    )

# st.divider()

# st.write("\n")

#####---------- Bermacam Pemakaian ----------#####
st.markdown(
    '<div class="sub-header">Distribusi Pemakaian Hari Ini</div>',
    unsafe_allow_html=True,
)

usage_left, usage_middle, usage_right = st.columns(3)

with usage_left:
    data_section = {
        "Section": [
            "Bag Go Down 1",
            "Bag Go Down 2",
            "Coarse Intake",
            "Fine Intake",
            "Silo",
            "Coarse Grinding 1",
            "Coarse Grinding 2",
            "Coarse Grinding 3",
        ],
        "Pemakaian": [1200, 1520, 729, 2011, 978, 672, 1102, 562],
    }

    df_section = pd.DataFrame(data_section)

    fig = px.pie(
        df_section,
        values="Pemakaian",
        names="Section",
        title=f"% Pemakaian Motor Feed Mill {current_date}",
        hole=0.0,
    )
    st.plotly_chart(fig)

with usage_middle:
    motor_rbd = {
        "Section": ["RBD 1", "RBD 2", "FH", "Liquid Pump", "Pellet RBD"],
        "Pemakaian": np.random.randint(500, 5000, 5),
    }

    df_motor_rbd = pd.DataFrame(motor_rbd)

    fig = px.pie(
        df_motor_rbd,
        values="Pemakaian",
        names="Section",
        title=f"% Pemakaian Motor RBD & Aqua {current_date}",
        hole=0.0,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig)

with usage_right:
    data_mesin = {
        "Machine Type": ["Blowers", "Conveyors", "Compressors", "Others"],
        "Consumption Mei 2025": [42000, 30000, 19000, 10000],
    }
    df_mesin = pd.DataFrame(data_mesin)

    # Create Plotly pie chart
    fig = px.pie(
        df_mesin,
        values="Consumption Mei 2025",
        names="Machine Type",
        title=f"% Pemakaian per Tipe Mesin {current_date}",
        hole=0.0,
        color_discrete_sequence=px.colors.qualitative.Vivid,
    )  # Optional: create a donut chart by setting hole

    # Display the chart in Streamlit
    st.plotly_chart(fig)  # use_container_width makes the chart responsive


#####---------- Perubahan Pemakaian ----------#####
st.markdown('<div class="sub-header">Perubahan Pemakaian</div>', unsafe_allow_html=True)

usage_delta_left, usage_delta_middle, usage_delta_right = st.columns(
    3, vertical_alignment="center"
)

with usage_delta_left:
    datadd = {
        "Bulan": ["Mei 2025", "Juni 2025"],
        "Pemakaian": [103027, 163027],
    }
    dfdd = pd.DataFrame(datadd)

    # Create the Plotly figure
    fig = px.bar(
        dfdd,
        x="Bulan",
        y="Pemakaian",
        title="Perubahan Pemakaian",
        # labels={"Category": "Food Group", "Quantity": "Amount in Stock"},
        color="Bulan",
        height=300,
        labels={"Pemakaian": "Pemakaian (kWh)"},
    )  # Color bars by category

    # Display the chart in Streamlit
    st.plotly_chart(fig)

with usage_delta_middle:
    st.metric(
        label="Pemakaian Bulanan Total (kWh)",
        value=163027,
        delta=163027 - 103027,
        border=True,
    )
    style_metric_cards(border_left_color="#003366")

with usage_delta_right:
    st.metric(
        label="Pemakaian Harian Total (kWh)",
        value="5230",
        delta="-0.5k",
        border=True,
    )
    style_metric_cards(border_left_color="#003366")

#####---------- Perubahan Biaya ----------#####
st.markdown('<div class="sub-header">Perubahan Biaya</div>', unsafe_allow_html=True)

cost_left, cost_right = st.columns([1, 2])

with cost_left:
    datadd = {
        "Bulan": ["Mei 2025", "Juni 2025"],
        "Biaya": [151877321, 234877321],
    }
    dfdd = pd.DataFrame(datadd)

    # Create the Plotly figure
    fig = px.bar(
        dfdd,
        x="Bulan",
        y="Biaya",
        title="Perubahan Biaya Total per Bulan",
        # labels={"Category": "Food Group", "Quantity": "Amount in Stock"},
        color="Bulan",
        color_discrete_map={"Mei 2025": "#117a65", "Juni 2025": "#73c6b6"},
        # color=["#117a65", "#73c6b6"],
        height=400,
        labels={"Biaya": "Biaya Rp"},
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

with cost_right:
    data_mesin = {
        "Tipe_Mesin": ["Blowers", "Conveyors", "Compressors", "Others"],
        "Biaya_Mei_2025": [512087, 331000, 227980, 122000],
        "Biaya_Juni_2025": [720000, 580121, 425908, 123000],
    }
    df_mesin = pd.DataFrame(data_mesin)

    fig = px.bar(
        df_mesin,
        x="Tipe_Mesin",
        y=["Biaya_Mei_2025", "Biaya_Juni_2025"],
        title="Perubahan Biaya per Mesin per Bulan",
        # labels={"Category": "Food Group", "Quantity": "Amount in Stock"},
        # color="Machine Type",
        color_discrete_map={"Biaya_Mei_2025": "#a93226", "Biaya_Juni_2025": "#e6b0aa"},
        # color=["#117a65", "#73c6b6"],
        barmode="group",
        height=400,
        labels={"value": "Biaya Rp", "variable": "Bulan", "Tipe_Mesin": "Tipe Mesin"},
    )
    st.plotly_chart(fig)

##############################

# st.subheader("Jumlah Mesin", anchor=False)
st.markdown('<div class="sub-header">Jumlah Mesin</div>', unsafe_allow_html=True)

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

##############################

# st.subheader("Konsumsi Listrik", anchor=False)
# st.write(
#     """
#     Konsumsi harian listrik real-time yang dibandingkan dengan konsumsi hari sebelumnya pada saat yang sama.
#     """
# )

# col21, col22, col23 = st.columns((3))

# with col21:
#     st.metric(label="Konsumsi Harian - Motor (kWh)", value="23.9k", delta="-1.2k")
#     style_metric_cards(border_left_color="#003366")


# with col22:
#     st.metric(label="Konsumsi Harian - Kompresor (kWh)", value="46.1k", delta="4.5k")
#     style_metric_cards(border_left_color="#003366")

# with col23:
#     st.metric(
#         label="Konsumsi Harian Total (kWh/month)",
#         value="50",
#         delta="-0.5k",
#         border=True,
#     )
#     style_metric_cards(border_left_color="#003366")

# st.markdown("---")

# st.divider()

st.markdown('<div class="sub-header">Plot Pemakaian</div>', unsafe_allow_html=True)

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
