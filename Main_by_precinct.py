import time
from time import sleep
from warnings import warn
import urllib.parse as up
from requests import get
from bs4 import BeautifulSoup
import re
import datetime
import psycopg2


def resultsScraper(countyCode, precinctCodes):

    print(countyCode, precinctCodes)
    precinct_entry = "INSERT INTO results18 (county, precinct, office, party, candidate, raw_votes, percentage) values "
    precincts = ""
    for precinct in precinctCodes:
        precincts += precinct
        precincts += ","

    precincts = precincts[:-1]
    # print(precincts)
    # specify the url with 'countyid' and 'precincts'
    response = get(
        'https://electionresults.sos.state.mn.us/Results/PrecinctListResults/115?countyid=' + countyCode + '&precincts=' + precincts)

    # parse the html using beautiful soup and store in variable `soup`
    # pip3 install lxlm
    soup = BeautifulSoup(response.text, 'html.parser')

    # Selects starting area in html at 'center'
    center = soup.find('center')

    # Creates list of precinct names,
    # sets iterator at 1 to skip "Results for Selected Precincts in Hennepin County"
    precinct_containers = soup.find_all('div', class_='resultgroupheader')
    pnum = 1

    # Creates list of all tables which is where results are stored for each precinct
    tables = center.find_all('table')

    # Iterates through table
    for ptable in tables:

        # Holds the name of the office_name candidates are running for i.e. U.S. Senator
        office_name = ""

        # Creates list of all rows which is where each candidates results are stored
        rows = ptable.find_all('tr')

        # Iterates through candidates
        for row in rows:

            # Initializes the string that holds the row for each candidate result in table
            # with precinct name and office name
            rowentry = "('" + precinct_containers[0].text.strip()[34:-7] + "','" + precinct_containers[pnum].text.strip() + "','" + office_name + "'"

            # Check if the row has 'class' so it doesn't error, skips if doesn't
            if row.has_attr('class'):

                # Updates the 'office_name' variable to whichever seat candidates are running for
                if row['class'] == ['resultofficeheader']:

                    # Generates and cleans the office name
                    office_name = row.find('div', class_='resultoffice')
                    office_name = office_name.text.strip()
                    office_name = re.sub(r"\s+", " ", office_name)

                # If not a new office, check if a candidate result
                elif row['class'] == ['resultcandidates']:

                    # Selects appropriate entries, cleans extra empty field, cleans text
                    cols = row.find_all('td')[:4]
                    cols = [ele.text.strip() for ele in cols]
                    if cols:
                        for ele in cols:
                            rowentry += ",'"
                            rowentry += ele.replace("'", "") + "'"
                        # rowentry += "," + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                        rowentry += "),"
                        # print(rowentry)
                        precinct_entry += rowentry

                        # print(rowentry)
        # Updates to next precinct once iterated through entire table
        pnum += 1
    precinct_entry = precinct_entry[:-1]
    cur.execute(precinct_entry)
    # print(precinct_entry)

def precinctCodes(countyCode, reportedPrecincts):

    # print(countyCode)
    # List to store codes in
    newPrecincts = []
    precinct_codes = ""
    precinct_counter = 0

    # Specificy URL
    response = get('https://electionresults.sos.state.mn.us/Select/CountyPrecinctSelect/115?districtid=' + countyCode)

    # Parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(response.text, 'html.parser')

    # Precinct list
    precinct_list = soup.find_all('option', class_='selOptNotReported', limit=5) # Change back to 'selOptReported' when actually using, and limit 253

    # Check all precinct codes
    for precinct in precinct_list:
        precinctCode = precinct.attrs['value']

        # Compile precincts that reported since last check
        if precinctCode not in reportedPrecincts:
            newPrecincts.append(precinctCode)
            precinct_counter += 1
            precinct_codes += precinctCode
            precinct_codes += ","

    # print(precinct_codes)
    # print(newPrecincts)
    # print(precinct_counter)

    return newPrecincts


#-- Main -------------------------------------------------------------------------------

conn = psycopg2.connect(dbname="results18", user="dflvictory", password="dflguest18", host="dfl-election-returns.cmycsq7ldygm.us-east-2.rds.amazonaws.com")
cur = conn.cursor()
cur.execute("set time zone 'America/Chicago'")



# while True:
# precinctsReported = numpy.empty(88, dtype=object)
precinctsReported = [[] for i in range(88)]
# print(precinctsReported)

# URL
URL = 'https://electionresults.sos.state.mn.us/Results/CountyStatistics/115'

# Open URL
response = get(URL)

# Monitor Loop
start_time = time.time()
requests = 0

# Throw a warning for non-200 status codes
if response.status_code != 200:
    requests += 1
    warn('Request: {}; Status code: []'.format(requests, response.status_code))

    # Slow the loop
    sleep(1)

# Parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(response.text, 'html.parser')

# Precinct list
counties_reported = soup.find_all('tr')

# Finding County Results
for county in counties_reported:

    # Removes nulls
    if county.find('a', href=True) is not None:

        # Get County Code
        row = county.find('a', href=True)
        url = row.get('href')
        parsed = up.urlparse(url)
        code = up.parse_qs(parsed.query)['countyId']
        countyCode = code[0]

        # Get Precincts Reported
        reported = county.find('td', class_='statscell statscellnumber').text
        numReported = int(reported)
        numReported = 500 # take out

        # print(numReported, " < ", len(precinctsReported))
        # Compared # of precincts currently reported to # previously reported
        if numReported > len(precinctsReported[int(countyCode)]): # look up syntax for this
            # Call PrecinctCodes helper function
            precinctsUpdated = precinctCodes(countyCode, precinctsReported[int(countyCode)])

            # Call MyScraper
            if(len(precinctsUpdated) > 0):
                resultsScraper(countyCode, precinctsUpdated)
            # Append new list of precincts to array
            # numpy.insert(precinctsReported, countyCode, precinctsUpdated)
    conn.commit()



print("Time:", time.time() - start_time)
cur.close()
conn.close()