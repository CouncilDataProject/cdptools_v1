from get_store_data import *
from pprint import pprint
import traceback

# generate_log_file function used as the default logging fucntion for cdp_runner
def generate_log_file(log_name, log_type, log_object, log_directory):

    '''Generate a log file after a block or system run.

    Arguments:

    log_name -- the actual storage name of the file to be stored. Default interaction: created and passed by the cdp_runner method.

    log_type -- the type of log desired for storage; 'block', 'system', or 'consolidated'. Default interaction: created and passed by the cdp_runner method.

    log_object -- the dictionary object to store. Default interaction: created and passed by the cdp_runner method.

    log_directory -- the directory or folder os path for where to store the log file.
    '''

    # ensure path safety
    log_directory = check_path_safety(log_directory)

    # check if the log folder exists, if not, create it
    if not os.path.exists(log_directory):
        os.mkdir(log_directory)

    # check if it is a system log
    if log_type == 'system':

        # create a consolidated log if it is
        consolidated = dict()
        consolidated['completed_feeds'] = 0
        consolidated['avg_feeds_duration'] = 0
        consolidated['completed_videos'] = 0
        consolidated['avg_videos_duration'] = 0
        consolidated['completed_audios'] = 0
        consolidated['avg_audios_duration'] = 0
        consolidated['completed_transcripts'] = 0
        consolidated['avg_transcripts_duration'] = 0
        consolidated['tfidf_duration'] = 0
        consolidated['search_duration'] = 0
        consolidated['avg_data_pull_duration'] = 0
        consolidated['avg_block_duration'] = 0

        # ethier set the most recent duration as the current duration or add the duration for later averaging
        for block in log_object:
            consolidated['system_start'] = block['system_start']
            consolidated['completed_feeds'] += block['completed_feeds']
            consolidated['avg_feeds_duration'] += block['feeds_duration']
            consolidated['completed_videos'] += block['completed_videos']
            consolidated['avg_videos_duration'] += block['videos_duration']
            consolidated['completed_audios'] += block['completed_audios']
            consolidated['avg_audios_duration'] += block['audios_duration']
            consolidated['completed_transcripts'] += block['completed_transcripts']
            consolidated['avg_transcripts_duration'] += block['transcripts_duration']
            consolidated['tfidf_duration'] = block['tfidf_duration']
            consolidated['search_duration'] = block['search_duration']
            consolidated['avg_block_duration'] += block['block_duration']
            consolidated['system_runtime'] = block['system_runtime']
            consolidated['combination_duration'] = block['combination_duration']
            consolidated['database_duration'] = block['database_duration']
            consolidated['avg_data_pull_duration'] += block['data_pull_duration']

        num_blocks = len(blocks)

        # average specific values
        consolidated['avg_feeds_duration'] = consolidated['avg_feeds_duration'] / num_blocks
        consolidated['avg_videos_duration'] = consolidated['avg_videos_duration'] / num_blocks
        consolidated['avg_audios_duration'] = consolidated['avg_audios_duration'] / num_blocks
        consolidated['avg_transcripts_duration'] = consolidated['avg_transcripts_duration'] / num_blocks
        consolidated['avg_block_duration'] = consolidated['avg_block_duration'] / num_blocks
        consolidated['avg_data_pull_duration'] = consolidated['avg_data_pull_duration'] / num_blocks

        # print the cosolidated log
        pprint(log_object)

        # generate a log with consolidated data
        log_name = 'consolidated_' + str(datetime.datetime.fromtimestamp(consolidated['system_start'])).replace(' ', '_').replace(':', '-')[:-7]
        generate_log_file(log_name=log_name, log_type='consolidated', log_object=consolidated, log_directory=log_directory)

    # store the log_object in specified path
    with open(log_directory + log_name + '.json', 'w', encoding='utf-8') as logfile:
        json.dump(log_object, logfile)

    # ensure log_file safety
    logfile.close()
    time.sleep(1)

# run_cdp function used to collect, transcribe, and store videos
def run_cdp(project_directory, json_directory, log_directory, video_routes, scraping_function, pull_from_database, database_head, versioning_head, relevant_tfidf_storage_key, commit_to_database, delete_videos=False, delete_splits=False, test_search_term='bicycle infrastructure', prints=True, block_sleep_duration=1800, run_duration=-1, logging=True):

    '''Run the backend transcription, local, and database storage system.

    Arguments:

    project_directory -- the directory or folder os path for where all created and generated non-storage (JSON) files will be stored.
        example path: 'C:/transcription_runner/seattle/'

    json_directory -- the directory or folder os path for where all created and generated storage (JSON) files will be stored.
        example path: 'C:/transcription_runner/seattle/json/'

    log_directory -- the directory or folder os path for where all created and generated log files will be stored.
        example path: 'C:/transcription_runner/seattle/logs/'

    video_routes -- the packed_routes dictionary object that contains labeling/ pathing as a each key, and a list of page url and a more specific naming target.
        formatted:
            video_routes = {
                label/ path_one: [url_one, specific_name_one],
                label/ path_two: [url_two, specific_name_two],
                ...
                label/ path_n: [url_n, specific_name_n]
            }

    scraping_function -- the function to return a completed list of information dictionaries regarding each video present in the video_routes provided.
        example function: scrape_seattle_channel in get_store_data.py

    pull_from_database -- the function used to retrieve data from a database storage system.
        example function: get_firebase_data in get_store_data.py

    database_head -- the part/ path of the database you would like to pull from and store with.

    relevant_tfidf_storage_key -- the key/ path for navigating the database information to retrieve specifically the tfidf information.

    commit_to_database -- the function used to push data from the local JSON storage to a database.
        example function: commit_to_firebase in get_store_data.py

    delete_videos -- boolean value to determine to keep or delete videos after audio has been stripped. Default: False (keep videos)

    delete_splits -- boolean value to determine to keep or delete audio splits after transcript has been created. Default: False (keep audio splits)

    test_search_term -- string value to act as a test search word or phrase to calculate search time of the tfidf tree. Default: 'bicycle infrastructure'

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)

    block_sleep_duration -- integer value for time in seconds for how long the system should wait after checking for need videos. Default: 1800 (0.5 hours)

    run_duration -- integer value for time in seconds for how long the system should run for. Default: -1s (endless)

    logging -- boolean value to determine if the system should create log files after each block run and system run. Default: True (create log files)
    '''

    # ensure safety of the entire run
    try:

        # ensure safety of paths
        project_directory = check_path_safety(project_directory)
        log_directory = check_path_safety(log_directory)

        # create system logging information
        system_start = time.time()
        time_elapsed = 0

        # create blocks list for logging information
        blocks = list()

        # check to see if the runner should continue
        while (time_elapsed + block_sleep_duration) <= run_duration or run_duration == -1:

            # create block logging information
            block_start = time.time()
            block = dict()
            block['system_start'] = system_start
            block['block_start'] = block_start

            # # @RUN
            # # Run for video feeds
            # feeds_start = time.time()
            # noNewFeedsAvailable = True
            # block['completed_feeds'] = 0

            # while (noNewFeedsAvailable):
            #     feed_results = get_video_feeds(packed_routes=video_routes, storage_directory=json_directory, scraping_function=scraping_function, prints=prints)

            #     block['completed_feeds'] = len(feed_results['feeds'])
            #     noNewFeedsAvailable = not feed_results['difference']

            #     time_elapsed = time.time() - system_start

            #     # sleep the system if it wont overflow into system downtime
            #     if (((time_elapsed + block_sleep_duration) <= run_duration) or (run_duration == -1) or (feed_results['difference'])):
            #         print('Collecting feeds again in:', (float(block_sleep_duration) / 60.0 / 60.0), 'HOURS...')
            #         time.sleep(block_sleep_duration)

            # feeds_duration = time.time() - feeds_start
            # block['feeds_duration'] = (float(feeds_duration) / 60.0 / 60.0)

            # # @RUN
            # # Run for mass video collection
            # videos_start = time.time()
            # block['completed_videos'] = get_video_sources(objects_file=(json_directory + 'video_feeds.json'), storage_directory=(project_directory + 'video/'), throughput_directory=(project_directory + 'audio/'), prints=prints)
            # videos_duration = time.time() - videos_start

            # block['videos_duration'] = (float(videos_duration) / 60.0 / 60.0)

            # # @RUN
            # # Run for mass audio stripping
            # audios_start = time.time()
            # block['completed_audios'] = strip_audio_from_directory(video_directory=(project_directory + 'video/'), audio_directory=(project_directory + 'audio/'), delete_videos=delete_videos, prints=prints)
            # audios_duration = time.time() - audios_start

            # block['audios_duration'] = (float(audios_duration) / 60.0 / 60.0)

            # # @RUN
            # # Run for mass transcripts
            # transcripts_start = time.time()
            # block['completed_transcripts'] = generate_transcripts_from_directory(audio_directory=(project_directory + 'audio/'), transcripts_directory=(project_directory + 'transcripts/'), ignore_files='C:/Users/jmax825/Desktop/transcription_runner/python/ignore_files.json', delete_splits=delete_splits, prints=prints)
            # transcripts_duration = time.time() - transcripts_start

            # block['transcripts_duration'] = (float(transcripts_duration) / 60.0 / 60.0)

            # @RUN
            # Run for tfidf saftey
            data_pull_start = time.time()
            prior_stored_data = pull_from_database(database_head=versioning_head)
            data_pull_duration = time.time() - data_pull_start

            block['data_pull_duration'] = (float(data_pull_duration) / 60.0 / 60.0)

            for transcript in prior_stored_data.each():
                print(transcript.key())

            # # @RUN
            # # Run for mass tfidf
            # tfidf_start = time.time()
            # if (type(prior_stored_data) is collections.OrderedDict) or (type(prior_stored_data) is dict):
            #     generate_tfidf_from_directory(transcript_directory=(project_directory + 'transcripts/'), storage_directory=json_directory, stored_versions=prior_stored_data, prints=prints)
            # else:
            #     generate_tfidf_from_directory(transcript_directory=(project_directory + 'transcripts/'), storage_directory=json_directory, stored_versions=None, prints=prints)
            # tfidf_duration = time.time() - tfidf_start

            # block['tfidf_duration'] = (float(tfidf_duration) / 60.0 / 60.0)

        #     # @RUN
        #     # Run for testing speed of search
        #     search_start = time.time()
        #     if prints:
        #         pprint(predict_relevancy(search=test_search_term, tfidf_store=(json_directory + 'tfidf.json')))
        #     else:
        #         predict_relevancy(search=test_search_term, tfidf_store=(json_directory + 'tfidf.json'))

        #     print('-------------------------------------------------------')
        #     search_duration = time.time() - search_start

        #     block['search_duration'] = (float(search_duration) / 60.0 / 60.0)

        #     # @RUN
        #     # Run for data combination
        #     combination_start = time.time()
        #     combine_data_sources(feeds_store=(json_directory + 'video_feeds.json'), tfidf_store=(json_directory + 'tfidf.json'), versioning_store=(json_directory + 'events_versioning.json'), storage_directory=json_directory, prints=prints)
        #     combination_duration = time.time() - combination_start

        #     block['combination_duration'] = (float(combination_duration) / 60.0 / 60.0)

        #     # @RUN
        #     # Run for database storage
        #     database_start = time.time()
        #     commit_to_database(data_store=(json_directory + 'combined_data.json'), database_head=database_head, prints=prints)
        #     database_duration = time.time() - database_start

        #     block['database_duration'] = (float(database_duration) / 60.0 / 60.0)

        #     block_duration = time.time() - block_start
        #     block['block_duration'] = block_duration

        #     time_elapsed = time.time() - system_start
        #     block['system_runtime'] = time_elapsed

        #     # check logging to log the block information
        #     if logging:
        #         log_name = 'block_' + str(datetime.datetime.fromtimestamp(block_start)).replace(' ', '_').replace(':', '-')[:-7]
        #         generate_log_file(log_name=log_name, log_type='block', log_object=block, log_directory=log_directory)

        #     # append the block to system log
        #     blocks.append(block)

        # # check logging to log the system information
        # if logging:
        #     log_name = 'system_' + str(datetime.datetime.fromtimestamp(system_start)).replace(' ', '_').replace(':', '-')[:-7]
        #     generate_log_file(log_name=log_name, log_type='system', log_object=blocks, log_directory=log_directory)

        # # return the basic block information
        # return blocks

    # print any exception that occurs and stop the run
    except Exception as e:
        print('---------------------------------------------------------------')
        print('---------------------- ENCOUNTERED ERROR ----------------------')
        print('---------------------------------------------------------------')
        return traceback.print_exc()

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
# where I store my firebase (pyrebase) configuration and api keys
from configure_keys import *

# using the configure_keys information, initialize the pyrebase connection
import pyrebase
firebase = pyrebase.initialize_app(pyrebase_config)
pyrebase_head = firebase.database()
pyrebase_versioning = pyrebase_head.child('transcript_versioning')

# the project directory where all files will be stored
project_directory = 'C:/Users/jmax825/Desktop/transcription_runner/resources/'

# actual runner function call
run_cdp(project_directory=project_directory, json_directory=(project_directory + 'stores/'), video_routes=video_routes, scraping_function=scrape_seattle_channel, log_directory=(project_directory + 'logs/'), pull_from_database=get_firebase_data, database_head=pyrebase_head, versioning_head=pyrebase_versioning, relevant_tfidf_storage_key='events_tfidf', commit_to_database=commit_to_firebase, delete_videos=True, delete_splits=True)
