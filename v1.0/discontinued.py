# ABANDONED

# DATA GRABBING

# get_stored_data
#   path: the path from the database origin
#   return_data: boolean true or false for if to return the actual values stored or the database object
def get_stored_data(path, return_data=True):

    # get a focus target
    focus = db

    # split the path given by the user for child function
    path = path.split('/')

    # navigate to target data
    for part in path:
        if part != '':
            focus = focus.child(part)

    # found the target return data desired
    if return_data:
        return focus.get().val()
    else:
        return focus.get()

# get_local_data for a dictionary of packed_routes
#   packed_route must contain:
#       path:           this will be the overarching body for the database or included in the filename
#       url:            the legistar url to pull data from
#       storage key:    the key that will be used to store an item in the database
#       cleaning_func:  a function that will be used to clean the data
#
#   packed_route formatted:
#       '{ path : [ url, storage key, cleaning_func ] }'
#
#   os_path: the directory path where the json data can be found
def get_local_data(packed_routes, os_path, prints=True):

    # create unpacked_data dictionary
    unpacked_data = dict()

    # for each path and packed_route
    for path, routes in packed_routes.items():

        # open the locally stored json
        with open(os_path + '_' + path + '.json', 'r', encoding='utf-8') as data_file:
            local_data = json.load(data_file)

        data_file.close()
        time.sleep(2)

        if prints:
            pprint(local_data)
            print('-----------------------------------------------------------')

        # store the retrieved data
        unpacked_data[path] = local_data

    # return the data for manipulation
    return unpacked_data

# LEGISTAR
def clean_time_data(item):

    try:
        stored_time = item['EventTime'].split(':')

        stored_min = stored_time[1].split(' ')

        calc_hour = float(stored_time[0])
        calc_minutes = float(stored_min[0]) / 60.0
        add_hours = 0
        if stored_min[1] == 'PM':
            add_hours += 12

        calc_time = (calc_hour + add_hours + calc_minutes)

        item['EventCalculatedTime'] = calc_time

    except:
        item['EventCalculatedTime'] = 24.01

    return item

# clean_events_data for an event item
#   item: the event unique item returned from the legistar events api
#
#   item must contain:
#       EventLocation: the location of where the event took place
def clean_events_data(item):

    # create a storage time attribute
    current_dt = datetime.datetime.now()
    item['EventStoredDatetime'] = str(current_dt)

    # reconstruct the EventLocation attribute
    item['EventLocation'] = item['EventLocation'].replace('\r', '').replace('\n', ', ')

    return item

# clean_bodies_data for a body item
#   item: the body unique item returned from legistar bodies api
def clean_bodies_data(item):

    # create a storage time attribute
    current_dt = datetime.datetime.now()
    item['BodyStoredDatetime'] = str(current_dt)

    return item

# get_all_data for a dictionary of packed routes
#   packed_route must contain:
#       path:           this will be the overarching body for the database or included in the filename
#       url:            the legistar url to pull data from
#       storage key:    the key that will be used to store an item in the database
#       cleaning_func:  a function that will be used to clean the data
#
#   packed_route formatted:
#       '{ path : [ url, storage key, cleaning_func ] }'
def get_all_data(packed_routes, storage_directory, prints=True):

    # ensure storage safety
    check_path_safety(storage_directory)

    # return object
    stored_data = dict()

    # for each path and packed_route
    for path, routes in packed_routes.items():
        if prints:
            print('getting data from:', routes[0])
            print('-----------------------------------------------------------')

        # request the url and store the data in json
        r = requests.get(routes[0])
        r = r.json()

        # # check output target
        # if not toLocal:
        #     for item in r:
        #         if prints:
        #             print('working on:', item)
        #
        #         # find the storage key
        #         store_id = item[routes[1]]
        #         del item[routes[1]]
        #
        #         # clean data
        #         item = routes[2](item)
        #
        #         if prints:
        #             print('completed:', item)
        #
        #         # store the data in the database
        #         db.child(path).child(store_id).set(item)
        #
        #         if prints:
        #             print('stored:', path, store_id)
        #             print('-------------------------------------------------------')

        # to local

        # clean data
        cleaned_r = list()
        for item in r:
            item = routes[2](item)
            cleaned_r.append(item)

        storage_path = storage_directory + 'local_store_' + path + '.json'

        # store data locally
        with open(storage_path, 'w', encoding='utf-8') as outfile:
            json.dump(cleaned_r, outfile)

        outfile.close()
        time.sleep(2)

        if prints:
            print('stored', path, 'at:\t', storage_path)

        stored_data[path] = cleaned_r

    return stored_data

def get_data_by_routed(packed_routes, storage_directory, prints=True):

    # ensure storage safety
    check_path_safety(storage_directory)

    # return object
    stored_data = dict()

    # for each path and packed_route
    for path, routes in packed_routes.items():
        if prints:
            print('getting data from:', routes[0])
            print('-----------------------------------------------------------')

        # request the url and store the data in json
        r = requests.get(routes[0])
        r = r.json()

        # clean data
        cleaned_r = dict()
        for item in r:
            item = routes[2](item)
            item = routes[4](item)

            try:
                cleaned_r[item[routes[6]]][item[routes[3]]].append(item)

            except:

                try:
                    cleaned_r[item[routes[6]]][item[routes[3]]] = list()
                    cleaned_r[item[routes[6]]][item[routes[3]]].append(item)

                except:
                    cleaned_r[item[routes[6]]] = dict()
                    cleaned_r[item[routes[6]]][item[routes[3]]] = list()
                    cleaned_r[item[routes[6]]][item[routes[3]]].append(item)

        sorted_r = dict()
        for key, data in cleaned_r.items():

            sorted_r[key] = dict()

            for sub_key, sub_data in data.items():
                sorted_r[key][sub_key] = sorted(sub_data, key=lambda x: x[routes[5]])

        storage_path = storage_directory + 'local_store_' + path + '_by_' + routes[3] + '.json'

        # store data locally
        with open(storage_path, 'w', encoding='utf-8') as outfile:
            json.dump(sorted_r, outfile)

        outfile.close()
        time.sleep(2)

        if prints:
            print('stored', path, 'at:\t', storage_path)

        stored_data[path] = sorted_r

    return stored_data

# get_test_data for url
#   url: the legistar url to pull data from
def get_test_data(url, prints=True):

    # get data from url
    r = requests.get(url)
    r = r.json()

    if prints:
        pprint(r)

    # return json for manipulation
    return r

def apply_naming_conventions_to_routed_legistar_data(data_path, rewrite=True):

    with open(data_path, 'r') as data_file:
        data = json.load(data_file)

    data_file.close()

    characters = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for key, datum in data.items():

        for sub_key, sub_datum in datum.items():

            datum_length = len(sub_datum)

            if datum_length == 1:

                sub_datum[0]['NamingConvention'] = ''

            else:

                time_period_one = 'AM' in sub_datum[0]['EventTime']
                time_period_two = 'AM' in sub_datum[1]['EventTime']

                if time_period_one != time_period_two and datum_length == 2:
                    sub_datum[0]['NamingConvention'] = 'AM'
                    sub_datum[1]['NamingConvention'] = 'PM'

                else:

                    for i in range(datum_length):
                        sub_datum[i]['NamingConvention'] = characters[i]

    if rewrite:
        os.remove(data_path)

        with open(data_path, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile)

        outfile.close()

    return data

def fix_video_feeds(storage_path):

    with open(storage_path, 'r') as feeds_file:
        feeds_data = json.load(feeds_file)

    feeds_file.close()
    time.sleep(1)

    os.remove(storage_path)

    for feed in feeds_data:
        converted_dt = datetime.datetime.strptime(feed['datetime'], '%m/%d/%Y')
        feed['datetime'] = str(converted_dt)

    with open(storage_path, 'w', encoding='utf-8') as feeds_file:
        json.dump(feeds_data, feeds_file)

    feeds_file.close()

    return feeds_data

def fix_video_feeds_naming(storage_path):
    with open(storage_path, 'r') as feeds_file:
        feeds_data = json.load(feeds_file)

    feeds_file.close()
    time.sleep(1)

    os.remove(storage_path)

    for feed in feeds_data:
        try:
            naming_splits = feed['video'].split('/')
            last_splits = naming_splits[-1:][0].split('_')
            filename = feed['path'] + '_' + last_splits[1][:-4]

            feed['naming'] = video_to_audio_rename(filename)

            if 'AM' in last_splits[0]:
                feed['naming'] += 'AM'

            if 'PM' in last_splits[0]:
                feed['naming'] += 'PM'

        except:
            feed['naming'] = ''

    with open(storage_path, 'w', encoding='utf-8') as feeds_file:
        json.dump(feeds_data, feeds_file)

    feeds_file.close()

    return feeds_data

# get_future_event_dates
#
# not needed for searching relevancy of videos/ events/ meetings
#
# data = get_local( { 'bodies': all_routes['bodies'] } , prints=False)
#
# for key, datum in data.items():
#     for item in datum:
#         body_events = get_test_data('http://webapi.legistar.com/v1/seattle/EventDates/' + str(item['BodyId']) + '?FutureDatesOnly=true', prints=False)
#         print(item['BodyName'], body_events)
