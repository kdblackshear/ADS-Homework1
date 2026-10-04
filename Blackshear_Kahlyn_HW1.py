import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('palmer_penguins_raw.csv')

# Display the first 5 rows of the DataFrame
print("First 5 rows of the DataFrame: ")
print(df.head())

# Display the last 5 rows of the DataFrame
print("\nLast 5 rows of the DataFrame: ")
print(df.tail())

# Display the number of rows and columns in the DataFrame
print("\nNumber of rows and columns in the DataFrame: ")
print(df.shape)

# Display the column names of the DataFrame
print("\nColumn names of the DataFrame: ")
print(df.columns)

# Display the data types of each column in the DataFrame
print("\nData types of each column in the DataFrame: ")
print(df.dtypes)

# Display the structural information of the DataFrame
print("\nStructural information of the DataFrame: ")
print(df.info())

# Display the summary statistics of the DataFrame
print("\nSummary statistics of the DataFrame: ")
print(df.describe())

# Display the number of missing values in each column of the DataFrame
print("\nNumber of missing values in each column of the DataFrame: ")
print(df.isna().sum())

# Create working copy of the DataFrame
raw_df = df.copy()
# Create a clean copy of the DataFrame
clean_df = df.copy()

# Rename columns in the clean DataFrame
clean_df = clean_df.rename(columns={
    'studyName': 'study_name',
    'Sample Number': 'sample_number',
    'Species': 'species',
    'Region': 'region',
    'Island': 'island',
    'Stage': 'stage',
    'Clutch Completion': 'clutch_completion',
    'Date Egg': 'date_egg',
    'Individual ID': 'individual_id',
    'Culmen Length (mm)': 'culmen_length_mm',
    'Culmen Depth (mm)': 'culmen_depth_mm',
    'Flipper Length (mm)': 'flipper_length_mm',
    'Body Mass (g)': 'body_mass_g',
    'Sex': 'sex', 
    'Delta 15 N (o/oo)': 'delta_15_n',
    'Delta 13 C (o/oo)': 'delta_13_c',
    'Comments': 'comments'})

# Convert the 'date_egg' column to datetime format
clean_df['date_egg'] = pd.to_datetime(clean_df['date_egg'], errors='coerce')

# Ensure primary meaurement columns are numeric
measurement_columns = ['culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g']
for col in measurement_columns:
    clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')

# Display the data types of each column in the clean DataFrame
print("\nData types of each column in the clean DataFrame: ")
print(clean_df.dtypes)

# Inspect columns species, island, clutch_completion and sex for unique values
print("\nUnique values in 'species' column: ")
print(clean_df['species'].unique())

print("\nUnique values in 'island' column: ")
print(clean_df['island'].unique())

print("\nUnique values in 'clutch_completion' column: ")
print(clean_df['clutch_completion'].unique())

print("\nUnique values in 'sex' column: ")
print(clean_df['sex'].unique())

# Display number of rows before cleaning
print("\nNumber of rows before cleaning: ")
print(clean_df.shape[0])

# Replace placeholder values in 'sex' column with pd.NA
clean_df['sex'] = clean_df['sex'].replace(['nan', '.'], pd.NA)
# Standardize the values in 'species' to shortened names
clean_df['species'] = clean_df['species'].replace({
    'Adelie Penguin (Pygoscelis adeliae)': 'Adelie',
    'Chinstrap penguin (Pygoscelis antarctica)': 'Chinstrap',
    'Gentoo penguin (Pygoscelis papua)': 'Gentoo'
})

# Display the number of duplicate rows in the clean DataFrame
print("\nNumber of duplicate rows in the clean DataFrame: ")
print(clean_df.duplicated().sum())

# Display repeated occurrences of the 'individual_id' values in the clean DataFrame
print("\nRepeated occurrences of 'individual_id' values in the clean DataFrame: ")
print(clean_df['individual_id'].duplicated(keep=False).sum())

# Display category counts for 'species', 'island', 'clutch_completion' and 'sex' columns in the clean DataFrame
print("\nCategory counts for 'species' column in the clean DataFrame: ")
print(clean_df['species'].value_counts())

print("\nCategory counts for 'island' column in the clean DataFrame: ")
print(clean_df['island'].value_counts())

print("\nCategory counts for 'clutch_completion' column in the clean DataFrame: ")
print(clean_df['clutch_completion'].value_counts())

print("\nCategory counts for 'sex' column in the clean DataFrame: ")
print(clean_df['sex'].value_counts())

# Keep only the rows that contain recorded value for required fields
required_fields = ['species', 'island', 'culmen_length_mm', 'culmen_depth_mm', 'flipper_length_mm', 'body_mass_g', 'sex']
clean_df = clean_df.dropna(subset=required_fields).copy()

# Display number of rows after cleaning
print("\nNumber of rows after cleaning: ")
print(clean_df.shape[0])

# Verify the four primary measurement columns contain only positive values
for col in measurement_columns:
    if (clean_df[col] <= 0).any():
        print(f"\nWarning: Column '{col}' contains non-positive values.")
    else:
        print(f"\nColumn '{col}' contains only positive values.")

# Verify that 'species' contains only 'Adelie', 'Chinstrap', or 'Gentoo'
valid_species = ['Adelie', 'Chinstrap', 'Gentoo']
assert set(clean_df['species'].unique()).issubset(valid_species), "Error: 'species' column contains invalid values."

# Verify that 'island' contains only the categories observed in the original dataset
valid_islands = clean_df['island'].unique()
assert set(clean_df['island'].unique()).issubset(valid_islands), "Error: 'island' column contains invalid values." 

# Verify that the required fields from Task 3 do not contain any missing values
assert clean_df[required_fields].notna().all().all(), "Error: Required fields contain missing values."

# Verify that the cleaned dataset contains no duplicate rows
assert clean_df.duplicated().sum() == 0, "Error: Cleaned dataset contains duplicate rows."

# Confimation message that all assertions passed
print("\nAll assertions passed. The cleaned dataset is valid.")

# Display all Gentoo penguins that have a body mass greater than 5000 grams
gentoo_over_5000 = clean_df[(clean_df['species'] == 'Gentoo') & (clean_df['body_mass_g'] > 5000)]
print("\nGentoo penguins with body mass greater than 5000 grams: ")
print(gentoo_over_5000)

# Display all female Adelie penguins from Torgersen Island
adelie_females_torgersen = clean_df[(clean_df['species'] == 'Adelie') & (clean_df['sex'] == 'FEMALE') & (clean_df['island'] == 'Torgersen')]
print("\nFemale Adelie penguins from Torgersen Island: ")
print(adelie_females_torgersen)

# Display the five penguins with the greatest flipper length
top_flipper_length = clean_df.nlargest(5, 'flipper_length_mm')[['species', 'island', 'sex', 'flipper_length_mm', 'body_mass_g']]
print("\nFive penguins with the greatest flipper length: ")
print(top_flipper_length)

# Display the number of penguins in each species category
print("\nNumber of penguins in each species category: ")
print(clean_df['species'].value_counts())

# Display the mean body mass for each species category
mean_body_mass = clean_df.groupby('species')['body_mass_g'].mean().round(2)
print("\nMean body mass for each species category: ")
print(mean_body_mass)

# Display the mean culmen length, mean flipper length, and mean body mass for each species category
mean_measurements = clean_df.groupby('species')[['culmen_length_mm', 'flipper_length_mm', 'body_mass_g']].mean().round(2)
print("\nMean culmen length, mean flipper length, and mean body mass for each species category: ")
print(mean_measurements)

# Display the number and mean body mass of penguins grouped by both species and sex
grouped_stats = clean_df.groupby(['species', 'sex']).agg(
    count=('body_mass_g', 'count'),
    mean_body_mass=('body_mass_g', 'mean')
).round(2)
print("\nNumber and mean body mass of penguins grouped by species and sex: ")
print(grouped_stats)

# Save the cleaned DataFrame to a new CSV file
clean_df.to_csv('palmer_penguins_cleaned.csv', index=False)

check_df = pd.read_csv('palmer_penguins_cleaned.csv')

# Display first 5 rows of the cleaned DataFrame
print("\nFirst 5 rows of the cleaned DataFrame: ")
print(check_df.head())

# Display shape of the cleaned DataFrame
print("\nShape of the cleaned DataFrame: ")
print(check_df.shape)

# Display the missing values in the cleaned DataFrame
print("\nMissing values in the cleaned DataFrame: ")
print(check_df.isna().sum())