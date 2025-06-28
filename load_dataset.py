from datasets import load_dataset

# Load the dataset
ds = load_dataset("TheGreatRambler/mm2_user")

# Display the first 10 rows
print("Dataset structure:")
print(ds)
print("\nFirst 10 rows:")

# Check if it's a DatasetDict (multiple splits) or a single Dataset
if hasattr(ds, 'keys'):
    # It's a DatasetDict with multiple splits
    for split_name in ds.keys():
        print(f"\n--- {split_name.upper()} split ---")
        split_data = ds[split_name]
        print(f"Number of rows: {len(split_data)}")
        
        # Show first 10 rows (or all if less than 10)
        num_rows_to_show = min(10, len(split_data))
        for i in range(num_rows_to_show):
            print(f"Row {i}: {split_data[i]}")
        break  # Just show the first split for now
else:
    # It's a single Dataset
    print(f"Number of rows: {len(ds)}")
    num_rows_to_show = min(10, len(ds))
    for i in range(num_rows_to_show):
        print(f"Row {i}: {ds[i]}") 