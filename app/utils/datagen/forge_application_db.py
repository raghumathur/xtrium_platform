import pandas as pd
import random

def create_applications_database(material_ids):
    applications = []
    industries = [
        "EV Batteries", "Semiconductors", "Space Research", "Defense", "Food Industry",
        "Jewelry", "Precious Metals", "Optics", "Solar Energy", "Quantum Computing",
        "Chip Design", "Chip Cooling", "Construction", "Healthcare", "Drug Discovery", 
        "Surgery", "Automotive", "Aerospace", "Telecommunications", "Energy Storage"
    ]
    products = [
        "Battery Cells", "Processors", "Thermal Shields", "Armor Plating", "Packaging",
        "Watches", "Catalysts", "Lenses", "Panels", "Quantum Chips",
        "Integrated Circuits", "Heat Sinks", "Cement", "Medical Implants", "Medicines",
        "Surgical Tools", "Car Bodies", "Satellites", "Antennas", "Fuel Cells"
    ]
    properties = [
        "Conductivity", "Thermal Resistance", "Strength", "Reactivity", "Corrosion Resistance",
        "Flexibility", "Transparency", "Hardness", "Durability", "Weight"
    ]
    fields_of_science = [
        "Physics", "Chemistry", "Biology", "Materials Science", "Engineering", 
        "Medicine", "Astronomy", "Geology", "Nanotechnology", "Computer Science"
    ]

    for i in range(300, 501):  # Create 300-500 rows
        application_id = f"A{i}"
        industry = random.choice(industries)
        product = random.choice(products)
        field = random.choice(fields_of_science)
        matched_material_id = random.choice(material_ids)
        required_properties = random.sample(properties, random.randint(2, 5))
        match_score = random.randint(70, 100)  # Match score between 70 and 100

        application_entry = {
            "Application ID": application_id,
            "Industry": industry,
            "Product": product,
            "Field of Science": field,
            "Material ID": matched_material_id,
            "Required Properties": ", ".join(required_properties),
            "Match Score": match_score,
            "Priority": random.choice(["High", "Medium", "Low"]),
            "Environmental Impact": random.choice(["Low", "Moderate", "High"]),
            "Economic Viability": random.choice(["Feasible", "Challenging", "Expensive"]),
            "Potential Market Size": random.choice(["Small", "Medium", "Large"]),
            "Future Research Scope": random.choice(["Low", "Medium", "High"]),
        }
        applications.append(application_entry)

    return pd.DataFrame(applications)

# Simulate material IDs
material_ids = [f"M{random.randint(1000, 1999)}" for _ in range(50)]

# Create the Applications Database
applications_database = create_applications_database(material_ids)

# Save the Applications Database CSV
applications_database.to_csv('applications_database.csv', index=False)

print("Applications database saved as 'applications_database.csv'")