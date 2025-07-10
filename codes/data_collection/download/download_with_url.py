import os
import requests
import pandas as pd
from tqdm import tqdm

# Load the CSV file
input_csv = '../../datasets/product/products.csv'
df = pd.read_csv(input_csv)

# Specify the directory where the PDFs will be saved
output_dir = 'pdf_downloads'
os.makedirs(output_dir, exist_ok=True)

for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Downloading PDFs"):
    url = row['File URL']
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        filename = os.path.join(output_dir, f'document_{index + 1}.pdf')

        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
