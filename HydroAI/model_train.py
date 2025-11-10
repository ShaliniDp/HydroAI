# model_train.py
import pandas as pd
from utils import train_model

if __name__ == "__main__":
    df = pd.read_csv("C:\Users\MONISHA .D\Desktop\ADS\HYDRO AI PROJECT\HydroAI\wellness_dataset.csv")
    info = train_model(df)
    print("Model trained and saved:", info)
