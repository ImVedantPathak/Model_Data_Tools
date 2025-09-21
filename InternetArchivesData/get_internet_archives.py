import internetarchive as ia

'''For Specific File Download'''
identifier = ""
ia.download(
    identifier, 
    verbose=True,
    destdir="", #put dest download folder path
    )


'''For Collection Download'''
collection_identifier = "mitlibrariespublicdomain"


destination_folder = ""#put dest download folder path
search_results = ia.search_items(f'collection:{collection_identifier}')

for result in search_results:
    item_identifier = result['identifier'] 
    print(f'Downloading item: {item_identifier}')
    try:
        ia.download(
            item_identifier,
            destdir=destination_folder,
            verbose=True,
            glob_pattern="*.pdf"
        )
    except Exception as e:
        print(f'Error downloading {item_identifier}: {e}')