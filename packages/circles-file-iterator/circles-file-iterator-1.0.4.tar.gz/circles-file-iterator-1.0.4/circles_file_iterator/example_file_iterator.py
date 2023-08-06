'''
--------------------------------------------------------------
                   Iterating over the files
--------------------------------------------------------------
This example file shows how to use the file iterator class. It allows 
to get files from CyVerse and treat them one by one, handling download,
caching and referencing all the available runs.

NOTE: Be sure to have configured your cache and your irods environment before 
testing these functionnalities. You can do so by using the file 'example_configuration.py's
--------------------------------------------------------------
'''

# ------------------ imports ------------------
import asyncio
from circles_file_iterator.utils.cache import init_cache
from circles_file_iterator.utils.file_iterator import FileIteratorCanGps

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


# ======================= CREATION OF THE FILE ITERATOR =======================
'''
Here, we create the file iterator object
'''

print('\n------------------------ CREATION OF THE FILE ITERATOR ------------------------\n')

FileIterator = FileIteratorCanGps()
print(f'\nThe file iterator object has been created: {FileIterator}')


# ======================= CONFIGURATION OF THE FILE ITERATOR =======================
'''
Here, we configure the file iterator object's rerference data. We set which file exploration
to use for iterating over the files. A file exploration is just a CSV file containing a list
of path to access runs on CyVerse.

For most of the cases, using only the default file explorations provided would be sufficient.
There is one "large" exploration, containing all the CSV files available on CyVerse. There is 
also a smaller one giving a few files to try the algorithm on.

If you need to add more referenced data to those exploration (different kind or more recent data),
you can look at the code example ./example_create_file_iteration.py.

Finally, this file shows how to set the before and after next functions. Those hooks are called
respectively before and after calling the next() method. In these methods, you can access the
functions and attributes of the class via self.attr_name or self.method_name.
Be sure to define the functions you set as function_name(self): ...
'''
print('\n------------------------ CONFIGURATION OF THE FILE ITERATOR ------------------------\n')

# Get Default explorations
loop.run_until_complete(FileIterator.get_default_explorations(clear_long_cache=True))
print(f'\nDefault explorations have been pulled from CyVerse and are now available locally.')

# Find the locally available explorations
available_explorations = FileIterator.find_locally_available_explorations()
print(f'\nThose explorations are: {available_explorations}')

# Set which local exploration to use for iterating over the files
# We use a large exploration with all the available runs on CyVerse
# here for the purposes of this demonstration. We will filter those out afterwards
index_of_large_file_iteration = [idx for idx, filename in enumerate(available_explorations) if 'full_exploration' in filename][0]
FileIterator.set_exploration_to_use(available_explorations[index_of_large_file_iteration])
print(f"\nThe file iterator's exploration is set. The file iterator now returns: {FileIterator}")

# Using filters
print(f"\nWe filter out those runs to only keep the ones having:\n\
        VIN=JTMB6RFV5MD010181,\n\
        date=2021-06-16")
FileIterator.filter(date='2021-06-16', vin='JTMB6RFV5MD010181')
print(f"\nWe have filtered out the referenced files in the file iterator.\nIt now returns: {FileIterator}")

# Setting hooks
def before_func(self):
    print(f'This print comes from inside of before next hook. It shows that the index is: {self.index}')

def after_func(self):
    print(f'This print comes from inside of after next hook. It shows that the index is: {self.index}')

FileIterator.set_hook_before_next(before_func)
FileIterator.set_hook_after_next(after_func)


# ======================= ITERATING OVER THE FILES =======================
'''
Now that everything is set up, we can finally present the core of what this package allows.
By calling the next() method of the file iterator, it:
- clears the temp cache
- downloads the next file in the list of available files from the file exploration
- returns the local path towards this downloaded file

For the demonstration of this file, we will simply print out the filename and not process them.

NOTE: here, we can use the file iterator on CAN/GPS file couples. For the purposes of this
explanation, we show how to do wiht or without the GPS file by setting the flag
ignore_gps_file=False or True when downloading a new file.
'''
print('\n------------------------ ITERATING OVER THE FILES ------------------------\n')

print('\nWithout downloading the GPS Files')
for _ in range(FileIterator.max_index):
    local_file_path = loop.run_until_complete(FileIterator.next(ignore_gps_file=True, verbose=True))
    # --- THIS IS WHERE YOU CAN MAKE YOUR FILE PROCESSING ---
    print(f'\nCurrent local address of the downloaded file is: {local_file_path}.\n\
        It will now be deleted before downloading the next file.')
print(f'\nThe iteration over the files (only CAN) is finished.')

FileIterator.reset()
print('\nThe File Iterator has been reset')

print('\With downloading of the GPS Files')
for _ in range(FileIterator.max_index):
    local_file_path = loop.run_until_complete(FileIterator.next(ignore_gps_file=False, verbose=True))
    # --- THIS IS WHERE YOU CAN MAKE YOUR FILE PROCESSING ---
    print(f'\nCurrent local address of the downloaded file is: {local_file_path}.\n\
        It will now be deleted before downloading the next file.')
print(f'\nThe iteration over the files (CAN+GPS) is finished.')


# ------------------ clear the cache ------------------
init_cache()
init_cache(long=True)

# ------------------ close the async loop ------------------
loop.close()
