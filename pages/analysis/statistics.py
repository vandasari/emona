import streamlit as st
import pandas as pd
import plotly.express as px


st.header("Statistics")

data = pd.read_csv("data/powerconsumption.csv")

st.subheader("Berdasarkan Pilihan Hari")

##--- Convert Datetime column to just date
data["Date"] = pd.to_datetime(data["Datetime"]).dt.date

day_list = list(data["Date"].unique())[::-1]

col1, col2 = st.columns(2)

with col1:
    selected_day = st.selectbox("Pilih hari", day_list, index=len(day_list) - 1)

with col2:
    selected_zone = st.selectbox("Pilih Zona", ["Zona 1", "Zona 2", "Zona 3"])


##--- All data in the selected day
df_selected_day = data[data["Date"] == selected_day]

if selected_zone == "Zona 1":
    power_consumption_per_zone = df_selected_day["PowerConsumption_Zone1"]
elif selected_zone == "Zona 2":
    power_consumption_per_zone = df_selected_day["PowerConsumption_Zone2"]
else:
    power_consumption_per_zone = df_selected_day["PowerConsumption_Zone3"]

tot_power_consumption_per_zone = power_consumption_per_zone.sum()


time_day = df_selected_day["Datetime"]
# zone1_power_consumption = df_selected_day["PowerConsumption_Zone1"]
cost_per_zone = 1444.70 * tot_power_consumption_per_zone


st.write(df_selected_day)

st.write("\n")

title = f"{selected_day.year}-{selected_day.month}-{selected_day.day}"

st.subheader(f"Konsumsi Listrik dan biaya untuk {selected_zone} periode {title}")

col3, col4 = st.columns([2, 3], border=True)

with col3:
    st.metric(
        label="Total Konsumsi",
        value=f"{tot_power_consumption_per_zone/1000:.2f} kW",
        delta=-2.5,
    )

with col4:
    bar_chart_zone1 = px.bar(x=time_day, y=power_consumption_per_zone, height=250)
    st.plotly_chart(bar_chart_zone1)


col5, col6 = st.columns([2, 3], border=True)

with col5:
    st.metric(label="Total Biaya", value=f"Rp {cost_per_zone:.2f}")


st.subheader(
    f"Pengaruh Suhu, Kelembaban, dan Kecepatan Angin untuk {selected_zone} periode {title}"
)

col_temp, col_pow_temp = st.columns(2, border=True)

temperature = df_selected_day["Temperature"]
humidity = df_selected_day["Humidity"]
windspeed = df_selected_day["WindSpeed"]

with col_temp:
    scatter_temp_in_a_day = px.scatter(
        x=time_day, y=temperature, title=f"Suhu pada {title}"
    )
    st.plotly_chart(scatter_temp_in_a_day, use_container_width=True)

with col_pow_temp:
    scatter_pow_vs_temp = px.scatter(
        x=temperature,
        y=power_consumption_per_zone,
        title="Suhu vs konsumsi listrik",
    )
    st.plotly_chart(scatter_pow_vs_temp, use_container_width=True)

st.divider()

col_hum, col_pow_hum = st.columns(2, border=True)

with col_hum:
    scatter_hum_in_a_day = px.scatter(
        x=time_day, y=humidity, title=f"Kelembaban pada {title}"
    )
    st.plotly_chart(scatter_hum_in_a_day, use_container_width=True)

with col_pow_hum:
    scatter_hum_vs_pow = px.scatter(
        x=humidity, y=power_consumption_per_zone, title="Kelembaban vs konsumsi listrik"
    )
    st.plotly_chart(scatter_hum_vs_pow, use_container_width=True)

st.divider()

col_wind, col_pow_wind = st.columns(2, border=True)

with col_wind:
    scatter_wind_in_a_day = px.scatter(
        x=time_day, y=windspeed, title=f"Kecepatan angin pada {title}"
    )
    st.plotly_chart(scatter_wind_in_a_day, use_container_width=True)

with col_pow_wind:
    scatter_wind_vs_pow = px.scatter(
        x=windspeed,
        y=power_consumption_per_zone,
        title="Kecepatan angin vs konsumsi listrik",
    )
    st.plotly_chart(scatter_wind_vs_pow, use_container_width=True)
