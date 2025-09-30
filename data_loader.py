import pandas as pd
import os

FILE_ID = "1NmsM2-TKO-lf6jX2R_V68bG05shkZ2On"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
raw_data = pd.read_csv(file_url)
raw_data.to_csv("data/raw_data.csv", index=False)
print("Данные сохранены в data/raw_data.csv")
print(raw_data.head(10))

df = pd.DataFrame(
    {"id": ["1", "2", "3"], "value": ["10.5", "20.1", "30.7"], "flag": [1, 0, 1]}
)
df["id"] = df["id"].astype(int)
df["value"] = df["value"].astype(float)
df["flag"] = df["flag"].astype(bool)

print(df.dtypes)
