# import libraries
from requests import get
from bs4 import BeautifulSoup
import csv
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn
import pandas as pd

precincts = [str(i) for i in range(1214202, 1214255)]

# Lists to store the data in
candidates = []
votes = []
precinctURL = []

# Monitor the loop
start_time = time()
requests = 0

# for county aitkin
for precinct in precincts:

    # specify the url
    response = get(
        'https://electionresults.sos.state.mn.us/Results/PrecinctListResults/115?countyid=1&precincts=' + str(
            precinct))

    # pause the loop
    sleep(1)

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: []'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > 55:
        warn('Number of requests was greater than expected.')
        break

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(response.text, 'html.parser')

    # candidate and vote containers
    candidate_containers = soup.find_all('tr', class_='resultcandidates', limit=35)

    for container in candidate_containers:
        # candidate name
        candidate = container.find('td', class_='resultcandidate').text
        candidate.replace(r'\r\n', " ")
        candidates.append(candidate)

        # candidate votes
        vote = container.find('td', class_='resultvotes').text
        vote.replace(r'\r\n', " ")
        votes.append(vote)

        # precinct URL
        precinctURL.append(str(precinct))


precinct_results = pd.DataFrame({'Candidate': candidates,
                                 'Vote Total': votes,
                                 'Precinct URL': precinctURL})
print(precinct_results.info())
print(precinct_results.head(10))

precinct_results = precinct_results[['Candidate', 'Vote Total', 'Precinct URL']]
precinct_results.head()

precinct_results.to_csv('scraped.csv')