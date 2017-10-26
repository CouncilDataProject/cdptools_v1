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
                print('File already removed')

    if prints:
        print('completed audio stripping for:', video_directory)
        print('---------------------------------------------------------------')

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

        if prints:
            print('transcript exists, and delete_splits marked true, no need to create splits...')

        return store_directory

    if prints:
        print('creating audio splits for:\t', audio_directory + audio_file)

    # check if the splits already exist
    if os.path.exists(store_directory):

        if prints:
            print('audio splits for:\t', audio_file, 'already exists...')

        # they existed, return the store_directory path
        return store_directory

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
        print('transcript for:\t', transcribed_name, 'already exists...')
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
        print('-------------------------------------------------------')

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

                    # files were previously deleted
                    if prints:
                        print('delete_splits marked true, audio was never created, thus never deleted for:\t', filename)

            # check if user wants to delete original audio file
            if delete_originals:

                # they do, delete file in original audio_directory
                os.remove(audio_directory + filename)

                if prints:
                    print('delete_originals marked true, deleted original audio for:\t', filename)

            if prints:
                print('---------------------------------------------------------------------------')

    if prints:
        print('completed transcript generation for all files in', audio_directory)

    return completed_transcripts