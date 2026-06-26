import streamlit as st
import pandas as pd
import numpy as np
import joblib
import datetime
import plotly.graph_objects as go
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Retail-AI Analytics Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)


bg = "#F8FAFC"               
text = "#0F172A"             
sidebar_bg = "#FFFFFF"      
card_bg = "#FFFFFF"          
card_border = "#E2E8F0"      
metric_text = "#0F172A"      
metric_label = "#64748B"     
accent_line = "#2563EB"      
icon_color = "#64748B"       
plotly_template = "plotly_white"

# CSS
st.markdown(f"""
<style>
    /* Main Layout Framework Elements */
    .stApp {{ 
        background-color: {bg}; 
        color: {text}; 
        font-family: 'Inter', -apple-system, sans-serif; 
    }}
    section[data-testid="stSidebar"] {{ 
        background-color: {sidebar_bg} !important; 
        border-right: 1px solid {card_border} !important; 
    }}
    
    /* Branding Hero Section Container Component */
    .hero-container {{ 
        background: linear-gradient(135deg, #1E40AF 0%, #0369A1 50%, #0D9488 100%); 
        padding: 40px; 
        border-radius: 16px; 
        color: #FFFFFF; 
        margin-bottom: 30px; 
        box-shadow: 0 10px 25px -5px rgba(3, 105, 161, 0.15);
    }}
    .hero-container h1 {{ 
        font-weight: 800 !important; 
        letter-spacing: -0.05em; 
        margin: 0 0 8px 0 !important; 
        color: #FFFFFF !important; 
    }}
    .hero-container p {{ 
        font-size: 1.1rem; 
        opacity: 0.95; 
        margin: 0 !important; 
        color: #E0F2FE !important; 
    }}
    
    /* Custom Metric Container Card Modules with Depth Interactivity */
    div[data-testid="metric-container"] {{ 
        background: {card_bg} !important; 
        border: 1px solid {card_border} !important; 
        padding: 24px !important; 
        border-radius: 14px !important; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.02);
        transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease; 
    }}
    div[data-testid="metric-container"]:hover {{ 
        transform: translateY(-4px); 
        border-color: {accent_line} !important; 
        box-shadow: 0 12px 20px -8px rgba(37, 99, 235, 0.12);
    }}
    div[data-testid="metric-container"] label {{ 
        color: {metric_label} !important; 
        font-weight: 600 !important; 
        font-size: 0.85rem !important; 
        text-transform: uppercase !important; 
        letter-spacing: 0.05em !important; 
    }}
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {{ 
        color: {metric_text} !important; 
        font-size: 32px !important; 
        font-weight: 800 !important; 
        letter-spacing: -0.03em !important; 
    }}
    
    /* Universal Component Header Typography Control */
    h1, h2, h3, h4 {{ 
        font-weight: 700 !important; 
        color: {text} !important; 
        letter-spacing: -0.03em; 
    }}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_historical_store_data(store_id):
    """
    Simulates a production database lookup for historical features.
    In a live architecture, this interfaces with Snowflake/SQL store repositories.
    """
    np.random.seed(store_id)
    base_sales = np.random.randint(4500, 8500)
    return {
        "sales_lag_7": float(base_sales + np.random.randint(-400, 400)),
        "sales_lag_30": float(base_sales + np.random.randint(-600, 600)),
        "sales_rolling_7": float(base_sales + np.random.randint(-200, 200)),
        "sales_rolling_30": float(base_sales + np.random.randint(-300, 300)),
        "base_stock": int(base_sales * 1.15)
    }

@st.cache_resource
def load_retail_model():
    """Safely initializes and extracts serialized predictive model binaries."""
    try:
        return joblib.load("retail_model.pkl")
    except:
        return None

model = load_retail_model()


if "calculated_forecast" not in st.session_state:
    st.session_state["calculated_forecast"] = 6850.0
if "target_store_id" not in st.session_state:
    st.session_state["target_store_id"] = 1


with st.sidebar:
    st.markdown(
        f"<div style='text-align:center; padding: 25px 0 15px 0;'>"
        f"<h2 style='margin:0; color:{accent_line}; font-size:28px; font-weight:900;'>RetailAI</h2>"
        f"<p style='margin:0; color:{metric_label}; font-size:13px; font-weight:500;'>Integrated ML Architecture</p>"
        f"</div>", 
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Demand Forecasting", "Pricing Intelligence", "Inventory Planning", "Model Insights"],
        icons=["grid", "graph-up", "cash-stack", "boxes", "bar-chart"],
        default_index=0,
        styles={
            "container": {"padding": "4px!important", "background-color": "transparent"},
            "icon": {"color": icon_color, "font-size": "15px"},
            "nav-link": {"font-size": "14px", "color": metric_label, "text-align": "left", "margin": "6px 0px", "border-radius": "8px", "font-weight": "500", "--hover-color": "#F1F5F9"},
            "nav-link-selected": {"background-color": accent_line, "color": "#FFFFFF", "font-weight": "600"}
        }
    )



#  PAGE 1: DASHBOARD 
if selected == "Dashboard":
    st.markdown("""
    <div class="hero-container">
        <h1>Retail-AI Analytics</h1>
        <p>Enterprise core control plane for automated demand modeling, price elasticity testing, and dynamic warehouse buffer pipelines.</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_db = get_historical_store_data(st.session_state["target_store_id"])
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("System Forecast Baseline", f"{st.session_state['calculated_forecast']:,.0f} Units")
    c2.metric("Pipeline Target Store", f"Node ID {st.session_state['target_store_id']}")
    c3.metric("Lookback 7D Sales Mean", f"{current_db['sales_rolling_7']:,.0f}")
    c4.metric("Recommended Safety Stock", f"{int(st.session_state['calculated_forecast'] * 0.15):,.0f} Units")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.subheader("Core Architecture Pipeline Infrastructure")
    summary1, summary2 = st.columns(2)
    with summary1:
        with st.container(border=True):
            st.markdown("### Demand Forecasting Matrix")
            st.write("Dynamic inference framework ingesting rolling auto-regressive lags and regional macro variations to plot regional consumer sales velocities.")
    with summary2:
        with st.container(border=True):
            st.markdown("### Elastic Price Optimizers")
            st.write("Calculates current cross-elasticity curves utilizing historical trend matrices to maximize marginal cash flow capture points.")

    st.subheader("Business Overview")
    st.write("Machine-learning powered demand forecasting, pricing intelligence and inventory optimization platform.")
    
    st.subheader("Future Enhancements")

    st.write("""
    • Real-time demand forecasting

    • Automated inventory replenishment

    • Dynamic pricing optimization

    • External market data integration

    • Generative AI retail assistant

    • Multi-store forecasting support
    """)
    
#  PAGE 2: DEMAND FORECASTING
elif selected == "Demand Forecasting":
    st.title("Demand Forecasting Deep-Inference Engine")
    st.write("Configure architectural parameters below to execute network model calculations.")
    
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            store = st.number_input("Store Node Index ID", 1, 1115, value=st.session_state["target_store_id"])
            promo = st.selectbox("Active Operational Advertisement Window", [0, 1], format_func=lambda x: "Active Promotion" if x==1 else "No Promotion")
            school = st.selectbox("Academic Holiday Tracking State", [0, 1], format_func=lambda x: "Holiday Window Open" if x==1 else "Standard Operations")
            competition = st.number_input("Nearest Competitor Perimeter Vector (Meters)", 0, 100000, 500)
        with c2:
            month = st.slider("Target Forecast Month Segment", 1, 12, 6)
            week = st.slider("Target Calendar Week Cycle", 1, 52, 25)
            quarter = st.slider("Target Operational Fiscal Quarter", 1, 4, 2)
        
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("Execute Network Prediction Run", use_container_width=True, type="primary")

    if generate_btn:
        st.session_state["target_store_id"] = store
        db_features = get_historical_store_data(store)
        
        if model is None:
            # Algorithmic backup math mapping structure to support environment execution if pkl binary breaks
            base_pred = db_features["sales_rolling_30"] * (1.30 if promo == 1 else 0.95)
            pred = float(base_pred + (month * 15) - (competition * 0.004))
        else:
            sample = pd.DataFrame({
                'Store': [store], 'DayOfWeek': [3], 'Promo': [promo], 'SchoolHoliday': [school],
                'CompetitionDistance': [competition], 'StoreType': [1], 'Assortment': [1],
                'Month': [month], 'Week': [week], 'Quarter': [quarter], 'CompetitionOpen': [60],
                'PromoOpen': [25], 
                'Sales_Lag_7': [db_features["sales_lag_7"]], 
                'Sales_Lag_30': [db_features["sales_lag_30"]],
                'Sales_Rolling_7': [db_features["sales_rolling_7"]], 
                'Sales_Rolling_30': [db_features["sales_rolling_30"]]
            })
            pred = float(model.predict(sample)[0])
        
        st.session_state["calculated_forecast"] = pred
        lower_bound = pred * 0.95
        upper_bound = pred * 1.05

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Model Calculation Boundaries")
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("Predicted Core Volume Output", f"{pred:,.0f} Units")
        mc2.metric("Inference Boundary Lower Limit", f"{lower_bound:,.0f} Units")
        mc3.metric("Inference Boundary Upper Limit", f"{upper_bound:,.0f} Units")

        st.markdown("<br>", unsafe_allow_html=True)
        if pred > 7000:
            st.success("High Velocity Pattern Detected: Scale warehouse purchase orders and load regional logistics parameters early to circumvent pipeline congestion.")
        elif pred > 4000:
            st.info("Stable Distribution State: Local inventory velocities remain strictly inline with model baseline performance indices.")
        else:
            st.warning("Dynamic Drawdown Pattern Detected: De-escalate active holding parameters to preserve asset liquid capital positions.")

#  PAGE 3: PRICING INTELLIGENCE
elif selected == "Pricing Intelligence":
    st.title("Price Elasticity & Frontier Curve Mapping")
    st.write("Calculates profit-maxima vectors relative to real-time predictive demand baseline outputs.")

    pipeline_baseline_demand = st.session_state["calculated_forecast"]
    price = st.slider("Simulated Pricing Matrix Unit Point (INR)", min_value=50, max_value=150, value=100)

    prices = np.arange(50, 151)
    demand_curve = np.maximum(pipeline_baseline_demand - ((prices - 100) * (pipeline_baseline_demand * 0.004)), pipeline_baseline_demand * 0.2)
    revenue_curve = prices * demand_curve

    selected_demand = max(pipeline_baseline_demand * 0.2, pipeline_baseline_demand - ((price - 100) * (pipeline_baseline_demand * 0.004)))
    selected_revenue = selected_demand * price
    optimal_idx = np.argmax(revenue_curve)
    optimal_price = prices[optimal_idx]
    optimal_revenue = revenue_curve[optimal_idx]

    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Simulated Unit Price", f"₹{price}")
        c2.metric("Calculated Local Demand", f"{selected_demand:,.0f} Units")
        c3.metric("Expected Financial Yield", f"₹{selected_revenue:,.0f}")
        c4.metric("Mathematical Maxima Pricing", f"₹{optimal_price}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prices, y=revenue_curve, mode="lines", name="Revenue Curve", line=dict(color=accent_line, width=3.5)))
    fig.add_vline(x=optimal_price, line_dash="dash", line_color="#EF4444", annotation_text="Revenue Yield Maxima Target")
    fig.add_trace(go.Scatter(x=[optimal_price], y=[optimal_revenue], mode="markers", marker=dict(size=12, color="#EF4444"), name="Optimum Apex"))
    
    fig.update_layout(
        title=f"Marginal Profit Optimization Field (Store Node {st.session_state['target_store_id']})",
        xaxis_title="Price Metric Allocation Variable (₹)", 
        yaxis_title="Gross System Financial Returns (₹)",
        template=plotly_template, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)', 
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

#  PAGE 4: INVENTORY PLANNING
elif selected == "Inventory Planning":
    st.title("Inventory Strategy Optimization Control")
    st.write("Automated storage scheduling engine integrated natively with active inference outputs.")
    
    forecast = int(st.session_state["calculated_forecast"])
    safety_stock = int(forecast * 0.15)
    db_lookup = get_historical_store_data(st.session_state["target_store_id"])
    inventory = db_lookup["base_stock"]
    
    inventory_health = round((inventory / (forecast + safety_stock)) * 100, 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Active Run-rate Projection", f"{forecast:,} Units")
    c2.metric("Calculated Safety Stock Margin", f"{safety_stock:,} Units")
    c3.metric("Warehouse On-Hand Availability", f"{inventory:,} Units")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader(f"System Asset Stock-out Coverage Protection: {inventory_health}%")
    st.progress(min(int(inventory_health), 100))

    col1, col2 = st.columns([1.2, 1])
    with col1:
        with st.container(border=True):
            fig = go.Figure(data=[go.Pie(
                labels=["Model Projections Metric", "Safety Cushion Variables"], 
                values=[forecast, safety_stock], 
                hole=0.55,
                marker=dict(colors=["#1E3A8A", "#0D9488"])
            )])
            fig.update_layout(
                template=plotly_template, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                height=280
            )
            st.plotly_chart(fig, use_container_width=True)
            
    with col2:
        st.markdown("#### Supply Chain Core Operations Directive")
        if inventory_health >= 95:
            st.success("Secure Status Level Confirmed: Warehouse inventory thresholds verify minimal structural depletion vulnerability. Current curves support upcoming baseline trends.")
        elif inventory_health >= 80:
            st.warning("Restricted Stock-out Safety Alert: Safety buffers have slipped below target margins. Minor spikes in region transaction metrics could induce spot deficits.")
        else:
            st.error("Critical Distribution Depletion Warning: Supply stock falls into structural failure levels. Execute an urgent processing run-order update directly to avoid retail out-of-stock events.")

#  PAGE 5: MODEL INSIGHTS 
elif selected == "Model Insights":
    st.title("Model Validation Matrix Parameters & Interpretability")
    
    c1, c2 = st.columns(2)
    c1.metric("Network R-Squared Metric (R² Score)", "94.45%")
    c2.metric("Mean Absolute Error Parameter (MAE)", "506.96 Units")

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.subheader("F-Score Factor Weight Distribution Splitting Metrics")
    drivers = pd.DataFrame({
        "Feature Input Parameter Variable Name": [
            "Competition Distance Vector Metric", 
            "Historical Transaction Log Window (7 Days)", 
            "Historical Transaction Log Window (30 Days)", 
            "Store Distribution Network Index ID", 
            "Rolling Aggregation Average (30 Days)"
        ],
        "F-Score Performance Splitting Matrix Calculation": [43309, 42009, 41220, 39413, 37453]
    })
    st.dataframe(drivers, use_container_width=True, hide_index=True)

    st.subheader("Feature Importance Interpretation")

    st.info("""
    The model relies heavily on:

    • Historical Sales Patterns

    • Competition Distance

    • Rolling Sales Trends

    • Promotional Campaigns

    • Store-Level Characteristics

    These variables contribute most to forecasting accuracy.
    """)


st.markdown(f"<div style='margin-top: 60px;'><hr style='border-color:{card_border};'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#64748B; font-size:12px; padding-bottom:20px; font-weight:500;'>
    Retail-AI Predictive Platform Architecture • Built utilizing Streamlit Core Engine, Plotly Graphic Models, and Light XGBoost Frameworks.<br>
     <a href="https://github.com/asrar-ahmed1" style="color:#2563EB; text-decoration:none; font-weight:600;">GitHub</a> | <a href="https://linkedin.com/in/asrar-ahmed18" style="color:#2563EB; text-decoration:none; font-weight:600;">LinkedIn</a><br>
     <span style='color:#0F172A; font-weight:600; font-size:13px;'>Asrar Ahmed</span>
</div>
""", unsafe_allow_html=True)