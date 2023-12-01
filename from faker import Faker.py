from faker import Faker
import random
import pandas as pd

# Initialize Faker with the 'en_IN' locale for Indian names
fake = Faker('en_IN')

# Function to generate a random connection between two first names
def generate_connection():
    source = fake.first_name()
    target = fake.first_name()
    while source == target:
        target = fake.first_name()
    return source, target

# Generate a big dataset with connections
num_records = 500  # Adjust the number of records as needed
connections = [generate_connection() for _ in range(num_records)]

# Create a DataFrame from the connections
df = pd.DataFrame(connections, columns=['Source', 'Target'])

# Save the DataFrame to a CSV file named 'insta.csv'
df.to_csv('insta.csv', index=False)

# Display the first few rows of the DataFrame
print(df.head())
