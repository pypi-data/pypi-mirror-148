'''
--------------------------------------------------------------
                    IRODS and CyVerse I/O
--------------------------------------------------------------
This example file shows some capabilities given by this utility class.
Here, we discuss the available wrapper on IRODS commands.
It allows to perform and automate actions on CyVerse's file storage system.

NOTE: Be sure to have configured your cache and your irods environment before 
testing these functionnalities. You can do so by using the file 'example_configuration.py'

Resources for more information:
- IRODS: https://docs.irods.org/4.2.11/
- python-irodsclient: https://github.com/irods/python-irodsclient
- CyVerse: https://cyverse.org/discovery-environment
--------------------------------------------------------------
'''

# ------------------ imports ------------------
import asyncio
from datetime import datetime
import os
from circles_file_iterator.utils.cache import init_cache, remove_file_from_cache, get_all_files_from_cache_dir
from circles_file_iterator.utils.cyverse_io_irods import IRODSGet, IRODSPut, getIRODSSession
from circles_file_iterator.utils.cyverse_files import ipwd, ils, icd
from circles_file_iterator.global_variables.global_variables import cyverse_path_server_resources, local_temp_folder, cyverse_path_server_resources_test

# ------------------ creating the async loop ------------------
'''
    -> AN IMPORTANT NOTE ON THE ASYNCHRONOUS BEHAVIOR:

we have to create an async loop and wait for its completion to be able to perform
an 'await' in the python script. See the link below for more information:
https://docs.python.org/3/library/asyncio-eventloop.html#running-and-stopping-the-loop
https://stackabuse.com/python-async-await-tutorial/, section 'Running the Event Loop'

In a server environment, you can just use those Get/Put inside of async functions, using await to wait
for their completion. You can see an example below

async def some_function():
    ....
    await IRODSGet(remote, local)
    ....
'''
loop = asyncio.get_event_loop()


# ======================= FILESHARE COMMANDS =======================
'''
These commands allows to perform remotely unix navigation commands within IRODS files.
'''

print('\n------------------------IRODS COMMANDS------------------------\n')

print('Going to /iplant/noecarras/resources_file_iterator/ with the irods cd command')
icd(cyverse_path_server_resources)

print('\nRetrieving the current location on CyVerse with the irods pwd command')
location = ipwd()
print('We are located at:\t', location)

print('\nRetrieving the folder structure at our current location with the irods ls command')
folder_structure = ils()
print('The folder structure at our current location is:\n', folder_structure)


# ======================= I/O COMMANDS =======================
'''
This part shows the IRODSGet and IRODSPut commands in action
'''

print('\n------------------------I/O COMMANDS------------------------\n')
file_to_download = '/iplant/home/noecarras/resources_file_iterator/default/file_exploration&full_exploration_publishable_circles&create_on=2021-12-01_06:10:16.920970&root=_iplant_home_sprinkjm_publishable-circles.csv'

print(f'\nDownloading this file: {file_to_download} to the local temp folder.')
local_path = loop.run_until_complete(IRODSGet(file_to_download, local_temp_folder))
print(f'The file has been downloaded into: {local_path}')

# NOTE: We modify the file so that the upload on CyVerse doesn't fail on object already existing
dl_filename = os.path.basename(local_path)
new_filename = dl_filename[:-4] + '&d' + str(datetime.now()).replace(' ', '') + '.csv'

remote_upload_path = os.path.join(cyverse_path_server_resources_test, new_filename)
print(f'\nUploading this file: {local_path} to the remote test folder: {remote_upload_path}')
remote_path = loop.run_until_complete(IRODSPut(remote_upload_path, local_path))
print(f'The file has been downloaded into: {local_path}')


# ======================= CACHE COMMANDS =======================
'''
The cache is constituted or 2 caching folders:{} long and temp.

Below lies an explanation of how to:
    - get all files from cache
    - remove 1 specific file from cache with its address
    - clearing the cache
'''
print('\n------------------------CACHE COMMANDS------------------------\n')

print('\nListing files in temp cache')
# NOTE: you can specify to check inside of the long cache folder rather than
# temp by passing the argument long=True to the function
files = get_all_files_from_cache_dir()
print('files found are:\n', files)

# We can remove 1 file from the cache like this:
print(f'\nRemoving {local_path}')
# NOTE: when using this function, be sure to pass absolute path (not relative)
# to avoid any unwanted behavior
file_removed = remove_file_from_cache(local_path)
print(f'Successful removal of the file {file_removed} from the cache')

# We can also clear the cache from all its files
# To demonstrate this, we re-download the file we used previously and we clear the cache
local_path = loop.run_until_complete(IRODSGet(file_to_download, local_temp_folder))
files = get_all_files_from_cache_dir()
print('\nfiles in the cache after redownload and before clearing are: ', files)
init_cache()
files = get_all_files_from_cache_dir()
print('files in the cache after clearing the cache are: ', files)


# ======================= MANIPULATING IRODS SESSIONS =======================
'''
I/O Commands are performed using python-irodsclient.
To handle the requests for uploading and downloading, it uses Sessions.

Below is an example or creating a long lasting session and uploading a file with this.
It can be useful for instance to upload large files.
'''

print('\n------------------------MANIPULATING IRODS SESSIONS------------------------\n')

print('\nCreating an IRODS Session object')
irods_session = getIRODSSession(timeout=3000)
print('Session object created: ', irods_session)

print('\nUsing the IRODS Session to download a file')
local_path = loop.run_until_complete(IRODSGet(file_to_download, local_temp_folder, irods_session))
print('The download of the file was performed wioth success, and the file has been placed in: ', local_path)


# ------------------ clear the cache ------------------
init_cache()

# ------------------ close the async loop ------------------
loop.close()
