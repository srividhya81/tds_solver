import pandas as pd
import rapidfuzz
from rapidfuzz import process

def analyze_sales(file_path: str, product: str, location: str, min_units: int) -> dict:
    """
    Analyze sales data to calculate total units sold for a specific product and location.

    Args:
        file_path (str): Path to the CSV file containing sales data.
        product (str): The product to filter (e.g., "Keyboard").
        location (str): The city to filter (e.g., "Chennai").
        min_units (int): Minimum number of units sold.

    Returns:
        dict: A dictionary containing the total units sold for the specified product and location.
    """
    try:
        # Step 1: Load the dataset
        df = pd.read_csv(file_path)

        # Step 2: Group mis-spelled city names using phonetic clustering
        unique_cities = df["City"].unique()
        city_mapping = {city: process.extractOne(city, unique_cities)[0] for city in unique_cities}
        df["City"] = df["City"].map(city_mapping)

        # Step 3: Filter sales entries
        filtered_df = df[
            (df["Product"] == product) &
            (df["City"] == location) &
            (df["Units Sold"] >= min_units)
        ]

        # Step 4: Aggregate sales by city
        aggregated_sales = filtered_df.groupby("City")["Units Sold"].sum()

        # Step 5: Return the result for the specified location
        total_units = aggregated_sales.get(location, 0)
        return {"city": location, "product": product, "total_units_sold": total_units}

    except Exception as e:
        return {"error": f"An error occurred: {e}"}