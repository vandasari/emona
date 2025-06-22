# import time
# import psutil
# import streamlit as st


# # Function to get the memory usage.
# def memory_usage():
#     return psutil.virtual_memory().percent


# # Assigning Streamlit metric to a variable.
# memory_data = st.metric(label="Live Memory Data", value=memory_usage())

# # Updating the data
# while True:
#     time.sleep(1)
#     memory_data.metric(label="Live Memory Data", value=memory_usage())


#############

import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

# # Configure page layout
# st.set_page_config(
#     page_title="Power Utility Monitoring Dashboard",
#     page_icon="⚡",
#     layout="wide"
# )

# Custom CSS for better appearance
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
        margin-top: -2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0D47A1;
        margin-top: 1rem;
    }
    .stContainer, .stColumn {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.07);
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
</style>
""",
    unsafe_allow_html=True,
)

# Title and intro
st.markdown(
    '<div class="main-header">Power Utility Monitoring Reports</div>',
    unsafe_allow_html=True,
)
st.markdown("Monitor electricity consumption, costs, and analysis in real-time")


# Generate sample data for demonstration
@st.cache_data
def generate_sample_data():
    # Generate dates for the last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    date_range = pd.date_range(start=start_date, end=end_date, freq="h")

    # Create dataframe with hourly data
    df = pd.DataFrame(
        {
            "timestamp": date_range,
            "consumption_kwh": np.random.normal(
                loc=2.1, scale=1.2, size=len(date_range)
            )
            * (1 + 0.3 * np.sin(np.pi * date_range.hour / 12))  # Daily pattern
            * (
                1 + 0.2 * np.sin(np.pi * date_range.dayofyear / 182.5)
            ),  # Seasonal pattern
            "voltage": np.random.normal(loc=230, scale=3, size=len(date_range)),
            "current": np.random.normal(loc=10, scale=3, size=len(date_range)),
            "power_factor": np.random.normal(
                loc=0.92, scale=0.03, size=len(date_range)
            ).clip(0.8, 1.0),
        }
    )

    # Ensure consumption is positive
    df["consumption_kwh"] = df["consumption_kwh"].clip(0.1, None)

    # Add price per kWh with seasonal variations
    df["price_per_kwh"] = 0.15 + 0.05 * np.sin(
        np.pi * df["timestamp"].dt.dayofyear / 182.5
    )

    # Calculate costs
    df["cost"] = df["consumption_kwh"] * df["price_per_kwh"]

    # Add some random peaks for anomaly detection
    random_peaks = np.random.choice(df.index, size=int(len(df) * 0.001), replace=False)
    df.loc[random_peaks, "consumption_kwh"] *= np.random.uniform(
        1.5, 3.0, size=len(random_peaks)
    )
    df.loc[random_peaks, "cost"] = (
        df.loc[random_peaks, "consumption_kwh"] * df.loc[random_peaks, "price_per_kwh"]
    )

    # Add appliance-specific data (simulated)
    appliances = [
        "HVAC",
        "Lighting",
        "Kitchen",
        "Electronics",
        "Water Heating",
        "Other",
    ]

    # For each appliance, create a distribution of consumption
    appliance_data = {}
    for app in appliances:
        base_consumption = np.random.uniform(0.1, 0.3)
        appliance_data[app] = (
            df["consumption_kwh"]
            * base_consumption
            * np.random.uniform(0.8, 1.2, size=len(df))
        )

    # Combine appliance data into one dataframe
    appliance_df = pd.DataFrame(appliance_data)

    # Normalize to make sure the sum equals the total consumption
    row_sums = appliance_df.sum(axis=1)
    for app in appliances:
        appliance_df[app] = appliance_df[app] / row_sums * df["consumption_kwh"]

    return df, appliance_df


# Load data
df, appliance_df = generate_sample_data()

# Create sidebar
st.sidebar.header("Dashboard Controls")

# Date range selection
date_range_option = st.sidebar.selectbox(
    "Select Date Range",
    [
        "Last 24 Hours",
        "Last 7 Days",
        "Last 30 Days",
        "Last 90 Days",
        "Last 365 Days",
        "Custom",
    ],
)

if date_range_option == "Custom":
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date")
    mask = (df["timestamp"].dt.date >= start_date) & (
        df["timestamp"].dt.date <= end_date
    )
else:
    end_date = df["timestamp"].max()
    if date_range_option == "Last 24 Hours":
        start_date = end_date - timedelta(hours=24)
    elif date_range_option == "Last 7 Days":
        start_date = end_date - timedelta(days=7)
    elif date_range_option == "Last 30 Days":
        start_date = end_date - timedelta(days=30)
    elif date_range_option == "Last 90 Days":
        start_date = end_date - timedelta(days=90)
    else:  # Last 365 Days
        start_date = end_date - timedelta(days=365)
    mask = (df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)

# Filter data based on date range
filtered_df = df.loc[mask].copy()
filtered_appliance_df = appliance_df.loc[mask].copy()

# Ensure all appliance columns exist after filtering
appliances = ["HVAC", "Lighting", "Kitchen", "Electronics", "Water Heating", "Other"]
for app in appliances:
    if app not in filtered_appliance_df.columns:
        filtered_appliance_df[app] = 0.0
filtered_appliance_df = filtered_appliance_df[appliances]

# Add date information for aggregations
filtered_df["date"] = filtered_df["timestamp"].dt.date
filtered_df["hour"] = filtered_df["timestamp"].dt.hour
filtered_df["day_of_week"] = filtered_df["timestamp"].dt.dayofweek
filtered_df["month"] = filtered_df["timestamp"].dt.month
filtered_df["year"] = filtered_df["timestamp"].dt.year

# Sidebar for aggregation level
aggregation = st.sidebar.selectbox(
    "Data Aggregation Level", ["Hourly", "Daily", "Weekly", "Monthly"]
)

# Sidebar for comparing periods
compare_periods = st.sidebar.checkbox("Compare with Previous Period")

# Comparison logic
if compare_periods:
    delta_days = (filtered_df["timestamp"].max() - filtered_df["timestamp"].min()).days
    previous_end = filtered_df["timestamp"].min() - timedelta(hours=1)
    previous_start = previous_end - timedelta(days=delta_days)
    previous_mask = (df["timestamp"] >= previous_start) & (
        df["timestamp"] <= previous_end
    )
    previous_df = df.loc[previous_mask].copy()

    # Add date information for previous period
    previous_df["date"] = previous_df["timestamp"].dt.date
    previous_df["hour"] = previous_df["timestamp"].dt.hour
    previous_df["day_of_week"] = previous_df["timestamp"].dt.dayofweek
    previous_df["month"] = previous_df["timestamp"].dt.month
    previous_df["year"] = previous_df["timestamp"].dt.year
else:
    previous_df = None

# Create tabs for different dashboard sections
tab1, tab2, tab3, tab4 = st.tabs(
    ["Overview", "Consumption Analysis", "Cost Analysis", "Appliance Breakdown"]
)


# Aggregate data based on selected aggregation level
def aggregate_data(df, agg_level):
    if agg_level == "Hourly":
        return df.set_index("timestamp").resample("h").mean(numeric_only=True)
    elif agg_level == "Daily":
        return df.set_index("timestamp").resample("D").mean(numeric_only=True)
    elif agg_level == "Weekly":
        return df.set_index("timestamp").resample("W").mean(numeric_only=True)
    else:  # Monthly
        return df.set_index("timestamp").resample("M").mean(numeric_only=True)


agg_df = aggregate_data(filtered_df, aggregation)
agg_cost = aggregate_data(filtered_df[["timestamp", "cost"]], aggregation)
agg_consumption = aggregate_data(
    filtered_df[["timestamp", "consumption_kwh"]], aggregation
)
agg_appliance = aggregate_data(
    pd.concat([filtered_df[["timestamp"]], filtered_appliance_df], axis=1), aggregation
)

# Calculate KPIs
total_consumption = filtered_df["consumption_kwh"].sum()
total_cost = filtered_df["cost"].sum()
avg_price = filtered_df["price_per_kwh"].mean()
peak_consumption = filtered_df.groupby("date")["consumption_kwh"].sum().max()
peak_date = filtered_df.groupby("date")["consumption_kwh"].sum().idxmax()

# Calculate comparisons if requested
if compare_periods:
    prev_total_consumption = previous_df["consumption_kwh"].sum()
    prev_total_cost = previous_df["cost"].sum()
    prev_avg_price = previous_df["price_per_kwh"].mean()

    consumption_change = (
        (total_consumption - prev_total_consumption) / prev_total_consumption * 100
    )
    cost_change = (total_cost - prev_total_cost) / prev_total_cost * 100
    price_change = (avg_price - prev_avg_price) / prev_avg_price * 100

# TAB 1: OVERVIEW
with tab1:
    st.markdown('<div class="sub-header">Key Metrics</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container():
            st.metric(
                "Total Consumption",
                f"{total_consumption:.2f} kWh",
                f"{consumption_change:.1f}%" if compare_periods else None,
                delta_color=(
                    "inverse"
                    if compare_periods and consumption_change > 0
                    else "normal"
                ),
            )
    with col2:
        with st.container():
            st.metric(
                "Total Cost",
                f"${total_cost:.2f}",
                f"{cost_change:.1f}%" if compare_periods else None,
                delta_color=(
                    "inverse" if compare_periods and cost_change > 0 else "normal"
                ),
            )
    with col3:
        with st.container():
            st.metric(
                "Average Price",
                f"${avg_price:.4f}/kWh",
                f"{price_change:.1f}%" if compare_periods else None,
                delta_color=(
                    "inverse" if compare_periods and price_change > 0 else "normal"
                ),
            )
    with col4:
        with st.container():
            st.metric(
                "Peak Daily Consumption",
                f"{peak_consumption:.2f} kWh",
                f"on {peak_date}",
            )

    st.markdown(
        '<div class="sub-header">Consumption Over Time</div>', unsafe_allow_html=True
    )
    with st.container():
        fig = px.line(
            agg_consumption.reset_index(),
            x="timestamp",
            y="consumption_kwh",
            title=f"{aggregation} Consumption",
            labels={"timestamp": "Time", "consumption_kwh": "Consumption (kWh)"},
            line_shape="spline",
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sub-header">Cost Over Time</div>', unsafe_allow_html=True)
    with st.container():
        fig = px.line(
            agg_cost.reset_index(),
            x="timestamp",
            y="cost",
            title=f"{aggregation} Cost",
            labels={"timestamp": "Time", "cost": "Cost ($)"},
            line_shape="spline",
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: CONSUMPTION ANALYSIS
with tab2:
    st.markdown(
        '<div class="sub-header">Consumption Patterns</div>', unsafe_allow_html=True
    )

    # Hourly consumption pattern
    hourly_avg = filtered_df.groupby("hour")["consumption_kwh"].mean().reset_index()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            hourly_avg,
            x="hour",
            y="consumption_kwh",
            title="Average Hourly Consumption",
            labels={"hour": "Hour of Day", "consumption_kwh": "Avg. Consumption (kWh)"},
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Daily consumption pattern
    daily_avg = (
        filtered_df.groupby("day_of_week")["consumption_kwh"].mean().reset_index()
    )
    daily_avg["day_name"] = daily_avg["day_of_week"].apply(
        lambda x: calendar.day_name[x]
    )

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            daily_avg,
            x="day_name",
            y="consumption_kwh",
            title="Average Daily Consumption",
            labels={
                "day_name": "Day of Week",
                "consumption_kwh": "Avg. Consumption (kWh)",
            },
            category_orders={"day_name": [calendar.day_name[i] for i in range(7)]},
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Monthly consumption pattern
    if (
        filtered_df["timestamp"].max() - filtered_df["timestamp"].min()
    ).days >= 60:  # Only show if enough data
        monthly_avg = (
            filtered_df.groupby("month")["consumption_kwh"].mean().reset_index()
        )
        monthly_avg["month_name"] = monthly_avg["month"].apply(
            lambda x: calendar.month_name[x]
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            monthly_avg,
            x="month_name",
            y="consumption_kwh",
            title="Average Monthly Consumption",
            labels={"month_name": "Month", "consumption_kwh": "Avg. Consumption (kWh)"},
            category_orders={
                "month_name": [calendar.month_name[i] for i in range(1, 13)]
            },
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Heatmap - Day vs Hour
    st.markdown(
        '<div class="sub-header">Consumption Heatmap</div>', unsafe_allow_html=True
    )
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Create day-hour heatmap
    pivot_df = filtered_df.pivot_table(
        index="day_of_week", columns="hour", values="consumption_kwh", aggfunc="mean"
    )
    # Dynamically generate y and x labels based on pivot_df shape
    y_labels = [calendar.day_name[i] for i in pivot_df.index]  # Only those present
    x_labels = [str(i) for i in pivot_df.columns]
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Hour of Day", y="Day of Week", color="Avg. Consumption (kWh)"),
        x=x_labels,
        y=y_labels,
        title="Consumption Heatmap - Day vs Hour",
        color_continuous_scale="Viridis",
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Anomaly detection
    st.markdown(
        '<div class="sub-header">Anomaly Detection</div>', unsafe_allow_html=True
    )

    # Define anomalies as points more than 3 standard deviations from the mean
    rolling_mean = filtered_df["consumption_kwh"].rolling(window=24).mean()
    rolling_std = filtered_df["consumption_kwh"].rolling(window=24).std()

    filtered_df["upper_bound"] = rolling_mean + 3 * rolling_std
    filtered_df["lower_bound"] = (rolling_mean - 3 * rolling_std).clip(0)

    # Identify anomalies
    filtered_df["anomaly"] = (
        filtered_df["consumption_kwh"] > filtered_df["upper_bound"]
    ) | (filtered_df["consumption_kwh"] < filtered_df["lower_bound"])

    anomalies = filtered_df[filtered_df["anomaly"]]

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = go.Figure()

    # Add consumption line
    fig.add_trace(
        go.Scatter(
            x=filtered_df["timestamp"],
            y=filtered_df["consumption_kwh"],
            name="Consumption",
            line=dict(color="blue", width=1),
        )
    )

    # Add upper bound
    fig.add_trace(
        go.Scatter(
            x=filtered_df["timestamp"],
            y=filtered_df["upper_bound"],
            name="Upper Bound",
            line=dict(color="red", width=1, dash="dash"),
            opacity=0.5,
        )
    )

    # Add lower bound
    fig.add_trace(
        go.Scatter(
            x=filtered_df["timestamp"],
            y=filtered_df["lower_bound"],
            name="Lower Bound",
            line=dict(color="red", width=1, dash="dash"),
            opacity=0.5,
        )
    )

    # Add anomalies
    if not anomalies.empty:
        fig.add_trace(
            go.Scatter(
                x=anomalies["timestamp"],
                y=anomalies["consumption_kwh"],
                mode="markers",
                name="Anomalies",
                marker=dict(color="red", size=10),
            )
        )

    fig.update_layout(
        title="Consumption Anomalies",
        xaxis_title="Time",
        yaxis_title="Consumption (kWh)",
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Display anomaly table if anomalies exist
    if not anomalies.empty:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.write(f"Found {len(anomalies)} anomalies in the selected period:")
        anomaly_table = anomalies[
            ["timestamp", "consumption_kwh", "upper_bound", "lower_bound"]
        ].copy()
        anomaly_table.columns = [
            "Timestamp",
            "Consumption (kWh)",
            "Upper Bound",
            "Lower Bound",
        ]
        st.dataframe(anomaly_table, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No anomalies detected in the selected time period.")

# TAB 3: COST ANALYSIS
with tab3:
    st.markdown('<div class="sub-header">Cost Breakdown</div>', unsafe_allow_html=True)

    # Daily cost breakdown
    daily_cost = (
        filtered_df.groupby("date")[["cost", "consumption_kwh"]].sum().reset_index()
    )
    daily_cost["unit_cost"] = daily_cost["cost"] / daily_cost["consumption_kwh"]

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.bar(
        daily_cost,
        x="date",
        y="cost",
        title="Daily Cost Breakdown",
        labels={"date": "Date", "cost": "Cost ($)"},
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Price variation
    st.markdown('<div class="sub-header">Price Variation</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Price trend
        daily_price = filtered_df.groupby("date")["price_per_kwh"].mean().reset_index()

        fig = px.line(
            daily_price,
            x="date",
            y="price_per_kwh",
            title="Price Trend",
            labels={"date": "Date", "price_per_kwh": "Price per kWh ($)"},
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        # Unit cost vs consumption
        fig = px.scatter(
            daily_cost,
            x="consumption_kwh",
            y="unit_cost",
            title="Unit Cost vs. Consumption",
            labels={
                "consumption_kwh": "Daily Consumption (kWh)",
                "unit_cost": "Unit Cost ($/kWh)",
            },
            trendline="ols",
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Cost projections
    st.markdown(
        '<div class="sub-header">Cost Projections</div>', unsafe_allow_html=True
    )

    # Calculate daily average consumption and cost
    avg_daily_consumption = filtered_df.groupby("date")["consumption_kwh"].sum().mean()
    avg_daily_cost = filtered_df.groupby("date")["cost"].sum().mean()

    # Projected costs
    time_periods = ["Next 7 Days", "Next 30 Days", "Next 90 Days", "Next 365 Days"]
    days = [7, 30, 90, 365]
    projections = [avg_daily_cost * day for day in days]

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    projection_df = pd.DataFrame(
        {"Period": time_periods, "Projected Cost": projections}
    )

    fig = px.bar(
        projection_df,
        x="Period",
        y="Projected Cost",
        title="Cost Projections",
        labels={"Period": "Time Period", "Projected Cost": "Projected Cost ($)"},
        text_auto=".2f",
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Cost optimization suggestions
    st.markdown(
        '<div class="sub-header">Cost Optimization Suggestions</div>',
        unsafe_allow_html=True,
    )

    # Find peak consumption hours
    peak_hours = (
        filtered_df.groupby("hour")["consumption_kwh"].mean().nlargest(5).index.tolist()
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.write("Cost Saving Opportunities:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        ### Peak Usage Hours
        Consider reducing usage during these hours:
        - {', '.join([f"{hour}:00" for hour in peak_hours])}
        
        ### Estimated Annual Savings
        - 10% reduction during peak hours: **${(avg_daily_cost * 365 * 0.1):.2f}**
        - 20% reduction during peak hours: **${(avg_daily_cost * 365 * 0.2):.2f}**
        """
        )

    with col2:
        st.markdown(
            f"""
        ### Energy Efficiency Improvements
        - LED Lighting: **${(avg_daily_cost * 365 * 0.05):.2f}** annually
        - Smart Thermostat: **${(avg_daily_cost * 365 * 0.08):.2f}** annually
        - Energy Star Appliances: **${(avg_daily_cost * 365 * 0.12):.2f}** annually
        - Insulation Improvements: **${(avg_daily_cost * 365 * 0.15):.2f}** annually
        """
        )

    st.markdown("</div>", unsafe_allow_html=True)

# TAB 4: APPLIANCE BREAKDOWN
with tab4:
    st.markdown(
        '<div class="sub-header">Appliance Consumption</div>', unsafe_allow_html=True
    )

    # Total consumption by appliance
    appliance_totals = filtered_appliance_df.sum().reset_index()
    appliance_totals.columns = ["Appliance", "Consumption (kWh)"]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.pie(
            appliance_totals,
            values="Consumption (kWh)",
            names="Appliance",
            title="Total Consumption by Appliance",
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig = px.bar(
            appliance_totals,
            x="Appliance",
            y="Consumption (kWh)",
            title="Appliance Consumption Breakdown",
            labels={"Appliance": "Appliance", "Consumption (kWh)": "Consumption (kWh)"},
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Appliance consumption over time
    st.markdown(
        '<div class="sub-header">Appliance Consumption Over Time</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    # Resample to daily for better visualization
    daily_appliance = (
        filtered_appliance_df.groupby(filtered_df["date"]).sum().reset_index()
    )

    # Create figure
    fig = go.Figure()

    # Add traces for each appliance
    for appliance in filtered_appliance_df.columns:
        fig.add_trace(
            go.Scatter(
                x=daily_appliance["date"],
                y=daily_appliance[appliance],
                name=appliance,
                stackgroup="one",
            )
        )

    fig.update_layout(
        title="Daily Appliance Consumption",
        xaxis_title="Date",
        yaxis_title="Consumption (kWh)",
        height=450,
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Appliance usage patterns
    st.markdown(
        '<div class="sub-header">Appliance Usage Patterns</div>', unsafe_allow_html=True
    )

    # Hourly usage patterns
    appliance_hourly = pd.DataFrame()
    for appliance in filtered_appliance_df.columns:
        # Create a temporary dataframe with hour and appliance data
        temp_df = pd.DataFrame(
            {
                "hour": filtered_df["hour"],
                "appliance_value": filtered_appliance_df[appliance],
            }
        )
        hourly_data = temp_df.groupby("hour")["appliance_value"].mean().reset_index()
        hourly_data["Appliance"] = appliance
        appliance_hourly = pd.concat([appliance_hourly, hourly_data])

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig = px.line(
        appliance_hourly,
        x="hour",
        y="appliance_value",
        color="Appliance",
        title="Hourly Appliance Usage Patterns",
        labels={"hour": "Hour of Day", "appliance_value": "Avg. Consumption (kWh)"},
    )
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Recommendations for appliance optimization
    st.markdown(
        '<div class="sub-header">Appliance Optimization Recommendations</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    # Sort appliances by total consumption
    top_appliances = appliance_totals.sort_values("Consumption (kWh)", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
        ### Top Energy Users
        1. **{top_appliances.iloc[0]['Appliance']}**: {top_appliances.iloc[0]['Consumption (kWh)']:.2f} kWh
        2. **{top_appliances.iloc[1]['Appliance']}**: {top_appliances.iloc[1]['Consumption (kWh)']:.2f} kWh
        3. **{top_appliances.iloc[2]['Appliance']}**: {top_appliances.iloc[2]['Consumption (kWh)']:.2f} kWh
        
        ### Optimization Tips
        - **HVAC**: Program your thermostat to adjust when you're away or sleeping
        - **Lighting**: Switch to LED bulbs and use motion sensors
        - **Water Heating**: Lower temperature and insulate the tank
        """
        )

    with col2:
        st.markdown(
            """
        ### Potential Annual Savings
        - Smart power strips for electronics: $75-150
        - Refrigerator/freezer maintenance: $50-100
        - HVAC regular maintenance: $120-250
        - Replace old appliances: $200-500
        
        ### Low-Hanging Fruit
        - Unplug devices when not in use
        - Use cold water for laundry when possible
        - Clean refrigerator coils and HVAC filters
        """
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # Appliance-specific recommendations
    st.markdown(
        '<div class="sub-header">Detailed Appliance Recommendations</div>',
        unsafe_allow_html=True,
    )

    # Create expandable sections for each appliance
    appliance_recommendations = {
        "HVAC": {
            "tips": [
                "Install a programmable thermostat and set it to adjust automatically",
                "Set your thermostat to 68°F (20°C) in winter and 78°F (26°C) in summer",
                "Clean or replace air filters regularly (every 1-3 months)",
                "Consider a home energy audit to check for air leaks and insulation issues",
                "Use ceiling fans to supplement air conditioning",
            ],
            "potential_savings": "10-15% on heating/cooling costs",
        },
        "Lighting": {
            "tips": [
                "Replace all incandescent bulbs with LEDs",
                "Install dimmer switches and motion sensors",
                "Maximize natural light during the day",
                "Turn off lights when not in use",
                "Consider smart lighting systems for automated control",
            ],
            "potential_savings": "5-10% on electricity bill",
        },
        "Kitchen": {
            "tips": [
                "Run dishwasher only when full and use eco settings",
                "Keep refrigerator coils clean and check door seals",
                "Use microwave or toaster oven instead of full-size oven when possible",
                "Defrost freezer regularly to maintain efficiency",
                "Cover pots when cooking to reduce cooking time",
            ],
            "potential_savings": "5-8% on electricity bill",
        },
        "Electronics": {
            "tips": [
                "Use advanced power strips to eliminate phantom power draw",
                "Enable power management features on computers and TVs",
                "Unplug chargers when not in use",
                "Consider ENERGY STAR certified electronics for replacements",
                "Turn off gaming consoles completely when not in use",
            ],
            "potential_savings": "2-5% on electricity bill",
        },
        "Water Heating": {
            "tips": [
                "Lower water heater temperature to 120°F (49°C)",
                "Insulate hot water pipes and the water heater tank",
                "Install low-flow showerheads and faucet aerators",
                "Take shorter showers and fix leaky faucets",
                "Consider a heat pump water heater for significant savings",
            ],
            "potential_savings": "7-12% on energy costs",
        },
    }

    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    for appliance, info in appliance_recommendations.items():
        with st.expander(f"{appliance} Recommendations"):
            st.markdown(f"### {appliance} Tips")
            for tip in info["tips"]:
                st.markdown(f"- {tip}")
            st.markdown(f"**Potential Savings**: {info['potential_savings']}")

    st.markdown("</div>", unsafe_allow_html=True)

# Add data download section
st.sidebar.markdown("---")
st.sidebar.markdown("### Export Data")


# Prepare data for download
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")


# Create download options
download_format = st.sidebar.selectbox("Select Format", ["CSV", "Excel"])

download_timeframe = st.sidebar.selectbox(
    "Select Timeframe", ["Current Selection", "All Data"]
)

if download_timeframe == "Current Selection":
    download_df = filtered_df
else:
    download_df = df

# Create download buttons
if download_format == "CSV":
    csv = convert_df_to_csv(download_df)
    st.sidebar.download_button(
        label="Download Data",
        data=csv,
        file_name="power_utility_data.csv",
        mime="text/csv",
    )
else:
    # For Excel format, we'll use a simple approach without actually creating Excel files
    st.sidebar.info("Excel download would be implemented here in a production app.")

# Add footer
st.markdown("---")
st.markdown("Power Utility Monitoring Dashboard • Created with Streamlit")
st.markdown("© 2025 • For demonstration purposes only")

# Add about section
with st.sidebar.expander("About Dashboard"):
    st.write(
        """
    This Power Utility Monitoring Dashboard provides comprehensive analytics and insights into electricity consumption and costs.
    
    **Features:**
    - Real-time monitoring of electricity usage
    - Cost analysis and projections
    - Consumption patterns and anomaly detection
    - Appliance-level energy breakdown
    - Optimization recommendations
    
    Data is refreshed hourly. For technical support or questions, please contact support@example.com
    """
    )

# Add settings
with st.sidebar.expander("Settings"):
    st.checkbox("Dark Mode (Premium Feature)", disabled=True)
    st.checkbox("Enable Notifications", value=False)
    st.checkbox("Auto-refresh Data", value=True, key="auto_refresh")
    if st.session_state.get("auto_refresh", True):
        import time

        st.experimental_rerun_interval = 60  # rerun every 60 seconds
    st.slider("Chart Animation Speed", min_value=0, max_value=10, value=5)
