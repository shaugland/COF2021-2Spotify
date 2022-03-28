import os
import spotipy
import spotipy.util as util
import json
from json.decoder import JSONDecodeError
from countryCodes import * 
import xlsxwriter
import geopandas
from iso3166 import countries

class Country: 
    def __init__(self, name, playlists, spotify): 
        self.country_code_2 = name
        self.country_code_3 = ''
        self.full_country = ''

        self.danceabilityTotal = 0
        self.energyTotal = 0
        self.loudnessTotal = 0
        self.speechinessTotal = 0
        self.acousticnessTotal = 0
        self.instrumentTotal = 0
        self.livenessTotal = 0
        self.valenceTotal = 0
        self.tempoTotal = 0

        self.totalTracks = 0

        self.spotify = spotify

        self.AddPlaylistData(playlists)
        self.CalculateAverage()
        self.GetCountryCode()

        
        

    def AddPlaylistData(self, playlists):
        for playlist in playlists:
            try:
                playlistTracks = self.spotify.playlist_items(playlist['id'], fields='items(track(id))')['items']
            except Exception as e:
                print("something happened")
            trackIds = []
            for track in playlistTracks:
                if (track['track'] != None):
                    trackIds.append(track['track']['id'])
            try: 
                features = self.spotify.audio_features(trackIds)
            except: 
                break
            
            for feature in features:
                if feature == None:
                    break
                try: 
                    self.danceabilityTotal += feature['danceability']
                    self.energyTotal += feature['energy']
                    self.loudnessTotal += feature['loudness']
                    self.speechinessTotal += feature['speechiness']
                    self.acousticnessTotal += feature['acousticness']
                    self.instrumentTotal += feature['instrumentalness']
                    self.livenessTotal += feature['liveness']
                    self.valenceTotal += feature['valence']
                    self.tempoTotal += feature['tempo']

                    self.totalTracks += 1
                except Exception as e: 
                    print(e)
                # break
        print("done calculating playlist")
    

    def CalculateAverage(self):
        self.danceabilityAvg = self.danceabilityTotal / self.totalTracks
        self.energyAvg = self.energyTotal / self.totalTracks
        self.loudnessAvg = self.loudnessTotal / self.totalTracks
        self.speechinessAvg = self.speechinessTotal / self.totalTracks
        self.acousticnessAvg = self.acousticnessTotal / self.totalTracks
        self.instrumentAvg = self.instrumentTotal / self.totalTracks
        self.livenessAvg = self.livenessTotal / self.totalTracks
        self.valenceAvg = self.valenceTotal / self.totalTracks
        self.tempoAvg = self.tempoTotal / self.totalTracks

    def GetAverages(self):
        return {
            "danceability": self.danceabilityAvg,
            "energy": self.energyAvg,
            "loudness": self.loudnessAvg,
            "speechiness": self.speechinessAvg,
            "acousticness": self.acousticnessAvg,
            "instrumentalness": self.instrumentAvg,
            "liveness": self.livenessAvg,
            "valence": self.valenceAvg,
            "tempo": self.tempoAvg
        }

    def GetCountryCode(self):
        # country_codes = getData()
        # for country in country_codes:
        #     if country == self.country_code_2:
        #         self.full_country = country_codes[country]    # full_country is the countries full name
        #         break 

        # if self.full_country == '':
        #     self.full_country = ''
        #     print(f'Could not get country name for: {self.country_code_2}')
        #     return


        # world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

        # # Get the 3 digit world code for what the country is.
        # for country in world.values:
        #     if country[2] == self.full_country:  # country[2] is the world['name'] which is the full country's name
        #         self.country_code_3 = country[3]
        #         break



        # if self.country_code_3 == '':
        #     print('Could not get 3 digit code for: ' + self.country_code_2)


        country = countries.get(self.country_code_2)
        self.full_country = country.name
        self.country_code_3 = country.alpha3