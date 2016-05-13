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
import xlrd


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
    cols = ['device_name', 'bna_realm', 'vendor', 'device_type', 'model',
            'os_image', 'bna_created_date', 'pri_host_name_ip', 'entities',
            'entities_descr', 'entities_PID', 'entities_VID', 'entities_SN',
            'device_function', 'region', 'serial_number', 'site_code',
            'supervisor_type']

    data = pd.read_csv(
        file_res, skiprows=3, skip_footer=1, index_col=False, sep=',',
        header=None, names=cols, engine='python'
    )
    # make col headers more 'key' friendly
    # data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
    # Drop rows where Serial Number is empty
    # data = data.dropna(subset=['serial_number'])
    # Split the OS Image column by "," and ";" to remove extraneous data
    data['os_image'].update(data['os_image'].apply(
        lambda x: x.split(",")[0] if len(x.split()) > 1 else None)
    )
    data['os_image'].update(data['os_image'].apply(
        lambda x: x.split(";")[0] if len(x.split()) > 1 else None)
    )
    # data.set_index('device_name', inplace=True)
    # convert data to JSON, one doc per row for insertion to mongoDB
    data_json = json.loads(data.to_json(orient='records'))
    # remove and previous stored data
    db_cm.remove()
    # insert JSON data to mongoDB collection.
    db_cm.insert(data_json)
    # create an Index for Serial Number; set to non-unique due to dirty data
    db_cm.create_index([('entities_SN', pymongo.ASCENDING)], unique=False)

    # write Device rows with duplicate Serial Numbers to a CSV
    # dupes = {}
    # dupes = data[data.duplicated(['serial_number'], keep='last') |
    #              data.duplicated(['serial_number'])]
    # dupes.to_excel(cdir + 'duplicates.xlsx')

    # by_model = []
    # by_model = data.os_image.groupby('model').nunique().sort_values(ascending=False)
    # by_model = pd.pivot_table(data, index=['model', 'os_image'],
    #                           values=['count'], aggfunc=[len])
    # by_model.to_excel(cdir + 'modelcount.xlsx', index=True,
    #                   sheet_name='by_model')

    # by_os = {}
    # by_os = data.groupby(['os_image', 'model']).size().sort_values(ascending=False)
    # by_os.to_frame().to_excel(cdir + 'oscount.xlsx', index=True,
    #                           sheet_name='by_os')

# call method
if __name__ == "__main__":
    # Define path to CSV
    filepath = '/vagrant/data/DeviceInventory-Category.Switch.XOM.csv'
    import_content(filepath)
