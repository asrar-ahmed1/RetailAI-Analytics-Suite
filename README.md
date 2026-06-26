# Retail-AI Analytics Suite 

An enterprise-grade predictive demand forecasting, price elasticity modeling, and automated inventory management system built with Streamlit, Plotly, and XGBoost.

##  Key Architectural Features
- **Demand Forecasting Engine:** Ingests dynamic rolling auto-regressive sales lags (7-day/30-day means) to project consumer transaction volumes.
- **Price Elasticity Frontier:** Simulates economic elasticity fields using empirical demand-price coefficients to optimize profit-maxima positions.
- **Automated Inventory Strategy:** Evaluates safety-stock cushion margins dynamically, throwing stock-out mitigation advisories.
- **Modern User Experience:** Built using custom modular light-mode UI design tokens, fast-caching algorithms (`@st.cache_data`), and crisp data vectors.

## Business Problem
Retailers struggle with:
Demand forecasting,
Price optimization,
Inventory planning,
Revenue maximization.

## Solution
Built a platform combining:
XGBoost Forecasting Model,
Streamlit Web Application.

##  Tech Stack & Architecture
- **Core App Framework:** Streamlit
- **ML & Data Processing:** Python, Pandas, NumPy, Joblib, XGBoost / Scikit-Learn
- **Inference Visualization:** Plotly Graphing Objects
- **Navigation Controls:** Streamlit Option Menu

## Machine Learning Performance
| Metric   | Value  |
| -------- | ------ |
| R² Score | 0.9445 |
| MAE      | 506.96 |

<img width="1918" height="917" alt="Screenshot 2026-06-26 221546" src="https://github.com/user-attachments/assets/25ffa3be-727f-4d6c-be64-63346cafd997" />

<img width="1907" height="915" alt="Screenshot 2026-06-25 151113" src="https://github.com/user-attachments/assets/c09616ba-6561-4f96-8e7b-c57402ea2a15" />

<img width="1918" height="915" alt="Screenshot 2026-06-25 151149" src="https://github.com/user-attachments/assets/5b33b826-630a-4770-90dd-27e6e1a206b0" />

<img width="1913" height="912" alt="Screenshot 2026-06-25 151209" src="https://github.com/user-attachments/assets/0d87143f-9849-4d19-8bfd-edc5552aa8fd" />


##  Local Quickstart Installation

1. Clone this repository to your local architecture:
   ```bash
   git clone [https://github.com/asrar-ahmed1/RetailAI-Analytics-Suite.git](https://github.com/asrar-ahmed1/RetailAI-Analytics-Suite.git)
   cd RetailAI-Analytics-Suite
