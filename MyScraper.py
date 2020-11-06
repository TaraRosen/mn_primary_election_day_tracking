# import libraries
from requests import get
from bs4 import BeautifulSoup
import csv
from time import time
import re

countyid = '4'

# MAX OF 253 PRECINCTS
# precincts = '1219427,1219428,1219429,1219430,1219431,1219432,1219433,1219812,1219434,1219435,1219436,1219437,1219438,1219439,1219440,1219813,1219441,1219442,1219443,1219444,1219445,1219446,1219447,1219814,1219815,1219448,1219449,1219450,1219451,1219452,1219816,1219817,1219453,1219454,1219455,1219456,1219457,1219458,1219459,1219460,1219461,1219462,1219463,1219464,1219465,1219466,1219467,1219468,1219469,1219470,1219471,1219472,1219825,1219473,1219474,1219475,1219476,1219831,1219477,1219478,1219826,1219479,1219480,1219481,1219482,1219483,1219484,1219485,1219486,1219487,1219488,1219489,1219490,1219822,1219491,1219492,1219823,1219493,1219494,1219824,1219495,1219496,1219497,1219498,1219499,1219500,1219501,1219502,1219503,1219504,1219505,1219506,1219507,1219508,1219509,1219510,1219511,1219512,1219513,1219514,1219515,1219516,1219517,1219518,1219519,1219520,1219832,1219521,1219522,1219523,1219524,1219525,1219526,1219527,1219528,1219529,1219530,1219531,1219532,1219533,1219534,1219535,1219536,1219537,1219538,1219539,1219540,1219541,1219542,1219543,1219544,1219545,1219546,1219547,1219548,1219549,1219550,1219551,1219552,1219553,1219554,1219555,1219556,1219557,1219558,1219559,1219560,1219561,1219562,1219563,1219564,1219565,1219566,1219567,1219568,1219569,1219570,1219571,1219572,1219573,1219574,1219575,1219576,1219577,1219578,1219579,1219580,1219581,1219582,1219583,1219584,1219585,1219841,1219586,1219587,1219819,1219588,1219589,1219590,1219591,1219592,1219593,1219594,1219595,1219596,1219597,1219833,1219598,1219599,1219600,1219601,1219602,1219603,1219604,1219605,1219606,1219607,1219842,1219608,1219609,1219610,1219611,1219612,1219613,1219614,1219615,1219616,1219834,1219835,1219836,1219617,1219618,1219619,1219620,1219621,1219622,1219623,1219624,1219625,1219626,1219627,1219628,1219629,1219630,1219631,1219632,1219837,1219633,1219634,1219635,1219636,1219637,1219638,1219639,1219640,1219827,1219641,1219642,1219643,1219644,1219645,1219646,1219647,1219648,1219649,1219650,1219651,1219652,1219653,1219654,1219655,1219656,1219657'
precincts = '1218548'

start_time = time()

# specify the url with 'countyid' and 'precincts'
response = get('https://electionresults.sos.state.mn.us/Results/PrecinctListResults/115?countyid=' + countyid + '&precincts=' + precincts)

# parse the html using beautiful soup and store in variable `soup`
# pip3 install lxlm
soup = BeautifulSoup(response.text, 'lxml')


# Selects starting area in html at 'center'
center = soup.find('center')

# Creates list of precinct names
precinct_containers = soup.find_all('div', class_='resultgroupheader')
# sets iterator at 1 to skip "Results for Selected Precincts in Hennepin County"
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
        rowentry = precinct_containers[pnum].text.strip() + "\t" + office_name

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
                        rowentry += "\t"
                        rowentry += ele
                    print(rowentry)
    # Updates to next precinct once iterated through entire table
    pnum += 1

print("Time: ", time() - start_time)