# JSON-Data-project


This project offers a hands-on tool for exploring and analyzing restaurant health inspection data using MongoDB, providing a setup for building querying skills and conducting data analysis. It includes the following components:

- **`create_database.py`**: Sets up a MongoDB database, loads restaurant data from a JSON file, and initializes a "restaurants" collection, readying the data for analysis.
  
- **`restaurant_data_api.py`**: This module provides a class to interact with the MongoDB database, enabling various data operations on the "restaurants" collection. Key methods include finding restaurants by borough, retrieving the top N restaurants with the highest inspection scores, and counting restaurants by location.

- **`Data_Interpretation.ipynb`**: A Jupyter notebook for visualizing data insights, helping users explore trends in health scores, compliance levels across cuisines, and the geographical distribution of restaurants across New York City’s boroughs.

The `Data_Interpretation.pdf` report serves as a reference, presenting visualization conclusions along with code snippets that demonstrate API usage, offering insights into the analysis process and results achieved.
