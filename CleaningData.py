import pandas as pd

df = pd.read_csv("C:/Users/eswar/Downloads/AB_NYC_2019.csv")
print("Data loaded successfully.")

print("\n--- Head of the Data ---")
print(df.head())

print("\n--- DataFrame Info ---")
df.info()

missing_values_count = df.isnull().sum()
print("\n--- Count of Missing Values per Column ---")
print(missing_values_count)

total_rows = len(df)
missing_values_percentage = (missing_values_count / total_rows) * 100
print("\n--- Percentage of Missing Values per Column ---")
print(missing_values_percentage)

df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
print("\n'reviews_per_month' missing values filled with 0.")

df['name'] = df['name'].fillna('Unknown')
df['host_name'] = df['host_name'].fillna('Unknown')
print("'name' and 'host_name' missing values filled with 'Unknown'.")

df['last_review'] = df['last_review'].fillna('No Review')
print("'last_review' missing values filled with 'No Review'.")

print("\n--- Verification: Missing Values After Cleaning ---")
print(df.isnull().sum())
