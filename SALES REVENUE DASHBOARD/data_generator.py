"""
Data Generator for Sales & Revenue Analysis Dashboard
Generates realistic sales transaction dataset with dates, regions, product categories, pricing, discounts, costs, and customer segments.
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sales_data(num_records: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic sales data dataframe."""
    np.random.seed(seed)
    random.seed(seed)

    # Date range: past 2 years up to current date
    end_date = datetime(2026, 9, 20)
    start_date = datetime(2024, 1, 1)
    days_span = (end_date - start_date).days

    # Regions and Cities
    location_hierarchy = {
        "North America": {
            "United States": ["New York", "Los Angeles", "Chicago", "Houston", "Seattle"],
            "Canada": ["Toronto", "Vancouver", "Montreal"],
        },
        "Europe": {
            "United Kingdom": ["London", "Manchester"],
            "Germany": ["Berlin", "Munich", "Frankfurt"],
            "France": ["Paris", "Lyon"],
        },
        "Asia Pacific": {
            "Japan": ["Tokyo", "Osaka"],
            "Australia": ["Sydney", "Melbourne"],
            "Singapore": ["Singapore"],
            "India": ["Bangalore", "Mumbai"],
        },
        "Latin America": {
            "Brazil": ["São Paulo", "Rio de Janeiro"],
            "Mexico": ["Mexico City", "Guadalajara"],
        },
        "Middle East & Africa": {
            "UAE": ["Dubai", "Abu Dhabi"],
            "South Africa": ["Cape Town", "Johannesburg"],
        }
    }

    # Products Hierarchy with Base Prices and Cost Ratios
    categories = {
        "Electronics": {
            "Smartphones": [
                ("Apex Pro Smartphone 256GB", 899.00, 0.65),
                ("Apex Lite Smartphone 128GB", 499.00, 0.62),
                ("Vanguard Ultra Phone", 1199.00, 0.60),
            ],
            "Laptops & Computers": [
                ("ProBook Workstation 16-inch", 1899.00, 0.58),
                ("SlimBook Air 13-inch", 1099.00, 0.60),
                ("Gaming Titan Desktop PC", 2499.00, 0.64),
            ],
            "Audio & Wearables": [
                ("Noise-Canceling Wireless Headphones", 249.00, 0.45),
                ("Acoustic Studio Earbuds", 149.00, 0.40),
                ("Smart Fitness Watch Series 5", 299.00, 0.50),
            ],
            "Monitors & Displays": [
                ("4K UltraWide Monitor 34-inch", 649.00, 0.55),
                ("Curved Gaming Monitor 27-inch", 399.00, 0.52),
            ]
        },
        "Office Supplies": {
            "Paper & Printing": [
                ("Premium Copy Paper A4 Box", 39.99, 0.35),
                ("High-Yield Laser Toner Cartridge", 119.00, 0.30),
            ],
            "Desk Accessories": [
                ("Ergonomic Keyboard & Mouse Combo", 89.00, 0.42),
                ("Dual Monitor Arm Stand", 79.00, 0.38),
                ("LED Desk Lamp with Wireless Charging", 59.00, 0.40),
            ],
            "Storage & Filing": [
                ("Heavy-Duty Filing Cabinet 3-Drawer", 199.00, 0.50),
                ("Portable External SSD 2TB", 159.00, 0.55),
            ]
        },
        "Furniture": {
            "Chairs & Seating": [
                ("ErgoExecutive Mesh Chair", 449.00, 0.52),
                ("Task Mesh Office Chair", 199.00, 0.50),
                ("Luxury Leather Executive Recliner", 699.00, 0.56),
            ],
            "Desks & Tables": [
                ("Electric Dual-Motor Standing Desk", 599.00, 0.54),
                ("Compact Home Office Writing Desk", 229.00, 0.48),
                ("Modular Conference Table 8-Person", 1299.00, 0.58),
            ]
        },
        "Software & Cloud Services": {
            "SaaS Licenses": [
                ("Enterprise ERP Annual License", 3499.00, 0.20),
                ("Business Analytics Suite (Per User)", 499.00, 0.15),
                ("CyberSecurity Shield Pro Annual", 899.00, 0.22),
                ("Cloud Backup & Storage Enterprise", 299.00, 0.18),
            ]
        },
        "Apparel & Merchandise": {
            "Corporate Apparel": [
                ("Embroidered Polo Shirt Pack", 85.00, 0.35),
                ("Weather-Proof Softshell Jacket", 120.00, 0.40),
                ("Branded Tech Backpack", 75.00, 0.38),
            ]
        }
    }

    customer_types = ["Corporate", "Small Business", "Consumer"]
    payment_methods = ["Credit Card", "Bank Transfer", "PayPal", "Direct Invoice"]
    shipping_statuses = ["Delivered", "Delivered", "Delivered", "Shipped", "Processing", "Cancelled"]

    data = []

    for i in range(1, num_records + 1):
        order_id = f"ORD-{2024 + random.randint(0, 2)}-{i:05d}"
        
        # Date with seasonal trends (higher Q4 volume)
        random_days = np.random.beta(a=1.5, b=1.2) * days_span
        order_date = start_date + timedelta(days=int(random_days))
        
        # Region hierarchy selection
        region = random.choice(list(location_hierarchy.keys()))
        country = random.choice(list(location_hierarchy[region].keys()))
        city = random.choice(location_hierarchy[region][country])

        # Category and Product hierarchy
        cat = random.choice(list(categories.keys()))
        sub_cat = random.choice(list(categories[cat].keys()))
        product_info = random.choice(categories[cat][sub_cat])
        product_name, base_unit_price, cost_ratio = product_info

        # Price variation (+/- 5%)
        unit_price = round(base_unit_price * np.random.uniform(0.95, 1.05), 2)
        
        # Quantity based on customer type
        customer_type = random.choice(customer_types)
        if customer_type == "Corporate":
            quantity = random.randint(3, 25)
            discount = float(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], p=[0.2, 0.3, 0.3, 0.15, 0.05]))
        elif customer_type == "Small Business":
            quantity = random.randint(1, 10)
            discount = float(np.random.choice([0.0, 0.05, 0.10, 0.12], p=[0.4, 0.3, 0.2, 0.1]))
        else:
            quantity = random.randint(1, 4)
            discount = float(np.random.choice([0.0, 0.05, 0.08], p=[0.7, 0.2, 0.1]))

        # Financial Calculations
        gross_sales = round(unit_price * quantity, 2)
        discount_amount = round(gross_sales * discount, 2)
        sales_revenue = round(gross_sales - discount_amount, 2)
        
        # Unit Cost with slight variance
        unit_cost = round(unit_price * cost_ratio * np.random.uniform(0.92, 1.05), 2)
        total_cost = round(unit_cost * quantity, 2)
        profit = round(sales_revenue - total_cost, 2)
        profit_margin_pct = round((profit / sales_revenue * 100) if sales_revenue > 0 else 0, 2)

        payment = random.choice(payment_methods)
        status = random.choice(shipping_statuses)

        data.append({
            "Order ID": order_id,
            "Order Date": order_date,
            "Year": order_date.year,
            "Month": order_date.strftime("%Y-%m"),
            "Quarter": f"{order_date.year}-Q{(order_date.month - 1) // 3 + 1}",
            "Customer Type": customer_type,
            "Region": region,
            "Country": country,
            "City": city,
            "Category": cat,
            "Sub-Category": sub_cat,
            "Product Name": product_name,
            "Unit Price": unit_price,
            "Quantity": quantity,
            "Gross Sales": gross_sales,
            "Discount %": round(discount * 100, 1),
            "Discount Amount": discount_amount,
            "Sales Revenue": sales_revenue,
            "Unit Cost": unit_cost,
            "Total Cost": total_cost,
            "Profit": profit,
            "Profit Margin %": profit_margin_pct,
            "Payment Method": payment,
            "Order Status": status
        })

    df = pd.DataFrame(data)
    # Sort chronologically
    df = df.sort_values(by="Order Date").reset_index(drop=True)
    return df

def get_or_create_dataset(filepath: str = "data/sales_data.csv", num_records: int = 5000, force_recreate: bool = False) -> pd.DataFrame:
    """Load existing dataset or generate new one if missing."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if os.path.exists(filepath) and not force_recreate:
        df = pd.read_csv(filepath, parse_dates=["Order Date"])
        return df
    else:
        print(f"Generating new synthetic sales dataset with {num_records} records...")
        df = generate_sales_data(num_records=num_records)
        df.to_csv(filepath, index=False)
        print(f"Dataset successfully saved to {filepath}")
        return df

if __name__ == "__main__":
    df_sample = get_or_create_dataset(force_recreate=True)
    print(df_sample.info())
    print(df_sample.head())
