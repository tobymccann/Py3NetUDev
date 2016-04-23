#!/usr/bin/env python
# Author: Jason Kennemer
# Purpose: Cleanup and upload BNA CSV inventory export to mongoDB
# Requires : Device, Serial Number, Realm, Vendor, Model, and OS Image in the
# CSV export;
# Omits rows where Serial Number is empty
# Outputs a CSV file containing Devices with duplicate Serian Numbers

# import modules
import sys
import os
import pandas as pd
import pymongo
import json


def import_content(filepath):
    # PyMongo DB setup; lazy - only called during db call
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['xom_bna_swx_inv']
    collection_name = 'device.switch'
    db_cm = mng_db[collection_name]
    # CSV filepath variable
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    # Use pandas to read CSV, skipping top 2 lines, last line from
    # BNA CSV export. Set column data to string type.
    data = pd.read_csv(
        file_res, index_col=False, skiprows=2,
        skip_footer=1, converters={'Device': str, 'Serial Number': str,
                                   'Realm': str, 'Vendor': str, 'Model': str,
                                   'OS Image': str},
        engine='python'
    )
    # make col headers more 'key' friendly
    data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
    # Drop rows where Serial Number is empty
    data = data.dropna(subset=['serial_number'])
    # Split the OS Image column by "," and ";" to remove extraneous data
    data['os_image'].update(data['os_image'].apply(
        lambda x: x.split(",")[0] if len(x.split()) > 1 else None)
    )
    data['os_image'].update(data['os_image'].apply(
        lambda x: x.split(";")[0] if len(x.split()) > 1 else None)
    )
    # convert data to JSON, one doc per row for insertion to mongoDB
    data_json = json.loads(data.to_json(orient='records'))
    # remove and previous stored data
    db_cm.remove()
    # insert JSON data to mongoDB collection.
    db_cm.insert(data_json)
    # create an Index for Serial Number; set to non-unique due to dirty data
    db_cm.create_index([('serial_number', pymongo.ASCENDING)], unique=False)

    # write Device rows with duplicate Serial Numbers to a CSV
    dupes = None
    dupes = data[data.duplicated(['serial_number'], keep='last') |
                 data.duplicated(['serial_number'])]
    dupes.to_csv(cdir+'duplicates.csv')

# call method
if __name__ == "__main__":
    # Define path to CSV
    filepath = '/vagrant/data/DeviceInventory-Category.Switch.csv'
    import_content(filepath)
