from transcription_runner import *
from pprint import pprint
import traceback


# CHANGE THESE FUNCTIONS AND VARIABLES TO WORK FOR THE CITY YOU WOULD LIKE TO HAVE CDP WORK WITH

# SCRAPER

# set_naming_conventions for the hardcoded naming conventions from City of Seattle
def set_naming_conventions(item):

    '''Ensure a string follows certain conventions.

    Arguments:

    item -- the string to be checked.
    '''

    if item[-2:] == 'VV':
        item = item[:-2]

    if item[-2:] == 'vV':
        item = item[:-2]

    if item[-1:] == 'V':
        item = item[:-1]

    if item[-1:] == 'v':
        item = item[:-1]

    if item[-1:] == 's':
        item = item[:-1] + 'a'

    return item

# scrape_seattle_channel for the path and routes provided
def scrape_seattle_channel(path, routes, prints=True):

    '''Find, collect, and generate all relevant information for a provided path and route information.

    Arguments:

    path -- the label for future files and also short name for body

    routes -- the list of url and long specific name

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # request the url and scrape the page to collect information
    r = requests.get(routes[0])
    soup = bs(r.content, 'html.parser')

    # each route has multiple videos to collect
    path_feeds = list()
    paginations = soup.find_all('div', class_='col-xs-12 col-sm-8 col-md-9')

    if prints:
        print('found', len(paginations), 'video elements for:', path)

    # for each video section find and store the video information
    for pagination in paginations:
        path_feed = dict()

        # page link
        bs_link = str(pagination.find('a')['href'])
        path_feed['link'] = bs_link

        # video source
        try:
            bs_video = str(pagination.find('a')['onclick'])
            video_end = bs_video.find('.mp4\',')
            bs_video = str(pagination.find('a')['onclick'])[26: video_end + 4]
        except:
            bs_video = ''
        path_feed['video'] = bs_video

        # agenda
        try:
            bs_agenda = str(pagination.find('div', class_='titleExcerptText').find('p').text)
            if 'Agenda: ' in bs_agenda:
                bs_agenda = bs_agenda[8:]
            path_feed['agenda'] = bs_agenda
        except:
            path_feed['agenda'] = ''

        # date published
        bs_datetime = str(pagination.find('div', class_='videoDate').text)
        converted_dt = datetime.datetime.strptime(bs_datetime, '%m/%d/%Y')
        path_feed['datetime'] = str(converted_dt)

        # body name
        path_feed['body'] = routes[1]

        # path name
        path_feed['path'] = path

        # apply naming conventions and store
        try:
            naming_splits = bs_video.split('/')
            last_splits = naming_splits[-1:][0].split('_')
            filename = path + '_' + last_splits[1][:-4]

            path_feed['naming'] = set_naming_conventions(filename)

            if 'AM' in last_splits[0]:
                path_feed['naming'] += 'AM'

            if 'PM' in last_splits[0]:
                path_feed['naming'] += 'PM'

        # no naming information could be determined
        except:
            path_feed['naming'] = ''

        # append this feed to list of feeds
        path_feeds.append(path_feed)

        if prints:
            print('constructed true link:', path_feed['naming'])

    if prints:
        print('completed feed construction for:', path)
        print('-----------------------------------------------------------')

    return path_feeds


# DATABASE PULL

# get_firebase_data for a given database head
def get_firebase_data(db_root, path):

    '''Pull all data from a database point.

    Arguments:

    database_head -- the pyrebase object where you want to pull data from.
        example: pyrebase object for 'firebase/transcript_versioning/'
    '''

    return db_root.child(path).get()


# DATABASE COMMIT

# try_catch_database_push a dataset to a database given safety constraints
def try_catch_database_push(db_root, data, wait_after_fail=600, prints=True):

    '''Push data to a database while ensuring safety and rerun

    Arguments:

    database_head -- the overall head of the database where all trees can be reached from.

    data -- the data that will be stored.

    wait_after_fail -- the time to wait before rerunning the data push if it was to fail. Default: 10 minutes (600 seconds)

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    try:
        for key in data:
            db_root.child(key).set(data[key])

    except Exception as e:
        if prints:
            print('error in database push...', e)

            if wait_after_fail >= 0:
                print('retrying in', wait_after_fail, 'seconds')
                time.sleep(wait_after_fail)
                try_catch_database_push(db_root=db_root, data=data, wait_after_fail=(wait_after_fail + 60), prints=prints)

# commit_to_firebase a combined_data store
def commit_to_firebase(data_store, db_root, prints=True):

    '''Push a combined data JSON file to firebase.

    Arguments:

    data_store -- the os file path for where the data_store created by combine_data_sources is stored.
        example: 'C:/transcription_runner/seattle/json/combined_data.json'

    database_head -- the pyrebase object where you want to pull data from.
        example: pyrebase object for 'firebase/'

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    if prints:
        print('starting storage of:', data_store)

    with open(data_store, 'r') as data_file:
        data = json.load(data_file)

    try_catch_database_push(db_root=db_root, data=data, prints=prints)

    if prints:
        print('pushed and stored data at:', db_root)
        print('---------------------------------------------------------------')


# VARIABLES AND OBJECTS

# video_routes is the seattle_channel packed_routes object
# change this to your own video routing
video_routes = {
                'briefings': ['http://www.seattlechannel.org/CouncilBriefings', 'Council Briefing'],
                'budget': ['http://www.seattlechannel.org/BudgetCommittee', 'Select Budget Committee'],
                'full': ['http://www.seattlechannel.org/FullCouncil', 'Full Council'],
                'park': ['http://www.seattlechannel.org/mayor-and-council/city-council/seattle-park-district-board', 'Select Committee on Parks Funding'],
                'transportation': ['http://www.seattlechannel.org/mayor-and-council/city-council/seattle-transportation-benefit-district', 'Select Committee on Transportation Funding'],
                'arenas': ['http://www.seattlechannel.org/mayor-and-council/city-council/select-committee-on-civic-arenas', 'Select Committee on Civic Arenas'],
                'housing': ['http://www.seattlechannel.org/mayor-and-council/city-council/select-committee-on-the-2016-seattle-housing-levy', 'Select Committee on the 2016 Seattle Housing Levy'],
                'lighting': ['http://www.seattlechannel.org/mayor-and-council/city-council/select-committee-on-the-2016-seattle-city-light-strategic-planning', 'Select Committee on the 2016 Seattle City Light Strategic Planning'],
                'finance': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-affordable-housing-neighborhoods-and-finance-committee', 'Affordable Housing, Neighborhoods, and Finance Committee'],
                'utilities': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-civil-rights-utilities-economic-development-and-arts-committee', 'Civil Rights, Utilities, Economic Development, and Arts Committee'],
                'education': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-education-equity-and-governance-committee', 'Education and Governance Committee'],
                'energy': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-energy-and-environment-committee', 'Energy and Environment Committee'],
                'communities': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-gender-equity-safe-communities-and-new-americans-committee', 'Gender Equity, Safe Communities, and New Americans Committee'],
                'public_health': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-human-services-and-public-health-committee', 'Human Services and Public Health Committee'],
                'civic_centers': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-parks-seattle-center-libraries-and-waterfront-committee', 'Parks, Seattle Center, Libraries, and Waterfront Committee'],
                'zoning': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-planning-land-use-and-zoning-committee', 'Planning, Land Use, and Zoning Committee'],
                'sustainability': ['http://www.seattlechannel.org/mayor-and-council/city-council/2016/2017-sustainability-and-transportation-committee', 'Sustainability and Transportation Committee']
}


# DATABASE CONNECTION

# database configuration and admin settings
# where I store my firebase configuration and api keys

# using the configure_keys information, initialize the firebase connection
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('C:/transcription_runner/python/cdp-sea-firebase-adminsdk.json')
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://cdp-sea.firebaseio.com/'
})

firebase_head = db.reference()
versioning_path = 'transcript_versioning/'

# the project directory where all files will be stored
project_directory = 'C:/transcription_runner/resources/'

# actual runner function call
transcription_runner(project_directory=project_directory, json_directory=(project_directory + 'stores/'), video_routes=video_routes, scraping_function=scrape_seattle_channel, log_directory=(project_directory + 'logs/'), pull_from_database=get_firebase_data, database_head=firebase_head, versioning_path=versioning_path, relevant_tfidf_storage_key='events_tfidf', commit_to_database=commit_to_firebase, delete_videos=True, delete_splits=True)
