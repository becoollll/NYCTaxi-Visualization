# NYC Taxi Visualization

## Project Overview
This is a web application built with Dash framework for analyzing New York City taxi trip data. The application provides multiple analysis modules including data cleaning, outlier detection, Principal Component Analysis (PCA), and more.

## Features
- Data cleaning and preprocessing
- Outlier analysis and handling 
- Principal Component Analysis (PCA)
- Normality testing
- Data transformation
- Numerical and categorical data visualization
- Statistical analysis

## Tech Stack
- Python
- Dash
- Pandas
- NumPy
- Scikit-learn
- Plotly

## Project Structure
```bash
NYCTaxiVisualization/
  ├── app.py                    # Main application entry 
  ├── data_manager.py           # Data management and processing 
  ├── components/
  │   ├── __init__.py                     
  │   ├── home.py
  │   ├── data_cleaning.py
  │   ├── outlier.py
  │   ├── pca.py
  │   ├── normality_test.py
  │   ├── data_transform.py
  │   ├── numerical_plots.py
  │   ├── categorical_plots.py
  │   └── statistics.py       
  ├── assets/
  ├── datasets/
  ├── Dockerfilie
  └── requirements.txt
```

## Installation
1. Clone the repository
```bash
git clone https://github.com/becoollll/NYCTaxi-Visualization/tree/main
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage
1. Run the application
```bash
python app.py
```

2. Open a browser and visit the local server
```bash
http://localhost:8050
```

## Docker Deployment
The project supports Docker deployment. Use these commands to build and run the container:
```bash
docker build -t taxi-analysis-dashboard .
docker run -p 8050:8050 taxi-analysis-dashboard
```

## Data Sources
- [NYC Yellow Taxi Trip Data (yellow_tripdata_2024-07.parquet)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- [Taxi Zone Geographic Data (taxi_zones.geojson)](https://data.cityofnewyork.us/Transportation/NYC-Taxi-Zones/d3c5-ddgc)

