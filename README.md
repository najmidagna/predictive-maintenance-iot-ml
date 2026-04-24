
🛢️ Predictive Maintenance System for Oil & Gas Equipment  
Built with Streamlit • XGBoost • Python

📘 Overview

This project is a Predictive Maintenance System designed for oil & gas pump equipment.  
It uses IoT sensor data and machine learning (XGBoost) to:

• Predict equipment failure probability  
• Monitor pump health in real time  
• Generate warnings and critical alerts  
• Visualize trends and performance  
• Maintain detailed logs of predictions  
• Provide a complete maintenance decision-support dashboard  

This system is built as part of a Final Year Project (FYP).

🚀 Key Features
User Authentication
• Login system (Admin / User)
• Admin‑only user registration
• Access‑protected pages

Upload IoT Sensor Data
Upload CSV files containing:
• Air temperature [K]  
• Process temperature [K]  
• Rotational speed [rpm]  
• Torque [Nm]  
• Tool wear [min]  

Predict Pump Health
• Uses XGBoost model  
• Calculates failure probability  
• Categorizes health status as:
  - 🟢 NORMAL  
  - 🟠 WARNING  
  - 🔴 CRITICAL  

Failure Probability Gauge
A speedometer‑style gauge showing average failure risk across the uploaded dataset.

Dashboard Analytics
• Sensor trend graphs  
• Failure probability trends  
• Status distribution pie chart  
• KPI summary  
• Alerts panel  
• Latest 10 logs  

Detailed Equipment Log
• Full prediction history  
• Search/filter by health status  
• CSV export  
• Timestamped entries

Instant Manual Health Check
Predicts pump condition without needing a CSV file.

Downloadable Reports
Generate and download:
• Prediction results  
• Filtered logs  
• Summary report  

## 📁 Project Structure

```
FYP2/
├── __pycache__/
│   ├── footer.cpython-312.pyc
│   ├── login.cpython-312.pyc
│   └── sidebar.cpython-312.pyc
├── model/
│   ├── scaler2.pkl
│   └── trained_model_xgb.pkl
├── pages/
│   ├── 0_Home.py
│   ├── 1_Dashboard.py
│   ├── 2_Upload_Data.py
│   ├── 3_Predict_Health.py
│   ├── 4_Instant_Health_Check.py
│   ├── 5_Detailed_Log.py
│   ├── 6_Download_Report.py
│   └── 7_Register_User.py
├── Test data/
├── Data_Preprocessing_and_Model_Training.py
├── footer.py
├── Login_Page.py                # Main entry (login + redirect)
├── login.py
├── sidebar.py
├── users.json
├── requirements.txt
└── README.md
```

🧠 Machine Learning Model
Algorithm:  
✔ XGBoost Classifier  
✔ Balanced using scalepos_weight  
✔ Features standardized using StandardScaler  
✔ Outputs probability 0–1

Input Features
• Air temperature  
• Process temperature  
• Shaft rotational speed  
• Torque  
• Tool wear  

Output
• Failure probability  
• Health status classification  
• Logged prediction for trend analysis  

📊 Data Flow
User logs in
Upload sensor CSV or use Instant Check
Data is preprocessed and scaled
Model predicts failure probability
Failure gauge + health label displayed
Result saved to system log
Logs used for:
   - Dashboard
   - Detailed log page
   - Reports
   - Latest prediction display on Home Page

🧩 Technology Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit UI |
| Backend | Python |
| Machine Learning | XGBoost, Scikit‑Learn |
| Data Visualization | Plotly, Streamlit charts |
| Storage | JSON (login), Session state (logs), CSV exports |

▶️ How to Run
1. Install Dependencies
`
pip install -r requirements.txt
`

2. Run the System
`
streamlit run Login_page.py
`

3. Login
Default admin (if users.json is empty):

`
username: admin
password: 1234
`


🛠️ Future Enhancements (Optional)
• Email/SMS alert system  
• Automated maintenance scheduling  
• Integration with real-time IoT MQTT sensors  
• Multi‑equipment support (Pump A, Pump B, etc.)  
• Predictive root‑cause analysis (SHAP values)

👨‍🎓 Author
Najmi Dagna
Final Year Project — Predictive Maintenance System for Oil & Gas Equipment  

