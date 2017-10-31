Final Summary
# Title
International awareness to notable events

# Abstract 
What's the motivation behind your project? A 150 word description of the project idea, goals, dataset used. What story you would like to tell and why? 


	Major events happen on a regular basis all around the world, some involving high number of casualties but the resulting reaction on the international scale is often far from proportional. Most of the time the largest reaction comes from the place where the incident occurred or places which are closeby. The objective would be  to create an awareness map, and determine why people react to an event. From that we would attempt to define an awareness metric. We want to see how factors other than physical proximity come into play such as country, culture, language, religion. With this we could determine which country has the highest level of international awareness.  The project would require the Twitter API to acquire hashtag specific tweets with geolocation and therefore measure the awareness and reactions of different communities to a given event. GDELT would be used to recover standardised information regarding different events. 


# Research questions 

A list of research questions you would like to address during the project. 


- Question 1: How do we measure awareness? Observation of the reaction in Twitter (awareness level) to some notable event in space and time using event specific hashtags. We will use the number of tweets as the metric to compute the awareness level.
- Question 2 : Why and how do different factors influence the reactions?
Geographic location:   is the distance between country - event location influencing the awareness level of the notable event in that country?
Language :  indicative of the relation between the different countries
Other metrics :culture, religion, government (democracy, kingdom, dictatorship …) , history, ...
- Question 3: Is there a particular country that has a particularly high level of awareness regarding what happens in the rest of the world?
- Bonus Question 4 : sentiment analysis? Study the positivity/negativity of the reactions  http://text-processing.com/demo/sentiment/ 
- Bonus Question 5 : Check if news has an impact on the country’s reaction or if reaction is news independent 

An important point to take into account was which events to select so that they could be comparable and tell a story. For this the nature of the event, the number of casualties, who was effected (civilians, military etc…)  needed to be taken into account. Another factor was the location. 


When analyzing the reactions we need to be attentive to the level of twitter activity. Between different different countries we may require a normalizing factor or selecting events in countries where there is a minimal twitter activity. We also need to be attentive to the size and population of the countries and the proportion of tweeters.

Case 1: Events of similar magnitude, civilian casualties, 6 months timeframe

- Nigeria 30/01/2016, Shooting 65 Deaths, 136 Injured
- Belgium 22/03/2016, Bombing in airport, 35 Deaths, 300+ Injured
- Pakistan 27/03/2016, Bombing, 70 Deaths, 300 Injured
- US 12/06/2016 Shooting in gay bar, 49 Deaths, 53 Injured
- Turkey 28/06/2016, Shooting + bombing in airport, 45 Deaths, 230 Injured
	
Case 2: Events of different magnitude
- France 07/01/2015, Charlie Hebdo, 12 Deaths, 11 Injured
- Nigeria 08/01/2015, Massacre Boko Haram, 200+ Deaths, unknown Injured
- Lebanon 10/01/2015, suicide bombing, 9 Deaths, 30+ Injured


Note : it would be interesting to see whether certain people mention multiple hashtags and where they come from. 

# Dataset 
List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.

- Twitter API : originally we had planned on using the given twitter dump, after discussing with the TAs we decided to create our own dataset based on twitter API. This is necessary as our project requires having the geotags of the tweets and or users to determine areas of higher awareness. Using the API we can extract the tweets for  given hasthags, the time of creation, the user information which is to say the location, language etc… We tested the API as can be seen in the following link [XXXX]. We can recover 180 pages of 100 tweets for a specific hashtag every 15 minutes. With 6 APIs (two per member of the group) this would mean 432’000 tweets per hour. Note : 1 API per hashtag to avoid recovering the same tweets twice. 
- GDELT (with queries) for major events with localisation with UCDP. This datasets would be useful to get standardised information on the selected events. 
- Wikidata for other metrics (language, religion, government, population, country size etc...)


# A list of internal milestones up until project milestone 2
Add here a sketch of your planning for the next project milestone.
Essentially : acquire, clean and merge the data
- Select the events
- Acquire relevant information from the GDELT and UCDP platform using queries to have standardised information 
- Identify hashtags corresponding to selected events
- Extract tweets related to the given hashtags with geo-localisation & time
- Geocode the tweets to link the user to geographic coordinates (countries/cities/…)
- Extract additional information for all countries : language, religion, government and merge into one dataframe
- Check for correlations in terms of number of tweets, country, language, religion etc… 
- Establish the awareness metric
- Start thinking about the data story

# Questions for TAs
Add here some questions you have for us, in general or project-specific.


- How many tweets would be considered as a sufficient sample for the analysis? If we assume that we want to recover up to 10 million tweets per event and we assume that we have 1 API per event, with up to 6 APIs for the group, We would need 8 full days to recover the tweets for an event given that the recovery can be done in parallel for 6 events. Would that be sufficient?
- How much memory RAM would this require? Would it be feasible to conduct the analysis without resorting to cloud computing?
- When are we getting the feedback for the milestone 1?
- Are the internal milestones sufficient to be up to date?
- Please don’t hate us for having written all of this <3



