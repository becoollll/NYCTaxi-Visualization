# NYCTaxi-Visualization

```bash
NYCTaxiVisualization/
  backend/
  ├── app/
  │   ├── __init__.py                     
  │   ├── main.py                         # 主伺服器檔案
  │   ├── models/
  │   │   ├── item_model.py     
  │   │   └── __init__.py                
  │   ├── routers/
  │   │   ├── TaxiDataset.parquet     
  │   │   ├── data_cleaning.py           
  │   │   ├── data_transformation.py     
  │   │   ├── data_visualization.py      
  │   │   ├── dimensionality_reduction.py
  │   │   ├── normality_test.py          
  │   │   ├── statistic.py               
  │   │   └── __init__.py                
  │   └── utils/
  │       └── plotting.py                
  └── requirements.txt
  frontend/
  ├── node_modules/
  ├── public/
  │   ├── index.html                     
  │   └── logo.png  
  ├── src/
  │   ├── App.js
  │   ├── App.css           
  │   ├── index.css
  │   ├── index.js
  │   ├── components/
  │   │   ├── Header.js     
  │   │   └── Footer.js
  │   └── styles/
  │       ├── Home.css   
  │       ├── DataCleaning.css           
  │       ├── DataTransformation.css     
  │       ├── DataVisualization.css      
  │       ├── DimensionalityReduction.css
  │       ├── NormalityTest.js                      
  │       └── Statistic.js               
  │   └── pages/
  │       ├── Home.js   
  │       ├── DataCleaning.js           
  │       ├── DataTransformation.js     
  │       ├── DataVisualization.js      
  │       ├── DimensionalityReduction.js
  │       ├── NormalityTest.js                      
  │       └── Statistic.js                
  ├── package-lock.json
  └── package.json
  .venv/                              
