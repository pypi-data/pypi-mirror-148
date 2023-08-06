'''
--------------------------------------------------------------
         Making and using custom file share explorations
--------------------------------------------------------------
This example file shows how to create a nexw file share exploration
file.

Those files are useful in different situation:
- You want to have a list of files that you will be working on
    repeatedly and you have specific requirements regarding the
    root, the kind of folder to look at, etc
- You want to reference files as in the default but new data needs
    to be added.
- You want to reference different kind of files.

After showing this, this files shows how to use those user-specific
explorations to iterate on them.

NOTE: Be sure to have configured your cache and your irods environment before 
testing these functionnalities. You can do so by using the file 'example_configuration.py's
--------------------------------------------------------------
'''

# ------------------ imports ------------------
import asyncio
from utils.cache import init_cache
from utils.file_iterator import FileIteratorCanGps
from utils.file_exploration import create_fileshare_exploration_can_gps

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


# ======================= MAKING A NEW FILE SHARE EXPLORATION =======================
'''
Here, we show how to run an exploration for CSV CAN+GPS coupled files.
It mostly relies on calling the async function "create_fileshare_exploration".
'''
print('\n------------------------ MAKING A NEW FILE SHARE EXPLORATION ------------------------\n')

root = '/iplant/home/sprinkjm/publishable-circles/2T3Y1RFV8KC014025/libpanda/2021_01_16/'
exploration_name = 'DemoUserTest'
print(f'\nStarting file share exploration at root {root}')
remote_file_name = loop.run_until_complete(create_fileshare_exploration_can_gps(root, exploration_name, verbose=True))
print(f'It has been uploaded to {remote_file_name}')


# ======================= ITERATING OVER USER DEFINED EXPLORATION =======================
'''
Now that we have created an custom exploration, let's see how to use it within a
FileIterator object.

We can check which user explorations has been done on CyVerse, then set the exploration
to the one we did, then download locally this user exploration.
'''
print('\n------------------------ ITERATING OVER USER DEFINED EXPLORATION ------------------------\n')

# create file iterator
FileIterator = FileIteratorCanGps()
print(f'\nFile Iterator instance has been created. It prints out: {FileIterator}')

# Get user explorations
print(f'\nGetting the list of user explorations')
available_explorations = FileIterator.find_available_user_explorations()
print(f'Available explorations on CyVerse are: {available_explorations}')

# Download this explorations
# NOTE: we use this specific file but we could have used any other one
exploration_to_download = '/iplant/home/noecarras/resources_file_iterator/user/file_exploration&example_small_exploration_vandertest&create_on=2021-11-29_19:28:05.073947&root=_iplant_home_sprinkjm_publishable-circles_2T3W1RFVXKW033343_libpanda_2021_08_02.csv'
print(f'\nWe want to download the user exploration {exploration_to_download}')
local_path_exploration = loop.run_until_complete(FileIterator.get_specific_user_exploration(exploration_to_download, clear_long_cache=True))
print(f'User exploration has been download locally and is available at: {local_path_exploration}')

# Set this exploration as the one for the file iterator
print(f'\nWe can now set the exploration to use by the file iterator')
FileIterator.set_exploration_to_use(local_path_exploration)
print(f'The exploration has been set up. The file iterator is configured, and returns when printing it: {FileIterator}')

# iterate
print(f'\nNow, you can use this iterator to work on each file and iterate over this list')
for _ in range(FileIterator.max_index):
    current_file = loop.run_until_complete(FileIterator.next())
    print(f'current file is: {current_file}')


# ------------------ clear the cache ------------------
init_cache()
init_cache(long=True)

# ------------------ close the async loop ------------------
loop.close()
