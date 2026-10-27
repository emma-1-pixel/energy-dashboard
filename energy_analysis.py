import pandas as pd

df = pd.read_csv("owid-energy-data.csv")
print("Original shape:", df.shape)

cols = ["country", "year", "iso_code", "population",
        "electricity_generation", "electricity_demand", "per_capita_electricity",
        "coal_share_elec", "gas_share_elec", "oil_share_elec", "nuclear_share_elec",
        "hydro_share_elec", "solar_share_elec", "wind_share_elec",
        "renewables_share_elec", "fossil_share_elec", "low_carbon_share_elec",
        "coal_electricity", "gas_electricity", "oil_electricity",
        "nuclear_electricity", "hydro_electricity", "solar_electricity",
        "wind_electricity", "carbon_intensity_elec"]
df = df[cols]

# Keep only countries: regions and totals like "World" have no iso_code
df = df[df["iso_code"].notna()]

# Keep 2000 onwards and rows that have electricity data
df = df[df["year"] >= 2000]
df = df.dropna(subset=["electricity_generation"])

print("Clean shape:", df.shape)
print("Countries:", df["country"].nunique())
print("Years:", df["year"].min(), "to", df["year"].max())
print("World still in data?", "World" in df["country"].values)
print(df[df["country"] == "Greece"].tail(3)[["country", "year", "electricity_generation", "renewables_share_elec"]])
# Duplicate country-year rows
print("Duplicate country-year rows:", df.duplicated(subset=["country", "year"]).sum())

# Missing values in the key columns (percent)
key = ["electricity_generation", "renewables_share_elec", "fossil_share_elec",
       "solar_share_elec", "wind_share_elec", "carbon_intensity_elec"]
print((df[key].isna().mean() * 100).round(1))

# Sanity check: shares should not exceed about 100%
print("Max renewables share:", df["renewables_share_elec"].max())
print("Min electricity generation:", df["electricity_generation"].min())
df.to_csv("energy_clean.csv", index=False)