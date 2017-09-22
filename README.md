# Transcription Runner
Multiple tools, mainly focused on searching, transparency, and accountability for City Councils.

Created by Jackson Maxfield Brown and Dr. Nicholas Weber

**If you are looking to setup your own version of the transcription runner, jump to: [Setup and Automation](#setup-and-automation)**

- [Project Updates and Timeline](#updates)
- [Background](#background)
   - [Need](#need)
   - [Questions](#questions)
   - [Additional Info](#additional-information)
   - [Previous Work](#previous-work)
- [Planning and Ideation](#planning-and-ideation)
   - [Understanding the Problem](#understanding-the-problem)
   - [Project Planning](#project-planning)
- [Development](#development)
   - [Current Work](#current-work)
   - [Future Work](#future-work)
- [Tools](#tools)
   - [Legistar](#legistar)
   - [scraping](#scraping)
   - [ffmpeg](#ffmpeg)
   - [speech recognition](#speech-recognition)
   - [tfidf](#tfidf)
   - [pyrebase](#pyrebase)
- [Setup and Automation](#setup-and-automation)
   - [Software Installations](#software-installations)
   - [Automation](#automation)
   - [Testing](#testing)
- [Final Comments](#final-comments)

## Updates
Current Development Items are marked in **_bolded italics_**

- [Understanding the Problem](#understanding) *- complete*
   - Own ideas and explanations
   - Exploration of other ideas
   - Meeting with direct users
   - Confirmation of problems and project potential

- [Planning for Development](#project-planning) *- complete*
   - Initial baseline development choices
   - Parse data and understand what is available
   - Testing and rough development
   - Establishment of stretch goals
   - Mockups and design, database and frontend

- [Development Work](#current-work)

   - Event Components (Chained Interactions)
      - [Legistar](#Legistar) *- complete*
         - Create connection to base Legistar system
         - Establish storage for database and local
         - Rebuild as reusable system

      - [Videos](#scraping) *- complete*
         - Understand available systems for requests
         - Use decided system to pull direct video sources and information
         - Establish storage for local
         - Rebuild as reusable system

      - [Audio Separation](#ffmpeg) *- complete*
         - General file and os handling
         - Video to Audio separation established
         - Audio file splitter created
         - Rebuild as reusable system

      - [Transcription Engine](#speech-recognition) *- complete*
         - Test run of system
         - Understand process, errors, limitations
         - Scale to larger files
         - Rebuild as reusable system

      - [Search Engine](#tfidf) *- complete*
         - Create working concept of tfidf for a set of transcripts
         - Build system to scale for larger audio files
         - Attach agenda information to scoring algorithm
         - Attach body, date, etc. information to scoring algorithm
         - Attach synonyms and common replacements of high score attributes to scoring algorithm **_need to find better implementation_**
         - Create search functionality from user input
         - Add Levenshtein Edit Distance to user input on search
         - Fix bugs and finalize search
         - Rebuild as reusable system

      - Event Attributes Combination *- complete*
         - Ensure all prior systems are attachable to Event JSON **_somewhat abandoned, as connecting Legistar systems was difficult, will return at a later point_**
         - Test true Event object combination completion
         - Scale and establish store in database and local
         - Rebuild as reusable system

   - Server Development *- complete*
      - Migrate to current systems to server
      - Test basic system functionality and storage
      - Strict test on transcription engine

   - Full Stack Components
      - Front End
         - Rough design and basic layout created
         - Present filler information
         - Connection to database
         - Redesign after full data connected **_current: waiting on software and backend systems completion, 18 August 2017_**
         - Attach search engine functionality
         - Create Wiki style transcription editor
         - Bug fix and test user feedback
         - Finalize service design and launch
         - Rebuild as reusable system

      - Back End *- complete*
         - Decide on storage system
         - Store basic testing information
         - Create checker functions to only collect not-currently-stored data
         - Create automation processes to collect data
         - Rebuild as reusable system

- Conclusion *- not started*
   - Create finalized notes and processes completed
   - Structure all information and documentation created
   - Potential to publish work/ build system for other organizations

[Back to Updates](#updates)

[Back to Top](#transcription-runner)

## Background
A bit about the who, what, when, where, why, and how.

### Need
Finding information, whether general or specific is incredibly hard to do with the current interface. For Events data, there is a lack of transcripts, fuzzy searching, and multiple information sources referencing the same event but are not consolidated into a single object. Meaning that if someone wanted the true complete information for a city council event, they would have to visit multiple pages. The data generated from a process to create event transcripts could be used in all sorts of future applications. Mainly, computational linguistics operations, but true valuable insight could be found in a large set of event transcripts. Not only does this improve legislator accountability, but it allows for future growth and development from civic technology advocates.

I was originally drawn to this problem when I tried to search for housing laws in Seattle and was returned information regarding housing laws but not necessarily exactly what I was looking for, *there was no system for determining relevance of video and meeting data*. And it's not any one party's fault, there are just so many moving parts and different storage systems in place it is hard to connect them and generate valuable insight.

People need better searching potential, citizens need higher accountability of their legislators, and all parties need higher transparency for public events. Additionally, because the Legistar system is used by many other cities and towns, and I assume similar video storage solutions to Seattle's are in place as well, then an open-source, free method of combination and insight generation, would be valuable to politically active citizens, NGOs, legislators themselves, and, an incredibly powerful party that I believe would use this more than all others combined, journalists. With no current transcription system in place, journalists who attend contentious city council meetings have to take their own notes and re-watch the videos at a later time. This system would allow for collaborative information crowdsourcing soon after a video is published for all journalists to use as their baseline.

### Questions
- What is a good starting point for predicting the relevancy of a video/ audio/ or transcript?
- What information is currently available in the events Legistar system?
- How is information stored in the City of Seattle's multiple storage solutions connected?
- Is it possible to create a system for the city but scalable to handle other city data?
- Who is the target audience for this system besides politically motivated individuals and groups?
- Are there features the Clerks office would like developed?
- Have there been studies into the effects of open-source information crowdsourcing transcribing?

### Additional Information
In [Need](#need), I discussed the direct motivation for developing the City of Seattle proof of concept and the consequential features to build. However, there is also plenty of [future work](#future-work) that can be done in this area of civic technology.

Ranging from better relevance prediction and returns to computational linguistics and data science systems to evaluate city council meetings themselves. This is an area where there *should* be plenty of data, but currently there isn't as much as we would like, and thus once it is available, should open the doors to much more research.

### Previous Work
[Councilmatic](https://www.councilmatic.org/) is an organization that creates a kind of Legistar data aggregator and puts an interface over top for clearer information design however I believe there are two areas where Councilmatic falls short of the goal of this project. The core utility of this project is the transcription engine, not only does this generate a workable transcription for an event as a public record if there wasn't one already available, but it allows for Wiki style editing of the transcript for long term betterment of the transcription. Additionally, while Councilmatic is open-source, I find it's systems hard to understand and utilize which is why making this system truly plug-and-play software is a main goal. This should be able to be used by other cities who want similar functionality.

There are multiple researchers working in computational linguistics on civic and government projects, [here is an example](http://shoub.web.unc.edu/files/2017/04/Shoub_ShiftingFramesToShiftPolicy.pdf). While this research was on congressional debate data, it is easy to see how this work could be apply to my own City Council system. Not only do I believe this would produce interesting results but may also help improve search functionality.

[Back to Background](#background)

[Back to Top](#transcription-runner)

## Planning and Ideation
While there are many paths this project could have taken, centering in on events occurred due to the planning and ideation processes.

### Understanding the Problem
The main problem stems from the multiple systems and interconnectedness of storage solutions in place. Routing of information and data is split and can't be combined without costly remodeling of system architecture. From a civic tech development standpoint this makes developing on this data incredibly hard. From a City IT Department standpoint, it's a game of catchup, developers want x but they don't have the resources or time, and they usually have much more pressing issues to attend to. Since this project is based on the legislative service, the Clerks Office is the record keeper for all the laws in the city. Their systems need to be interconnected to multiple other services and should be able to handle the data ingestion from other government departments and agencies well before any third party users are addressed. This constant catchup and data splitting is usually due to parties coming in and continually building on top of preexisting software instead of rebuilding. While I understand I am doing the same, and building on top again, I am also trying to consolidate the information back together, and hopefully make it easier for this data to be used.

However, this leaves an incredibly opportunity gap for contribution to civic systems. While there are services like Councilmatic that can create more citizen focused interfaces and interactivity, there is still the problem of lack of data available. If the multiple systems are going to be combined, what other insight can you generate from the full event information rather than parts of it?

After meeting with individuals from the Clerks department there were a few direct hopeful outcomes for the project, the largest was a fuzzy search system for the data available. Secondly was just a front end update so that more than just the legislative minded would be able to use the system successfully.

### Project Planning
The targeted outcomes for the project are doable, but require a bit of scoping. As a fuzzy search system can be relatively similar across datasets, we can focus on one as a proof of concept and show how it can expand to cover more of the data available with more work. And for the interface and information design, we can narrow our focus to one section that I believe needs it the most: Events and event data. There are many more individuals who want to understand a recent council meeting and the events that occurred in the meeting than the number of individuals planning on attending an event, proposing legislation, etc. Additionally, creating a system that focused on the meetings of the legislators holds a lot of accountability and transparency value over the storage and presentation of the bills and amendments themselves.

Overall, the project will aim at developing a system to allow for fuzzy searching over event information that is available across the many platforms run by the City of Seattle. As well as providing a way for self-selected civic engagement for transparency and accountability of legislators.

And lastly, the project will aim to be structured as future plug-and-play work for further research and development in information crowdsourcing.

[Back to Planning and Ideation](#planning-and-ideation)

[Back to Top](#transcription-runner)

## Development
Development aims, uses, goals, and etc.

### Current Work
The aim for the proof of concept is as follows:
- Event data collection from multiple systems
- Generation of event transcripts
- Combination and storage of all relevant data
- Fuzzy search implementation by scoring
- Automated processing of new event videos and information

 We believe this is enough to at least get the ball rolling on civic technology influencing how city council members are held accountable for their actions and decisions. Making this information available, I believe incredibly interesting data science and computational linguistics projects to be developed. And really, this project is about data aggregation and consolidation. Bringing all the different resources into a single unified place will help all parties who want to access the data as well as encouraging them to work together in improving the information.

### Future Work
While the current work is decently shallow, there is plenty to continue working on after we finish the proof of concept.

Examples include:
- Adding request functionality in the case an audio file or transcript is missing (or the most recent run of the system occurred before the event was published).
- Better scoring and ranking algorithms for searching and determining relevance of an event.
- Adding synonym checking for searching to compare to known words and weight them
- Adding nearby words comparison to searching
- Scoring and ranking algorithms for other sections of City Council data.
- Add third party data ingestion, from the Clerks office themselves, so that they can directly add information to our storage so that we don't bog down their servers with additional scraping, and API usage.
- Determining trends in City Council for decisions on bills and amendments.
- Determining or predicting a council member's position on an upcoming bill, amendment, or resolution, based off of past meetings.
- Adding a 'How to Speak at a City Council Meeting' template for individuals who want to express their opinion on a piece of legislation.
- Using the generated transcripts to build an influential speaking template for communicating to City Council.
- Adding other sections of the Legistar and City Council data to the service. Specifically: creating a system for helping the public understand the current process and timeline of an event, or action awaiting decision.

[Back to Development](#development)

[Back to Top](#transcription-runner)

## Tools
Frameworks, libraries, and more that are being used by this project with explanations on how to used them and why they were selected to be used.

### Legistar

**The Legistar functions development have stopped for now, will be returned to at a later point, the functions themselves can still be found in the discontinued.py file**

Legistar is a system developed by [Granicus](https://granicus.com/) that enables storage and manipulation of public sector data. A large part of the Legistar system is that it allows for building and tailoring you own version of the service to each organization's needs. It is also incredibly robust in terms of scalability and data availability. [Link to the API methods available](http://webapi.legistar.com/help)

The main chunk of information I am pulling from the City of Seattle's Legistar API is the Events data. I utilize other API sections, bodies, bodytypes, etc., but it they are all used in order to help the Events data merging down the line.

Technically, I have created a system to pull any data from a Legistar system and format it for use with the other systems I am building by asking for a list of, what I am calling packed_route's. This is just an object that's key is the path for storage, either locally or in a NoSQL database, and the list attached to the key is the Legistar API URL (example: [http://webapi.legistar.com/v1/seattle/Events](http://webapi.legistar.com/v1/seattle/Events')), a targeting attribute to specify an individual element (example: 'EventID'), and a data cleaning_function. The cleaning function is user created but allows for a much more scalable system, instead of forcing the user into my own methods and functions, I allow them to change and manipulate each single entity returned from the call how they like and then return the completed entity. I believe my cleaning_functions and naming_functions should work for nearly all users however.

There is one additional parameter that should be addressed, the toLocal boolean parameter for the function acts as a way to stop the storage to a database and instead save a json file to your working directory. Originally implemented to save on storage cost, I realized this actually incredibly beneficial for later combining all the data together and then storing it in a single database put.

There is still some work to be done in my opinion. There can be improvements made in routing, and handling of data, however, for now, I believe this is a large improvement to developing with Legistar systems than previous build from the ground up methods. If an individual wanted to get data from a Legistar subscribing city into python, my functions would work for them.

[Back to Tools](#tools)

### scraping
Initially, I figured there would be transcripts available for all the meetings, usually called 'meeting minutes,' and while I am sure they may be tucked away somewhere in the databases of the City of Seattle. It posed an interesting problem to tackle. How to create a transcript from what was available. While the Legistar system had a plethora of Events data in their system, meeting minutes were not available, however in a separate Legistar system, videos were collected and had proper links. I could not find a solution to how to pull en masse the City Council meetings recordings however.

I asked for an API link, and searched the other Legistar services, was even pointed in the direction of an associated RSS feed, however none of the solutions presented to me really suited the problem I was facing of trying to store their videos for future processing.

Enter, web scraping. I built a simple enough way to generate a JSON object with the required information needed to run the rest of the video transcription process, given a suitable scraping function created by the user. Again, hoping that this software will be used by other cities as a way for better City Council meeting understand, searching, and accountability, this needed to be modularized.

Using a similar model as the Legistar system, the user supplies a list of packed_routes, the key still acts a path and storage identifier, this time however, the URL is linking to the page with the video sources, and a body_name is supplied which is the name of the body as it is stored in the Legistar system. This is required for matching the data later on as what I found was that Seattle would have a video body name and label but internally, they have a Legistar name and label that sometimes doesn't match.

The scraping function defaults to my Seattle Channel specific scraper, but it is a simple function using [BS4](https://pypi.python.org/pypi/beautifulsoup4) and [Requests](http://docs.python-requests.org/en/master/) to retrieve, all the video links on a page, and for each link, the source URL, the video agenda, and store the datetime of publishing.

Lastly, I have a toLocal boolean again to ensure safety in processing the data and finally I returned the constructed json objects with all the completed data back.

[Back to Tools](#tools)

### FFmpeg
One of the areas I think this system also is valuable, is that it creates all different types of way to view the City Council event media. I originally planned on only returning back the transcripts for a meeting, but as a way to generate the transcripts I first needed to split the videos audio into a specific audio file.

FFMPEG allows for such, quickly and easily. Using subprocess and a bit of path chaining, it was easy to set up functions for splitting audio from a single file to all files in a directory.

[Back to Tools](#tools)

### speech recognition
The python speech recognition package is really what this entire project hinges on. It creates a link to the Google Speech Recognition API and generates a transcript for a portion of audio. Sounds simple enough?

In reality, Google will almost never let an individual process large chunks of audio at a time, so we needed to create a system to split the audio and then transcribe each snippet and then combine all the smaller transcripts back together.

To split the audio, I created a function that utilizes the [AudioSegment](http://pydub.com/) package, and from there you can do simple list slicing on Audio to create smaller segments of Audio without any data loss. The real issue with this step in the process is the labeling of the audio splits themselves. While I want as much of this project to be modular and very easy to plug-and-play with different parts of it, the naming function I created I believe is the best route forward if you are going to be continuing on into the transcription process. If you aren't continuing on and just want the audio splits, the use your own naming function and label each split whatever you like. But currently, the transcription function that utilized the create audio splits function is hard coded to find only splits named by my function.

This is just due to how to easily stitch the splits back together. The simplest solution I could think of and the one I chose to implement, was to naming the files with an integer range. Incrementing with each subsequent audio split. So that when stitching them back together I could just run a loop from zero to length of audio file divided by the Google Audio clip size (I believe 18,000ms).

Additionally, there are boolean parameters to delete the original audios that was split from the video files, and/ or delete the constructed audio splits.

Once all transcripts are completed, they are stored, and the number of completed transcripts is returned to the user to ensure a complete run or for logging purposes.

[Back to Tools](#tools)

### tfidf

[Back to Tools](#tools)

### pyrebase


[Back to Tools](#tools)

## Setup and Automation
For individuals, organizations, or even cities that want to use this for their own city council data. I have tried to make this process as simple as possible.

**As a precautionary note:** Please ensure you have a decent amount of storage on your computer/ server as the initial video storage was about 360 GB of data. Additionally, while most people will be running this on a server, if you are running it on your computer, it is recommended to have at least 6 GB of memory (RAM).

### Software Installations
Required Dependencies:

- [64 bit Python 3.6](https://www.python.org/downloads/)
   - Navigate and hover over 'Downloads' on navigation bar
   - Click on your operating system
   - Find and download the most recent Python 3.6 64 bit installer
   - Install with PATH permissions, and pip.
   - After install, find the Python executable file in your directories
   - Whichever folder the executable is in, give that folder all access security permissions.

- [Visual C++ Build Tools 2015](http://landinghub.visualstudio.com/visual-cpp-build-tools)
  - Download and install

- [FFmpeg](https://ffmpeg.zeranoe.com/builds/)
   - For Windows
      - Indicate which version, architecture, and linking you want
      - Download and extract files to where you want to store them
      - Where ever you stored them find the bin folder
      - Add bin folder to your system environment PATH

   - For Mac
      - Using [homebrew](https://brew.sh/)
      - 'brew install ffmpeg --with-libvorbis --with-ffplay --with-theora'

   - For Linux
      - 'apt-get install ffmpeg libavcodec-extra-53'

   - Ensure it installed correctly by opening a Command Prompt, Terminal, etc, and typing 'ffmpeg -version'      

- [Requests](http://docs.python-requests.org/en/master/)
   - Open a Command Prompt, Terminal, etc. with Administrator privileges
   - Try: 'pip install requests'
   - Didn't work, Try: 'python -m pip install requests'

- [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
   - Open a Command Prompt, Terminal, etc. with Administrator privileges
   - Try: 'pip install beautifulsoup4'
   - Didn't work, Try: 'python -m pip install beautifulsoup4'

- [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)
   - Open a Command Prompt, Terminal, etc. with Administrator privileges
   - Try: 'pip install SpeechRecognition'
   - Didn't work, Try: 'python -m pip install SpeechRecognition'

- [pprint](https://docs.python.org/2/library/pprint.html)
   - Open a Command Prompt, Terminal, etc. with Administrator privileges
   - Try: 'pip install pprint'
   - Didn't work, Try: 'python -m pip install pprint'

- [Pydub](https://pypi.python.org/pypi/pydub)
   - Open a Command Prompt, Terminal, etc. with Administrator privileges
   - Try: 'pip install pydub'
   - Didn't work, Try: 'python -m pip install pydub'

- [Levenshtein](https://pypi.python.org/pypi/python-Levenshtein)
   - Open a Command Prompt, Terminal, etc. with Administrator privileges
   - Try: 'pip install python-Levenshtein'
   - Didn't work, Try: 'python -m pip install python-Levenshtein'

### Automation
As I said previously, I tried to make this service as simple to setup as possible.

With that said, there is a bit of work to be done when adding a new city. You need a scraper function, or, if it is available an API, for the videos collection. My Seattle Channel scrapper can be found in the [get_store_data.py](https://github.com/OpenDataLiteracy/jksn-2017/blob/master/CDP/python/get_store_data.py) file as an example. Additionally there is a general template down below in [Testing](#testing).

After that however, as long as you have the required dependencies installed correctly, you can find an automated runner, and logging function [here](https://github.com/OpenDataLiteracy/jksn-2017/blob/master/CDP/python/cdp_runner.py). Which does everything else for you.

Provide the run_cdp function with a project_directory, this will be where everything is stored. I have this in my resources folder, however you can have this wherever you want. Provide the legistar packed_routes object you would like to collect. Provide a video_routes packed_routes object you would like to collect. Provide a log_directory path. Provide a scraping_function for the video_routes. And lastly, there are also many default parameters such as delete_videos, delete_splits, test_search_term, prints, block_sleep_duration, run_duration, and logging.

An example of how you might set up the automated run is below.

**Example:**

```python
from cdp_runner import *

# VARIABLES AND OBJECTS

# project_directory is where everything will be stored
project_directory = 'C:/transcription_runner/city/resources/'

# json_directory is where all local JSON files will be stored
json_directory = project_directory + 'json/'

# logging directory is where all logging files will be stored
log_directory = project_directory + 'logs/'

# video_routes is the seattle_channel packed_routes object
video_routes = {
                # path: [videos page, legistar body name]
                'full_council': ['http://www.testcity.gov/meetings', 'Full Council']
}

# my scraper for collecting video sources
def my_scraper(path, routes, prints=True):

  # i need to work on my scraper...

  constructed_feeds = list()

  for each video element available in routes[0]:

    feed_info = dict()
    feed_info['path'] = path
    feed_info['body'] = routes[1]

    # required
    # feed_info['video'] = ...
    # feed_info['naming'] = ...

    # nice to have
    # feed_info['agenda'] = ...
    # feed_info['datetime'] = ...
    # feed_info['link'] = ...

    collected_feeds.append(feed_info)

  if prints:
    print('collected feeds for:', route[0])

  return constructed_feeds

# my database pull function
def my_pull_function(database_head):

  # this could probably use some work too...

  return database_head.get()

# path to where i want the database to pull from
database_head = database.main

# identifier to specify something relates to the tfidf process
relevant_tfidf_storage_key = 'events_tfidf'

def my_commit_function(data_store, database_head, prints=True):

  # wow, i really need to work on my functions...

  with open(data_store, 'r') as data_file:
    data = json.load(data_file)

  for key in data:
    database_head.push(data[key])

  if prints:
    print('stored data from:', data_store)


run_cdp(project_directory=project_directory, json_directory=json_directory, video_routes=video_routes, scraping_function=my_scraper, log_directory=log_directory, pull_from_database=my_pull_function, database_head=database_head, relevant_tfidf_storage_key=relevant_tfidf_storage_key, commit_to_database=my_commit_function)
```

Here is a list of other default settings:

- delete_videos = False; keeps or removes the videos once the audio is stripped
- delete_splits = False; keeps or removes the audio splits once the transcript is generated
- test_search_term = 'bicycle infrastructure'; used for testing the speed of searching the tfidf created tree
- prints = True; adds or removes prints when completed process for better understanding of what is happening in the system
- block_sleep_duration = 21600; duration of time in seconds that should sleep after completing a single cycle of the program
- run_duration = -1; total system runtime, if -1, runs infinitely, else, duration in seconds
- logging = True; adds or removes log creation for the automated runner

To run, open a Command Prompt, Terminal, etc. in Administrator. Navigate directories to where you runner python file is located. And run `python cdp_runner.py`

That's it. It will run and collect data until you manually shut it down unless you changed the default settings to have a run_duration.

### Testing
If you want to test a specific part of the actual service, I recommend making your own testing python file and importing my [get_store_data](https://github.com/OpenDataLiteracy/jksn-2017/blob/master/CDP/python/get_store_data.py) like so:

`from get_store_data import *`

This will import all functions and more importantly variables. Then you can go ahead and test the functions you like.

There are also some discontinued and abandoned functions to experiment with if you would like in the discontinued.py file.

**Examples:**

```python
from get_store_data import *

video_routes = {
                'test': ['http://www.testcity.gov/meetings', 'Full Council']
}

storage_path = 'C:/Users/Me/Desktop/video_feeds.json'

# my scraper for collecting video sources
def my_scraper(path, routes, prints=True):

  # i need to work on my scraper...

  constructed_feeds = list()

  for each video element available in routes[0]:

    feed_info = dict()
    feed_info['path'] = path
    feed_info['body'] = routes[1]

    # required
    # feed_info['video'] = ...
    # feed_info['naming'] = ...

    # nice to have
    # feed_info['agenda'] = ...
    # feed_info['datetime'] = ...
    # feed_info['link'] = ...

    collected_feeds.append(feed_info)

  if prints:
    print('collected feeds for:', route[0])

  return constructed_feeds

get_video_feeds(packed_routes=video_routes, storage_path=storage_path, scraping_function=my_scraper)
```

[Back to Top](#transcription-runner)

## Final Comments

[Back to Top](#transcription-runner)
