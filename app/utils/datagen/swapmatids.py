import pandas as pd
import random

# Load the Materials Database
materials_database_path = 'materials_materialsproject_LiFexx_new.csv'  # Replace with your file path
materials_database = pd.read_csv(materials_database_path)

# Get unique Material IDs from Materials Database
material_ids = materials_database['Material ID'].unique()

# Load the Suppliers Database
suppliers_database_path = 'supplier_database.csv'  # Replace with your file path
suppliers_database = pd.read_csv(suppliers_database_path)

# Replace Material IDs in Suppliers Database
suppliers_database['Material ID'] = random.choices(material_ids, k=len(suppliers_database))

# Save the updated Suppliers Database
updated_suppliers_database_path = 'updated_suppliers_database.csv'
suppliers_database.to_csv(updated_suppliers_database_path, index=False)

# Load the Applications Database
applications_database_path = 'applications_database.csv'  # Replace with your file path
applications_database = pd.read_csv(applications_database_path)

# Replace Material IDs in Applications Database
applications_database['Material ID'] = random.choices(material_ids, k=len(applications_database))

# Save the updated Applications Database
updated_applications_database_path = 'updated_applications_database.csv'
applications_database.to_csv(updated_applications_database_path, index=False)

print("Material IDs updated in Suppliers and Applications Databases.")
print(f"Updated Suppliers Database saved to: {updated_suppliers_database_path}")
print(f"Updated Applications Database saved to: {updated_applications_database_path}")