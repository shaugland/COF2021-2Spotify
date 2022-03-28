import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from country import Country
import threading
import concurrent.futures
import xlsxwriter
import geopandas
from countryCodes import * 


def UpdateSongData():
    scope = "user-library-read"

    auth_manager = SpotifyClientCredentials()
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    sp = spotipy.Spotify(auth_manager=auth_manager)


    markets = sp.available_markets()

    countries = []
    def AppendCountry(market):
        print(f'{market} starting...')
        playlists = sp.featured_playlists(country=market)['playlists']['items']
        country = Country(market, playlists, sp)
        if (country.full_country != None):
            print(country.full_country + " successfully added")
        else:
            print(country.country_code_2 + " could not be added")
        try:
            countries.append(country)
        except Exception as e:
            print("could not append country")


    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(AppendCountry, markets['markets'])
        

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    # Writes a seperate worksheet for each feature
    features = [
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo"
    ]

    worksheets = []
    workbooks = []
    for item in features:
        workbook = xlsxwriter.Workbook("data/" + item + '.xlsx')
        workbooks.append(workbook)
        worksheets.append(workbook.add_worksheet(item))

    row = 1 # Used later for determining which row that the worksheets are on
    for sheet in worksheets:
        sheet.write(0, 0, 'Country Code')
        sheet.write(0, 1, 'data')

    iso_codes_used = [] 
    for country in countries: 
        sheet_num = 0
        for item in country.GetAverages():
            if country.country_code_3 == '':
                print('Could not find 3 digit ISO number so the country was not added')
                row -= 1 # Used so that another blank row isn't used
                break
            worksheets[sheet_num].write(row, 0, country.country_code_3) 
            worksheets[sheet_num].write(row, 1, country.GetAverages()[item]) 
            
            if sheet_num == 8:  # Places sheet number back to the danceability sheet when going over the number of features
                sheet_num = 0
            else:               # Increases what sheet to use from which feature.
                sheet_num += 1

        iso_codes_used.append(country.country_code_3) 

            
        print(f'Appended files for the country {country.full_country}')
        row += 1

    sheet_num = 0
    # Placing the iso codes that did not have any data for their countries
    for country in world.values:  # ISO codes are actually world.values[iso][3]
        # See if there is data for the code value
        iso_been_used = False
        for iso in iso_codes_used:
            if country[3] == iso:
                iso_been_used = True
                break

        if iso_been_used:
            # print(country[3] + ' has been used')
            continue
        # IF THE ISO HAS NO DATA: write in each worksheet a 0 for that country 3 digit code
        for worksheet in worksheets:
            worksheet.write(row, 0, country[3])
            worksheet.write(row, 1, 0)
        row += 1


    # Close each excel file
    print('closing workbooks...')
    for workbook in workbooks:
        workbook.close()