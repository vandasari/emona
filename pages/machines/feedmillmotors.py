import streamlit as st
import streamviz
import numpy as np
import time


def plot_gauge(
    indicator_value,
    title,
    lower_indicator=1650,
    middle_indicator=3300,
    highest_indicator=5000,
    size="SML",
    mode="gauge+number",
):
    streamviz.gauge(
        indicator_value,
        gTitle=title,
        gSize=size,
        gMode=mode,
        grLow=lower_indicator,
        grMid=middle_indicator,
        arTop=highest_indicator,
        gcLow="#1B8720",
        gcMid="#FF9400",
        gcHigh="#FF1708",
    )


def gauge_description(value, power, amp, cost):
    st.write(f"{value} Watt")
    st.write(f"Power: {power} kW")
    st.write(f"{amp} Amp")
    st.write(f"Rp {cost:.2f}")


st.header("Feed Mill Motors", anchor=False)

st.subheader("SECTION: BAG GO DOWN 1", anchor=False)

value0 = np.random.randint(100, 4900)
value1 = np.random.randint(100, 4900)
value2 = np.random.randint(100, 4900)
value3 = np.random.randint(100, 4900)

value4 = np.random.randint(100, 4900)
value5 = np.random.randint(100, 4900)
value6 = np.random.randint(100, 4900)
value7 = np.random.randint(100, 4900)

total_value1 = value0 + value1 + value2 + value3
per_kwh = 1444.70
total_cost1 = total_value1 * per_kwh

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"##### Total Konsumsi: {total_value1} kW")

with col2:
    st.warning(f"##### Biaya per kWh: Rp {per_kwh}")

with col3:
    if total_cost1 < 20000000:
        st.success(f"##### Total Biaya: Rp {total_cost1:.2f}")
    else:
        st.error(f"##### Total Biaya: Rp {total_cost1:.2f}")

row1 = st.columns(2)
row2 = st.columns(2)

grid = [col.container(height=200) for col in row1 + row2]

with grid[0]:
    left1, right1 = st.columns([4, 2], gap="medium")
    with left1:
        plot_gauge(value0, "BF-111 Blower - Bag Filter")
    with right1:
        gauge_description(value0, 15, 6.4, value0 * per_kwh)

with grid[1]:
    left2, right2 = st.columns([4, 2], gap="medium")
    with left2:
        plot_gauge(value1, "CC-111 Chain Conveyor")
    with right2:
        gauge_description(value1, 15, 19.5, value1 * per_kwh)

with grid[2]:
    left3, right3 = st.columns([4, 2], gap="medium")
    with left3:
        plot_gauge(value2, "BE-112 Bucket Elevator")
    with right3:
        gauge_description(value2, 22, 25, value2 * per_kwh)

with grid[3]:
    left4, right4 = st.columns([4, 2], gap="medium")
    with left4:
        plot_gauge(value3, "DS-113 Drum Sieve")
    with right4:
        gauge_description(value3, 1.5, 2.2, value3 * per_kwh)


st.divider()

st.subheader("SECTION: BAG GO DOWN 2", anchor=False)

value4 = np.random.randint(100, 4900)
value5 = np.random.randint(100, 4900)
value6 = np.random.randint(100, 4900)
value7 = np.random.randint(100, 4900)

total_value2 = value4 + value5 + value6 + value7
per_kwh = 1444.70
total_cost2 = total_value2 * per_kwh

col1, col2, col3 = st.columns(3)

with col1:
    st.info(f"##### Total Konsumsi: {total_value2} kW")

with col2:
    st.warning(f"##### Biaya per kWh: Rp {per_kwh}")

with col3:
    if total_cost2 < 20000000:
        st.success(f"##### Total Biaya: Rp {total_cost2:.2f}")
    else:
        st.error(f"##### Total Biaya: Rp {total_cost2:.2f}")

row1 = st.columns(2)
row2 = st.columns(2)

grid = [col.container(height=200) for col in row1 + row2]

with grid[0]:
    left1, right1 = st.columns([4, 2], gap="medium")
    with left1:
        plot_gauge(value4, "BF-121 Blower - Bag Filter")
    with right1:
        gauge_description(value4, 15, 6.4, value4 * per_kwh)

with grid[1]:
    left2, right2 = st.columns([4, 2], gap="medium")
    with left2:
        plot_gauge(value5, "CC-121 Chain Conveyor")
    with right2:
        gauge_description(value5, 15, 19.5, value5 * per_kwh)

with grid[2]:
    left3, right3 = st.columns([4, 2], gap="medium")
    with left3:
        plot_gauge(value6, "BE-122 Bucket Elevator")
    with right3:
        gauge_description(value6, 22, 25, value6 * per_kwh)

with grid[3]:
    left4, right4 = st.columns([4, 2], gap="medium")
    with left4:
        plot_gauge(value7, "DS-123 Drum Sieve")
    with right4:
        gauge_description(value7, 1.5, 2.2, value7 * per_kwh)

st.divider()

if st.button("STOP", type="primary", use_container_width=True):
    st.stop()

for count in range(1, 20):
    time.sleep(0.95)
    st.rerun()


# col1, col2 = st.columns([2, 3])
# with col1:
#     st.metric(label="Metric 1", value=123)
#     st.caption(
#         "This is some additional information about Metric 1. This is some additional information about Metric 2."
#     )
# with col2:
#     st.metric(label="Metric 2", value=456)
#     st.caption(
#         "This is some additional information about Metric 2. This is some additional information about Metric 2."
#     )

# st.divider()

# left, middle, right = st.columns(3, border=True)

# left.markdown("Lorem ipsum " * 5)
# middle.markdown("Lorem ipsum " * 3)
# right.markdown("Lorem ipsum ")
