from time import time
from requests import get
from time import sleep
from IPython.core.display import clear_output
from bs4 import BeautifulSoup

# List to store codes in
counties = [27] # should be 88
print(counties)
precinctCodes = {}
countyURLS = {}
precinct_codes = ""
precinct_counter = 0

# Monitor the loop
start_time = time()
requests = 0

# For county Aitkin
for county in counties:

    # Specificy URL
    response = get('https://electionresults.sos.state.mn.us/Select/CountyPrecinctSelect/118?districtid=69')

    # pause the loop
    sleep(1)

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(response.text, 'html.parser')

    # Precinct list
    precinct_list = soup.find_all('option', class_='selOptNotReported', limit=254)

    for precinct in precinct_list:
        precinctCode = precinct.attrs['value']
        precinctName = precinct.text
        precinctCodes[precinctName] = precinctCode


        precinct_counter += 1
        precinct_codes += precinctName
        precinct_codes += ","
        precinct_codes += precinctCode
        precinct_codes += "\n"




    # Gets "Select Precincts in _______ County"

print(precinct_codes)

print(precinct_counter)


# 1218315, 1218316, 1218317, 1218318, 1218319, 1218320, 1218321, 1218367, 1218322, 1218323, 1218324, 1218325, 1218326, 1218327, 1218328, 1218329, 1218330, 1218368, 1218331, 1218332, 1218333, 1218334, 1218335, 1218336, 1218337, 1218338, 1218339, 1218340, 1218341, 1218342, 1218343, 1218344, 1218345, 1218346, 1218347, 1218348, 1218349, 1218350, 1218351, 1218352, 1218353, 1218354, 1218355, 1218356, 1218357, 1218358, 1218359, 1218360, 1218361, 1218362, 1218364, 1218365, 1218363, 1218366