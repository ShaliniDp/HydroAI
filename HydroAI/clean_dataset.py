import pandas as pd

# 1️⃣ Load your full dataset
df = pd.read_csv("C:\Users\MONISHA .D\Desktop\ADS\HYDRO AI PROJECT\HydroAI\wellness_dataset.csv")

# 2️⃣ Keep only the columns needed for HydroAI
columns_needed = ["age", "gender", "weight_kg", "hydration_level", "activity_type"]
df = df[columns_needed]

# 3️⃣ Keep only the first 50 rows (you can adjust the number)
df_small = df.head(50)

# 4️⃣ Save the cleaned dataset
df_small.to_csv("health_fitness_dataset_clean.csv", index=False)

print("✅ Clean dataset saved as health_fitness_dataset_clean.csv")
print(f"👉 Columns kept: {columns_needed}")
print(f"👉 Rows kept: {len(df_small)}")
