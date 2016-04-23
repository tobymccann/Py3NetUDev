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


def export_content(filepath):
    # PyMongo DB setup; lazy - only called during db call
    mng_client = pymongo.MongoClient('localhost', 27017)
    mng_db = mng_client['xom_bna_swx_inv']
    collection_name = 'device.switch'
    db_cm = mng_db[collection_name]
    # CSV filepath variable
    cdir = os.path.dirname(__file__)
    file_res = os.path.join(cdir, filepath)

    cursor = db_cm.aggregate(
        [
            {"$group": {"_id": "$os_image", "count": {"$sum": 1}}}
        ]
    )

# call method
if __name__ == "__main__":
    # Define path to CSV
    filepath = '/vagrant/data/DeviceInventory-Category.Switch.Export.csv'
    export_content(filepath)
