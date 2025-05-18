# This file runs necessary setup before starting the Streamlit app
import os
import sys
# Add the current directory to the path so we can import from app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Force TensorFlow to run on CPU only and suppress warnings
from app.utils.suppress_warnings import suppress_tensorflow_warnings
suppress_tensorflow_warnings()

# Run data ingestion if data file doesn't exist
from app.ingest.ipea_data import run_pipeline
from app.utils.carregar_dados import carregar_dados
import pandas as pd

def setup():
    print("Setting up application...")
    
    # Check if data exists, otherwise run ingestion
    data_path = "data/ipeadata_series.csv"
    if not os.path.exists(data_path) or os.path.getsize(data_path) == 0:
        print("Data file not found. Running data ingestion...")
        try:
            run_pipeline()
            print("Data ingestion completed successfully!")
        except Exception as e:
            print(f"Error during data ingestion: {str(e)}")
            # Create an empty dataframe with the expected columns as a fallback
            df = pd.DataFrame(columns=["data", "valor"])
            os.makedirs(os.path.dirname(data_path), exist_ok=True)
            df.to_csv(data_path, index=False)
    
    # Verify data was loaded
    df = carregar_dados()
    if df.empty:
        print("Warning: Dataset is empty. The app may not function correctly.")
    else:
        print(f"Data loaded successfully. Total records: {len(df)}")
    
    print("Setup completed!")

if __name__ == "__main__":
    setup()
