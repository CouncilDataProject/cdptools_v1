import requests
import subprocess
import shutil
from bs4 import BeautifulSoup as bs
import json
import datetime
import time
import speech_recognition as sr
import re
import os
from pydub import AudioSegment
import math
import sys
import Levenshtein
import collections

# GENERAL

# check_path_safety to ensure paths end with '/'
def check_path_safety(path):

    '''Ensure that a folder/ directory path is complete.

    Arguments:

    path -- the directory or folder os path to check if the path is complete.
        example: 'C:/transcription_runner/seattle/'
    '''

    if '/' == path[:1]:
        path = path[1:]

    if '/' != path[-1:]:
        path += '/'

    return path

# clean_video_filename for a video file
def clean_video_filename(item):

    '''Ensure that a string doesn't contain spaces.

    Arguments:

    item -- string to be checked for spaces
    '''

    # check filename for spaces:
    if ' ' in item:

        # replace the spaces with underscore
        item = item.replace(' ', '_')

    return item

# clean_audio_filename for an audio file
def clean_audio_filename(item):

    '''Ensure a string is safe to use.

    Arguments:

    item -- string to be checked
    '''

    return item

# video_to_audio_rename with '.wav'
def video_to_audio_rename(video_in):

    '''Convert a video filename to a .wav file.

    Arguments:

    video_in -- string filename with filetype ending to be converted to '.wav'
        example: 'transporation_112315.mp4'
    '''

    return video_in[:-4] + '.wav'

# name_transcription with '.txt'
def name_transcription(audio_label):

    '''Convert an audi filename to a .txt file.

    Arguments:

    audio_label -- string filename with filetype ending to be converted to '.txt'
        example: 'transporation_112315.wav'
    '''

    return audio_label[:-4] + '.txt'

# rename_files for an os directory or folder
def rename_files(directory, cleaning_func):

    '''Rename all files in the given directory using the provided cleaning function.

    Arguments:

    directory -- the string path or os folder to be cleaned
        example: 'C:/transcription_runner/seattle/video/'

    cleaning_func -- the function to clean each individual file name in the directory
    '''

    # ensure path safety
    directory = check_path_safety(directory)

    # get the current working directory for comparison
    cwd = os.getcwd()

    # check if the path is in the current working directory
    if directory not in cwd:

        # update the directory to match path
        os.chdir(directory)

    # for each file run the cleaning_func
    for filename in os.listdir():
        if os.path.isfile(directory + filename):
            os.rename(filename, cleaning_func(filename))

# progress print function
def progress(count, total, status=''):

    '''Print a progress bar to the console.

    Credit: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    '''

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

# VIDEO

# get_video_feeds for a dictionary of packed routes
def get_video_feeds(packed_routes, storage_directory, scraping_function, prints=True):

    '''Get all video feed information from a provided packed_routes.

    Arguments:

    packed_routes -- the dictionary of video information to collect.
        contains:
            path:           the overaching body for the database and filename pathing
            url:            the page/ or api collection point to gather information from regarding the specified path
            specific_name:  the longer more specific name for additional detail and possible later connection

        formatted:
            video_routes = {
                path_one: [url_one, specific_name_one],
                path_two: [url_two, specific_name_two],
                ...
                path_n: [url_n, specific_name_n]
            }

    storage_directory -- the directory or folder os path for where the JSON file will be stored.
        example: 'C:/transcription_runner/seattle/json/'

    scraping_function -- the function to collect the information which uses each individual video_route contained in video_routes.
        must return:
            list of path_feeds...

            path_feed must contain:
                video: the actual video file server path. Ends in '.mp4'
                    example: 'http://video.seattle.gov:8080/media/council/transben_112315V.mp4'
                naming: how to name each associated file.
                    example: 'transporation_112315'

                any other information you would like to collect.
                    example: link to where to view the video on official webpage, datetime of video creation, the associated body, etc.

        formatted:
            path_feeds = [
                path_feed_one, path_feed_two, ... , path_feed_n
            ]

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # ensure storage safety
    storage_directory = check_path_safety(storage_directory)

    # create empty list to store video information
    constructed_feeds = list()

    feed_difference = False

    # for each path and packed_route
    for path, routes in packed_routes.items():
        # if prints:
        #     print('collecting feeds for:\t', path)

        # attach the found feeds to the storage list
        for item in scraping_function(path=clean_video_filename(path), routes=routes, prints=prints):
            constructed_feeds.append(item)

    # if prints:
    #     print('----------------------------------------------------------------------------------------')

    # store the found feeds locally
    previous_feeds = list()

    # add to previous store
    try:

        # read the previous store
        with open(storage_directory + 'video_feeds.json', 'r', encoding='utf-8') as previous_store:
            temp = previous_store.read()

        # safety
        previous_store.close()
        time.sleep(2)

        # load the store data
        previous_feeds = json.loads(temp)

        previous_length = len(previous_feeds)

        if prints:
            print('previous store length:\t', previous_length)

        previous_videos = list()

        for previous_feed in previous_feeds:
            previous_videos.append(previous_feed['video'])

        # only add new items
        for new_feed in constructed_feeds:

            if new_feed['video'] not in previous_videos:
                previous_feeds.append(new_feed)

        if prints:
            print('new store length:\t', len(previous_feeds))
            # print('----------------------------------------------------------------------------------------')

        feed_difference = (previous_length != len(previous_feeds))

        # set the new feeds appended to old
        constructed_feeds = previous_feeds

    # no previous store found, create new
    except Exception as e:
        print(e)

        feed_difference = True

        if prints:
            print('no previous storage found...')

    if not os.path.exists(storage_directory):
        os.mkdir(storage_directory)

    with open(storage_directory + 'video_feeds.json', 'w', encoding='utf-8') as outfile:
        json.dump(constructed_feeds, outfile)

    # safety
    outfile.close()
    time.sleep(2)

    # return the data for manipulation
    returnObject = {'feeds': constructed_feeds, 'difference': feed_difference}

    return returnObject

# get_video_sources for a json/ dictionary of video information
def get_video_sources(objects_file, storage_directory, throughput_directory, prints=True):

    '''Get all video source files from the previously stored video_feeds associated JSON file.

    Arguments:

    objects_file -- the os path to the stored video_feed collected information JSON file.
        created by: get_video_feeds function
        example: 'C:/transcription_runner/seattle/json/video_feeds.json'

    storage_directory -- the directory or folder os path for where the videos will be stored.
        example: 'C:/transcription_runner/seattle/video/'

    throughput_directory -- the directory or folder os path for where audio will be stored if the process were to continue.
        example: 'C:/transcription_runner/seattle/audio/'

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # ensure path safety
    storage_directory = check_path_safety(storage_directory)
    throughput_directory = check_path_safety(throughput_directory)

    # ensure directory safety
    if not os.path.exists(storage_directory):
        os.mkdir(storage_directory)

    # read the video_feeds
    with open(objects_file, 'r', encoding='utf-8') as objects_:
        objects = json.load(objects_)

    # ensure safe close
    objects_.close()

    completed_stores = 0

    prior_check_dict = {'prior audio': 0, 'prior video': 0, 'collected': 0}

    # for each dictionary in list of data
    for datum in objects:

        # check that a video source exists
        if datum['video'] != '' and datum['naming'] != '':

            # ensure safety against errors
            try:

                # check it the video exists
                if os.path.exists(throughput_directory + datum['naming'] + '.wav'):
                    prior_check_dict['prior audio'] += 1
                    # if prints:
                    #     print('audio stored previously, skipping', datum['video'], 'collection...')

                elif os.path.exists(storage_directory + datum['naming'] + '.mp4'):
                    prior_check_dict['prior video'] += 1
                    # if prints:
                    #     print('video stored previously, skipping', datum['video'], 'collection...')

                # video must need to be downloaded
                else:
                    prior_check_dict['collected'] += 1

                    if prints:
                        print('collecting:', datum['video'])

                    # request the video source and store the file
                    r = requests.get(datum['video'], stream=True)
                    if r.status_code == 200:
                        with open((storage_directory + datum['naming'] + '.mp4'), 'wb') as mp4_out:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, mp4_out)

                            completed_stores += 1

                        mp4_out.close()
                        time.sleep(2)

            # print the exception for error handling
            except Exception as e:

                print(e)

    if prints:
        print('completed all video collections')
        print(prior_check_dict)
        print('----------------------------------------------------------------------------------------')

    return completed_stores

# AUDIO

# strip_audio using subprocess to run ffmpeg
def strip_audio(video_dir, audio_dir, video_in, audio_out):

    '''Strip the audio from a video file and store the newly created audio file.

    Arguments:

    video_dir -- the directory or folder os path for where the videos are stored.
        example: 'C:/transcription_runner/seattle/video/'

    audio_dir -- the directory or folder os path for where the audio will be stored.
        example: 'C:/transcription_runner/seattle/audio/'

    video_in -- the filename for the file in the video_dir to be stripped of audio.
        example: 'transporation_112315.mp4'

    audio_out -- the name given to the stripped audio to be stored.
        example: 'transporation_112315.wav'
    '''

    command = 'ffmpeg -hide_banner -loglevel warning -i '

    command += video_dir
    command += video_in
    command += ' -ab 160k -ac 2 -ar 44100 -vn '
    command += audio_dir
    command += audio_out

    subprocess.call(command, shell=True)

# strip_audio_from_directory for given directory
def strip_audio_from_directory(video_directory, audio_directory, audio_directory_cleaning_function=clean_audio_filename, video_directory_cleaning_function=clean_video_filename, naming_function=video_to_audio_rename, delete_videos=False, prints=True):

    '''Strip the audio from a video file directory and store the striped audio in an audio file directory.

    Arguments:

    video_directory -- the directory or folder os path for where the videos are stored.
        example: 'C:/transcription_runner/seattle/video/'

    audio_directory -- the directory or folder os path for where the audio will be stored.
        example: 'C:/transcription_runner/seattle/audio/'

    audio_directory_cleaning_function -- a cleaning function for ensuring files in the audio_directory follow naming conventions as a whole.

    video_directory_cleaning_function -- a cleaning function for ensuring files in the video_directory follow naming conventions as a whole.

    naming_function -- a specific function to convert a video file name to an audio file name.

    delete_videos -- boolean value to determine to keep or delete videos after audio has been stripped. Default: False (keep videos)

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # check_path_safety for all path variables
    video_directory = check_path_safety(video_directory)
    audio_directory = check_path_safety(audio_directory)

    if not os.path.exists(audio_directory):
        os.mkdir(audio_directory)

    # ensure file naming conventions follow same pattern
    rename_files(directory=audio_directory, cleaning_func=audio_directory_cleaning_function)
    rename_files(directory=video_directory, cleaning_func=video_directory_cleaning_function)

    # set working directory to the video_dir
    os.chdir(video_directory)

    if prints:
        print('set cwd to:', os.getcwd())

    completed_strips = 0

    # for each video in the found directory
    for video_file in os.listdir():

        # construct the audio file name
        audio_out_label = naming_function(video_file)

        # ensure safety against errors
        try:

            # check if the audio exists
            if os.path.exists(audio_directory + audio_out_label):
                if prints:
                    print('audio stored previously, skipping', video_file, 'strip...')

            # audio needs to be stripped
            else:

                if prints:
                    print('stripping audio using:', video_directory, audio_directory, video_file, audio_out_label)

                # strip the audio
                strip_audio(video_directory, audio_directory, video_file, audio_out_label)

                completed_strips += 1

        except Exception as e:

            print(e)

        # ensure safety against already removed files
        try:

            # check if to delete
            if delete_videos:

                if prints:
                    print('delete_video is marked as True, deleting original video file for:', audio_out_label)

                os.remove(video_directory + video_file)

        # file already removed
        except FileNotFoundError as e:

            if prints:
                print('file already removed')

    if prints:
        print('completed audio stripping for:', video_directory)
        print('----------------------------------------------------------------------------------------')

    return completed_strips

# name_audio_splits for an audio directory
def name_audio_splits(audio_directory, output_directory, audio_splits):

    '''Construct a dictionary of names to audio split files.

    Arguments:

    audio_directory -- the directory or folder os path for where the audio will be stored.
        example: 'C:/transcription_runner/seattle/audio/'

    output_directory -- the directory or folder os path for where the audio splits will be stored.
        example: 'C:/transcription_runner/seattle/audio/splits/'

    audio_splits -- the list of audio splits to be named.
    '''

    # create empty dict for labels and associated split files
    split_names = dict()

    # simple name by index value
    for i in range(len(audio_splits)):
        split_names[audio_directory + output_directory + str(i) + '.wav'] = audio_splits[i]

    # return dict
    return split_names

# split_audio_into_parts for an audio_directory and a targetted audio file
def split_audio_into_parts(audio_directory, transcripts_directory, audio_file, naming_function=name_audio_splits, split_length=18000, delete_splits=False, override_splits=False, splits_directory='splits/', prints=True):

    '''Create slices of an audio file.

    Arguments:

    audio_directory -- the directory or folder os path for where the audio will be stored.
        example: 'C:/transcription_runner/seattle/audio/'

    transcripts_directory -- the directory of folder os path for where the transcript will be stored.
        example: 'C:/transcription_runner/seattle/transcripts/'

    audio_file -- the specific audio file to be split into smaller slices.
        example: 'transporation_112315.wav'

    naming_function -- the audio split naming function.

    split_length -- integer value time in ms for length of each audio split. Default: 18000ms (18 seconds)

    delete_splits -- boolean value to determine if splits should be removed after transcription process. Default: False (don't delete audio splits)

    override_splits -- boolean value to determine if previous audio splits created should be overwritten. Default: False (don't rewrite audio splits)

    splits_directory -- string os path attachment for where to store the created splits. Default: 'splits/'
        example: 'splits/'

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # check_path_safety for all pathing variables
    audio_directory = check_path_safety(audio_directory)
    splits_directory = check_path_safety(splits_directory)

    # create the subfolder label for checking and future storage
    subfolder = check_path_safety(splits_directory + audio_file[:-4])

    # ensure the splits directory exists
    if not os.path.exists(audio_directory + splits_directory):
        os.mkdir(audio_directory + splits_directory)

    # create the specific store_directory for checking and future storage
    store_directory = check_path_safety(audio_directory + subfolder)

    # if the transcript exists already, no need to create splits unless directly overriden
    if os.path.exists(transcripts_directory + audio_file[:-4] + '.txt') and delete_splits:

        # if prints:
        #     print('transcript exists, and delete_splits marked true, no need to create splits...')

        return store_directory

    # check if the splits already exist
    if os.path.exists(store_directory):

        if prints:
            print('audio splits for:\t', audio_file, 'already exists...')

        # they existed, return the store_directory path
        return store_directory

    if prints:
        print('creating audio splits for:\t', audio_directory + audio_file)

    # create an AudioSegment from full audio file
    audio_as_segment = AudioSegment.from_wav(audio_directory + audio_file)

    if prints:
        print('audio was stored as segment...')

    # create the list of smaller audio segments according to split_length
    audio_segments = [audio_as_segment[i:i+split_length] for i in range(0, len(audio_as_segment), split_length)]

    if prints:
        print('audio splits created successfully...')

    # combine the audio segments with their naming conventions, for now, this is forced
    split_names = naming_function(audio_directory=audio_directory, output_directory=subfolder, audio_splits=audio_segments)

    if prints:
        print('audio splits assigned names based off of', str(naming_function) + '...')

    # create the storage directory
    os.mkdir(store_directory)

    total_s = len(audio_segments)
    i = 0

    # store each split AudioSegment under its associated label
    for output_path, split in split_names.items():
        split.export(output_path, format='wav')

        if prints:
            progress(count=i, total=total_s)

        i += 1

    if prints:
        print('')

    if prints:
        print('created audio splits for:\t', audio_file, '\t||\t', store_directory)

    # return the store_directory path
    return store_directory

# TRANSCRIPTION

#generate_transcript_from_audio_splits for a directory of audio split files
def generate_transcript_from_audio_splits(audio_directory, transcripts_directory, filename, naming_function=name_transcription, prints=True):

    '''Generate a transcript using audio slices.

    Arguments:

    audio_directory -- the directory or folder os path for where the audio are stored.
        example: 'C:/transcription_runner/seattle/audio/splits/transporation_112315/'

    transcripts_directory -- the directory or folder os path for where the transcripts will be stored.
        example: 'C:/transcription_runner/seattle/transcripts/'

    filename -- the specific file to be transcribed.
        example: 'transporation_112315.wav'

    naming_function -- the function to convert the audio filename to a transcript filename. Default: name_transcription

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # check_path_safety for audio splits directory
    audio_directory = check_path_safety(audio_directory)
    transcripts_directory = check_path_safety(transcripts_directory)

    # construct a transcribed_name for checking and future processing
    transcribed_name = name_transcription(transcripts_directory + filename)

    # check if the transcription already exists
    if os.path.exists(transcribed_name):
        # print('transcript for:\t', transcribed_name, 'already exists...')
        return 'existed, not opened'

    if prints:
        print('starting transcription from audio splits in:\t', audio_directory)

    # no file found, start transcription engine
    r = sr.Recognizer()

    # ensure the current working directory is the audio_directory
    os.chdir(audio_directory)

    # start transcription string
    transcript = ''

    # find audio splits
    splits = os.listdir()

    if prints:
        print('found', len(splits), 'splits in directory to transcribe from...')

    total_s = len(splits)

    # for each split (assuming standard splits naming)
    for i in range(total_s):

        # follow google transcription engine process
        with sr.AudioFile(audio_directory + str(i) + '.wav') as source:

            # record audio
            audio = r.record(source)

            try:

                # try to transcribe the recording
                g_transcript = r.recognize_google(audio)

                # add successful transcription to cumulative transcript
                transcript += ' ' + g_transcript

            # no reason to stop transcription process with UVE, but alert user of error
            except sr.UnknownValueError as e:
                pass

            # major error, stop the engine and return
            except sr.RequestError as e:
                return 'Could not request results from Google Speech...', e

            if prints:
                progress(count=i, total=total_s)

    if prints:
        print('')

    # transcription fence post fix
    transcript = transcript[1:]

    if not os.path.exists(transcripts_directory):
        os.mkdir(transcripts_directory)

    # create and store the transcription in a file
    with open(transcribed_name , 'w', encoding='utf-8') as outfile:
        outfile.write(transcript)

    outfile.close()
    time.sleep(2)

    if prints:
        print('stored transcription at:\t', transcribed_name)

    if prints:
        print('created transcript for:\t', transcribed_name, '\t||\t',  transcript[:20] + '...')

    # return the transcript string
    return transcript

# generate_transcripts_for_directory for a directory of audio files
def generate_transcripts_from_directory(audio_directory, transcripts_directory, transcript_naming_function=name_transcription, audio_splits_directory='splits/', ignore_files=None, delete_originals=False, delete_splits=False, prints=True):

    '''Generate transcripts for all audio files in a directory.

    Arguments:

    audio_directory -- the directory or folder os path for where the audio are stored.
        example: 'C:/transcription_runner/seattle/audio/'

    transcripts_directory -- the directory or folder os path for where the transcripts will be stored.
        example: 'C:/transcription_runner/seattle/transcripts/'

    transcript_naming_function -- the function to convert the audio filename to a transcript filename. Default: name_transcription

    audio_splits_directory -- the os path attachment for where to store audio splits created. Default: 'splits/'
        example: 'splits/'

    delete_originals -- boolean value to determine if original audio files should be removed after transcription process. Default: False (keep audio files)

    delete_splits -- boolean value to determine if audio split files should be removed after transcription process. Default: False (keep audio split files)

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # check_path_safety for project
    audio_directory = check_path_safety(audio_directory)
    audio_splits_directory = check_path_safety(audio_splits_directory)
    transcripts_directory = check_path_safety(transcripts_directory)

    # after check, set the directory to match
    os.chdir(audio_directory)

    if ignore_files is not None:
        if os.path.exists(ignore_files):
            with open(ignore_files, 'r') as ignore_files_file:
                ignore_files = json.load(ignore_files_file)

    if prints:
        print('starting work for', audio_directory, '...')
        print('----------------------------------------------------------------------------------------')

    completed_transcripts = 0

    # for all .wav files create audio splits and generate transcript
    for filename in os.listdir():

        # ensure file is valid for transcription process
        if ('.wav' in filename) and (filename not in ignore_files):

            # create audio splits and save the splits directory for use in processing transcript
            split_audio_dir = split_audio_into_parts(audio_directory=audio_directory, transcripts_directory=transcripts_directory, audio_file=filename, splits_directory=audio_splits_directory, delete_splits=delete_splits, prints=prints)

            # create the transcript from the audio split directory
            transcript = generate_transcript_from_audio_splits(audio_directory=split_audio_dir, transcripts_directory=transcripts_directory, filename=filename, naming_function=transcript_naming_function, prints=prints)

            completed_transcripts += 1

            # check if the user wants to delete the created audio splits
            if delete_splits:

                # files exist
                try:

                    # ensure safety in file deletion
                    os.chdir(audio_directory)

                    # they do, delete folder and all contents
                    shutil.rmtree(split_audio_dir)

                    if prints:
                        print('delete_splits marked true, deleted audio splits for:\t', filename)

                # files don't exist because previous transcription creation
                except FileNotFoundError as e:
                    pass
                    # files were previously deleted
                    # if prints:
                    #     print('delete_splits marked true, audio was never created, thus never deleted for:\t', filename)

            # check if user wants to delete original audio file
            if delete_originals:

                # they do, delete file in original audio_directory
                os.remove(audio_directory + filename)

                if prints:
                    print('delete_originals marked true, deleted original audio for:\t', filename)

            # if prints:
            #     print('---------------------------------------------------------------------------')

    if prints:
        print('completed transcript generation for all files in', audio_directory)

    return completed_transcripts

# RELEVANCY

# generate_words_from_doc for a document
def generate_words_from_doc(document, filename, versioning, prints=True):

    '''Generate the terms and term frequency in a single document.

    Arguments:

    document -- the os file path for where the transcript is stored.
        example: 'C:/transcription_runner/seattle/transcripts/transporation_112315.txt'

    filename -- the filename associated with the transcript.
        example: 'transporation_112315.txt'

    versioning -- the dictionary of previous versions the transcript has had. Default: dict()

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # initialize py-dict for synonyms
    # dictionary = PyDictionary()

    # construct results dictionary object to store all generated information
    results = dict()

    # construct versioning dictionary object to store all transcript versions
    versions = list()

    # construct base term frequency dictionary object to store term frequency information
    results['tf'] = dict()

    # if prints:
    #     print('started work on:', document, '...')

    # initialize transcript variable
    transcript = ''

    # try to find most recent version
    try:
        most_recent = len(versioning) - 1
        transcript = versioning[most_recent]['full_text']
        versions = versioning

        # if prints:
        #     print('using previously stored transcript')

    # no version, open the file
    except:

        # open the transcription file and read the content
        with open(document, 'r') as transcript_file:
            transcript = transcript_file.read()

        transcript_file.close()
        time.sleep(2)

        to_append_version = dict()
        to_append_version['full_text'] = transcript

        current_dt = datetime.datetime.now()
        split_point = filename.rfind('_')

        to_append_version['datetime'] = str(current_dt)
        to_append_version['version_shortname'] = filename[:split_point] + '_' + str(current_dt.date()) + 'T' + str(current_dt.hour) + '-' + str(current_dt.minute)
        versions.append(to_append_version)

        if prints:
            print('using newly created transcript')

    # replace any conjoining characters with spaces and split the transcription into words
    words = re.sub('[_-]', ' ', transcript).split()

    # if prints:
    #     print('split words...')

    # for each word in the transcription
    for word in words:

        # get rid of any non-alphanumeric characters
        word = re.sub('[!@#$]', '', word)

        # temporary fixes for transcription generated decimals and percents
        word = word.replace('/', ' over ')
        word = word.replace('.', ' point ')
        word = word.lower()

        if len(word) > 0:

            # try adding to the word counter
            try:
                results['tf'][word]['count'] += 1

            # must not have been initialized yet
            except:

                # construct the synonyms list
                # synonym_add_list = list()

                # construct the nearby words list
                # nearby_words_list = list()

                # to_check_synonyms = dictionary.synonym(word)
                #
                # if type(to_check_synonyms) is list:
                #     for synonym in dictionary.synonym(word):
                #         if ' ' not in synonym_add_list:
                #             synonym_add_list.append(synonym)

                # initialize the word counter and add the synonyms
                results['tf'][word] = {'count': 1}

    # store the word length of the transcription
    results['length'] = float(len(words))

    # if prints:
    #     print('initial pass for transcript complete')

    # for each word in the generated term frequency dictionary
    for word, data in results['tf'].items():

        # compute the true term frequency
        results['tf'][word]['score'] = float(data['count']) / results['length']

    # if prints:
    #     print('secondary pass for transcript complete, sending completed items')

    # return the completed term frequency dictionary
    return results, versions

# generate_tfidf_from_directory for a directory of transcripts
def generate_tfidf_from_directory(transcript_directory, storage_directory, stored_versions=None, prints=True):

    '''Generate the tfidf JSON tree for a directory of transcripts.

    Arguments:

    transcript_directory -- the directory or folder os path for where the transcripts are stored.
        example: 'C:/transcription_runner/seattle/transcripts/'

    storage_directory -- the directory or folder os path for where the storage (JSON) files will be stored.
        example: 'C:/transcription_runner/seattle/json/'

    stored_versions -- the previously stored tfidf data, retrieved either from local storage or database storage. Default: None

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    # check_path_safety for project
    transcript_directory = check_path_safety(transcript_directory)
    storage_directory = check_path_safety(storage_directory)

    # after check, set the directory to match
    os.chdir(transcript_directory)

    if prints:
        print('starting work on:', transcript_directory, '...')

    # initialize versioning dictionary
    versioning = dict()

    # check if the previously stored data falls into the local or database storage conventions used by this system
    if (type(stored_versions) is collections.OrderedDict) or (type(stored_versions) is dict):

        rewrites = 0

        # for each transcript in the previously stored data complete rewrite process if needed
        for transcript in stored_versions:

            # check for versions created not by this process
            versions = stored_versions[transcript]
            versioning[transcript] = versions
            most_recent = len(versions) - 1

            # if the most recent version was not created by this process, rewrite the transcript file for backup and tfidf processing
            if most_recent != 0:

                rewrites += 1

                # remove original
                os.remove(transcript_directory + transcript + '.txt')

                # actual rewrite
                with open(transcript_directory + transcript + '.txt', 'w', encoding='utf-8') as outfile:
                    outfile.write(versions[most_recent]['full_text'])

                # file safety
                outfile.close()
                time.sleep(1)

                # if prints:
                #     print('rewrote file:', transcript_directory + transcript + '.txt')
                #     print('\tusing text:', versions[most_recent]['full_text'][:20])

        if prints:
            print('rewrote', rewrites, 'files ...')

    # initialize results dictionaries
    results = dict()

    # initialize base dictionaries for storage of deep information
    results['words'] = dict()
    results['transcripts'] = dict()

    transcript_counter = 0

    # for all .txt files generate words information and calculate tfidf
    for filename in os.listdir():

        # ensure file is valid for tfidf process
        if '.txt' in filename:

            # increment total transcriptions counter
            transcript_counter += 1

            try:
                # get words information for file
                file_results, file_versions = generate_words_from_doc(document=transcript_directory+filename, filename=filename, versioning=versioning[filename[:-4]], prints=prints)

            except:
                # no versioning, create new
                file_results, file_versions = generate_words_from_doc(document=transcript_directory+filename, filename=filename, versioning=None, prints=prints)

            versioning[filename[:-4]] = file_versions

            # if prints:
            #     print('adding word set to corpus...')

            # get results for all words in corpus
            for word, score in file_results['tf'].items():

                # try adding to word counter
                try:
                    results['words'][word] += 1

                # was not initialized yet
                except:
                    results['words'][word] = 1

            # add single file results to total file results
            results['transcripts'][filename[:-4]] = file_results

            # if prints:
            #     print('completed file:', filename, '...')
            #     print('---------------------------------------------------------------')

    if prints:
        print('starting second pass word tfidf scoring ...')

    cleaned_results = dict()

    # for each transcript construct a tfidf dictionary to hold completed computation
    for transcript, data in results['transcripts'].items():

        # deep copy
        temp_data_hold = dict(data)

        # base layer for storage
        data['tfidf'] = dict()

        # for each word compute tfidf score
        for word, score in temp_data_hold['tf'].items():

                # debug items
                # print('transcript:', transcript, '\tword:', word, '\ttf score:', score, '\n\toccurances:', score['score'] * data['length'], '\tlength:', data['length'])

                # actual computation
                data['tfidf'][word] = float(score['score']) * math.log(transcript_counter / float(results['words'][word]))

        del data['tf']

    for transcript, data in results['transcripts'].items():
        cleaned_results[transcript] = data['tfidf']

    if prints:
        print('completed all files, storing and returning results for:', transcript_directory)
        print('----------------------------------------------------------------------------------------')

    if not os.path.exists(storage_directory):
        os.mkdir(storage_directory)

    # completed all computation, dump into output file
    with open(storage_directory + 'tfidf.json', 'w') as outfile:
        json.dump(cleaned_results, outfile)

    with open(storage_directory + 'events_versioning.json', 'w') as outfile:
        json.dump(versioning, outfile)

    # file safety
    outfile.close()
    time.sleep(1)

    # return the final dictionary object
    return cleaned_results, versioning

# predict_relevancy for a corpus of tfidf documents
def predict_relevancy(search, tfidf_store, edit_distance=True, adjusted_distance_stop = 0.26, results=10):

    '''Predict the relevancy of a transcript based off a search term or phrase.

    Arguments:

    search -- string value to be searched on against the tfidf created JSON tree.
        example: 'bicycle infrastructure'

    tfidf_store -- the os file path to where the tfidf JSON tree is stored.
        example: 'C:/transcription_runner/seattle/json/tfidf.json'

    edit_distance -- boolean value to determine if Levenshtein distance should be enabled. Default: True (allow edit distance to influence relevancy score)

    adjusted_distance_stop -- float value for setting the max weight an editted distance search term can affect relevancy. Default: 0.26 ( (1 - 0.26 = 0.74) * tfidf value )

    results -- integer value for number of results to be returned from the search.
    '''

    # open the locally stored json
    with open(tfidf_store, 'r', encoding='utf-8') as data_file:
        tfidf_dict = json.load(data_file)

    # ensure file safety
    data_file.close()
    time.sleep(1)

    # split the search into words
    split_search = search.split()

    # initialize the found comparisons dict
    found_dict = dict()

    # for each search term, construct relevancy dictionaries
    for transcript, data in tfidf_dict.items():

        correct_found = dict()
        similar_found = dict()

        # for each data point and information stored in stored dictionary
        for search_word in split_search:

            correct_chain_find = 0
            similar_chain_find = 0

            # for each word and it's score
            for stored_word, score in data.items():

                # if the word direct matches the search term
                if stored_word == search_word:

                    true_weight = score
                    correct_found[stored_word] = true_weight

                # direct search term not found as a word
                else:

                    # check if edit distance is allowed as attribute for searching
                    if edit_distance:

                        # calculate the adjusted_distance
                        adjusted_distance = float(Levenshtein.distance(stored_word, search_word)) / len(stored_word)

                        # if the adjusted_distance isn't too large
                        if adjusted_distance < adjusted_distance_stop:

                            true_weight = ((1 - adjusted_distance_stop) - adjusted_distance) * score
                            similar_found[stored_word] = true_weight

        # initialize a found result dictionary
        found_dict[transcript] = dict()
        found_dict[transcript]['relevancy'] = 0
        found_dict[transcript]['searched'] = dict()

        # add all correct words and associated scores with weighting to the found dictionary
        for correct_word, correct_score in correct_found.items():
            found_dict[transcript]['relevancy'] += (correct_score * 3)
            found_dict[transcript]['searched'][correct_word] = correct_score

        # add all similar words and associated scores with weighting to the found dictionary
        for similar_word, similar_score in similar_found.items():
            found_dict[transcript]['relevancy'] += similar_score
            found_dict[transcript]['searched'][similar_word] = similar_score

    # sort the found data by the relevancy score
    found_dict = sorted(found_dict.items(), key=lambda x: x[1]['relevancy'], reverse=True)

    print('searched corpus for:', search)

    # return the found data
    return found_dict[:results]

# COMBINING AND STORING

# combine_data_sources for JSON files of video feeds and tfidf tree
def combine_data_sources(feeds_store, tfidf_store, versioning_store, storage_directory, prints=True):

    '''Combine feeds storage and tfidf storage objects into a single object.

    Arguments:

    feeds_store -- the os file path for where the feeds_store created by get_video_feeds is stored.
        example: 'C:/transcription_runner/seattle/json/video_feeds.json'

    tfidf_store -- the os file path for where the tfidf_store created by generate_tfidf_from_directory is stored.
        example: 'C:/transcription_runner/seattle/json/tfidf.json'

    storage_directory -- the directory or folder os path for where to store the combined JSON file.
        example: 'C:/transcription_runner/seattle/json/'

    prints -- boolean value to determine to show helpful print statements during the course of the run to indicate where the runner is at in the process. Default: True (show prints)
    '''

    if prints:
        print('combining data sources:')
        print('\t', feeds_store)
        print('\t', tfidf_store)
        print('\t', versioning_store)

    # ensure path safety
    storage_directory = check_path_safety(storage_directory)

    if not os.path.exists(storage_directory):
        os.mkdir(storage_directory)

    # read the feeds_data in
    with open(feeds_store, 'r') as feeds_file:
        feeds_data = json.load(feeds_file)

    # ensure file safety
    feeds_file.close()
    time.sleep(1)

    # read the tfidf_data in
    with open(tfidf_store, 'r') as tfidf_file:
        tfidf_data = json.load(tfidf_file)

    # ensure file safety
    tfidf_file.close()
    time.sleep(1)

    with open(versioning_store, 'r') as versioning_file:
        versioning_data = json.load(versioning_file)

    versioning_file.close()
    time.sleep(1)

    # initialize the combined_data dictionary to be stored
    combined_data = dict()
    combined_data['events'] = dict()
    combined_data['events_tfidf'] = tfidf_data
    combined_data['transcript_versioning'] = versioning_data

    # place each item from the feeds data into the matching combined_data location
    for item in feeds_data:
        if item['naming'] != '':
            combined_data['events'][item['naming']] = item

    # give the combined_data a filename
    result_file = storage_directory + 'combined_data.json'

    # always rewrite the file because of potential changes in tfidf process
    if os.path.exists(result_file):
        os.remove(result_file)

    # actual rewrite of file
    with open(result_file, 'w') as combined_file:
        json.dump(combined_data, combined_file)

    # ensure file safety
    combined_file.close()
    time.sleep(1)

    current_dt = datetime.datetime.now()
    curr_date = current_dt.date()
    curr_time = current_dt.time()

    result_log_file = storage_directory + 'combined_data_' + str(curr_date) + 'T' + str(curr_time).replace(':', '-') + '.json'

    with open(result_log_file, 'w') as combined_log_file:
        json.dump(combined_data, combined_log_file)

    combined_log_file.close()
    time.sleep(1)

    if prints:
        print('stored combined data at: ' + result_file)
        print('stored combined data at: ' + result_log_file)
        print('----------------------------------------------------------------------------------------')

    return combined_data

