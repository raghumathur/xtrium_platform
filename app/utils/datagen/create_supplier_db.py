import pandas as pd
import random

def create_updated_supplier_database(material_ids):
    supplier_data = []
    geolocations = ['USA', 'Germany', 'India', 'Japan', 'Australia']
    supplier_names = [f"Supplier {chr(65 + i)}" for i in range(20)]
    material_types = ['Element', 'Compound', 'Custom']
    certifications = ['ISO 9001', 'ISO 14001', 'RoHS', 'CE', 'None']

    for material_id in material_ids:
        num_suppliers = random.randint(3, 6)  # 3 to 6 suppliers per material
        for _ in range(num_suppliers):
            supplier_entry = {
                'Supplier ID': f"S{random.randint(1000, 9999)}",
                'Supplier Name': random.choice(supplier_names),
                'Material ID': material_id,
                'Material Type': random.choice(material_types),
                'Geolocation': random.choice(geolocations),
                'Contact Info': f"contact_{random.randint(1000, 9999)}@example.com",
                'Availability': random.choice(['In Stock', 'Out of Stock', 'Limited']),
                'Cost Range': f"{round(random.uniform(10, 100), 2)}-{round(random.uniform(101, 500), 2)} USD",
                'Rating': round(random.uniform(1, 5), 1),
                'Certifications': random.choice(certifications)
            }
            supplier_data.append(supplier_entry)

    return pd.DataFrame(supplier_data)

# Simulate material IDs
material_ids = [f"M{random.randint(1000, 1999)}" for _ in range(50)]

# Create the updated Supplier Database
updated_supplier_database = create_updated_supplier_database(material_ids)

# Save the updated CSV
updated_supplier_database.to_csv('updated_supplier_database.csv', index=False)

print("Updated supplier database saved as 'updated_supplier_database.csv'")