from datasets import load_dataset

def dataset_to_dict(dataset_name:str, split=None) -> dict:
    dataset = load_dataset(dataset_name)
    if split:
        splits = {split: dataset[split]}
    else:
        splits = dataset
    combined = {} # This is the dict which is going to store all the columns 
    # of the dataset as the keys and the row values as a index positioned lists
    for split_name, split_data in split.items():
        for col in split_data.column_names:
            if col not in combined:
                combined[col] = []
            combined[col].extend(split_data[col])
    return combined