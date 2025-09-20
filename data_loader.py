import pandas as pd
FILE_ID = "1NmsM2-TKO-lf6jX2R_V68bG05shkZ2On"
file_url = f"https://drive.google.com/uc?id={FILE_ID}"
raw_data = pd.read_csv(file_url)
print(raw_data.head(10))