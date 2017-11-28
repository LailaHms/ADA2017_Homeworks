### README - HOW TO USE THE TWITTER ACQUISITION SCRIPTS :

# First Start :

- 0 : install the requirements : Selenium and PhantomJS
- 1 : Create the **Folder** in which all the files are going to be stored. (for example ./Charlie-Hebdo/ for the Paris attack)
- 3 : Open the script `tweet_acquisition.py` in an editor and modify the variables : `path_save` and `log_save` accordingly
- 4 : Modify the list of hashtags `hashtags` and the start and end time of acquition : `date_start` and  `date_stop`
- 2 : Launch the script `tweet_acquisition.py` without any options.
- 3 : Launch the script `location_acquisition.py` and specify in input the folder of step 1. The script wait until there in a `Tweets_X.pickle` inside the folder and create immediatly and empty equivalent : `Located_Tweets_X.pickle`
- 4 : Launch several other instances of `location_acquisition.py` (in different terminals).

# Restart after a crash or internet connection loss of bug or anything weird :
- 1 : Launch the script `tweet_acquisition.py` with in option the name and path of the last `Tweets_X.pickle`
- 2 : Delete the empty pickles `Located_Tweets_X.pickle`, the script didn't has the chance to fill them.
- 3 : Launch the script `location_acquisition.py` and specify in input the **folder** of step 1
- 4 : Launch several other instances of `location_acquisition.py` (in different terminals).

# Time Informations :

- `tweet_acquisition.py` takes about 20min to create a pickle with about 6500 tweets inside
- `location_acquisition.py` is extremely slow (same as the API) it takes about 2h30 to convert a normal tweet pickle into a located tweet pickle. Be patient ;)
