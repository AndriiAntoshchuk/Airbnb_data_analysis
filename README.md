# **Airbnb Data Analysis & Forecasting Project**

## **Project Overview**
This project analyzes Airbnb availability data to provide insights into listing trends, neighborhood availability, and forecast future trends. It utilizes **Streamlit** for an interactive dashboard, **Prophet** for time-series forecasting, and **Folium** for geographical visualization.

## **Features**
1. **Availability Trend Analysis**
    - Visualizes the total number of available Airbnb listings over time using line charts.
2. **Availability by Neighborhood**
    - Displays a bar chart of Airbnb availability across different neighborhoods.
3. **Time-Series Forecasting**
    - Uses Facebook's **Prophet** model to predict future availability trends.
4. **Geographical Visualization**
    - Generates an interactive map of Munich, color-coded by Airbnb availability in different neighborhoods.

---

## **Project Structure**
```
Airbnb_data_analysis/
│── .idea/               # IDE configuration files (can be ignored)
│── data/                # Data directory
│   ├── raw/             # Raw input data
│   │   ├── calendar.csv.gz        # Airbnb availability data
│   │   ├── listings.csv           # Listings with neighborhood information
│   │   ├── neighbourhoods.geojson # Geographical data for neighborhoods
│── data_analyse.py      # Main script for data analysis & visualization
│── launcher.py          # Script to launch the Streamlit dashboard
│── README.md            # Project documentation
```

---

## **Technologies Used**
- **Python** (`pandas`, `matplotlib`, `seaborn`, `geopandas`, `folium`)
- **Machine Learning** (Prophet for time-series forecasting)
- **Streamlit** (Interactive visualization framework)

---

## **How to Run the Project**
### Create & Activate Virtual Environment (Recommended)
Instead of globally installing dependencies, use a virtual environment:

#### **Mac/Linux**
```sh
python3 -m venv venv
source venv/bin/activate
```

#### **Windows (Command Prompt)**
```sh
python3 -m venv venv
venv\Scripts\activate
```

#### **Windows (PowerShell)**
```sh
python3 -m venv venv
venv\Scripts\Activate.ps1
```

---

###  Install Dependencies
```sh
pip install pandas matplotlib seaborn streamlit prophet geopandas folium streamlit_folium
```

---

### Navigate to the Project Directory
```sh
cd /path/to/Airbnb_data_analysis/
```
(Replace `/path/to/` with your actual path.)

---

### Run the Streamlit App
```sh
python3 launcher.py
```
or directly via:
```sh
streamlit run data_analyse.py
```

---

### (Optional) Deactivate Virtual Environment
After running the project, deactivate the virtual environment:
```sh
deactivate
```


