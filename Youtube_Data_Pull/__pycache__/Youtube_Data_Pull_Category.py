from __future__ import print_function
import httplib2
import os
import pandas as pd
import sys
import csv
import datetime

from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client.client import flow_from_clientsecrets

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
def Data_pull():
    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'

    def get_authenticated_service():
        flow=flow_from_clientsecrets(CLIENT_SECRETS_FILE,scope=SCOPES)
        storage=Storage("%s-oauth2.json"% sys.argv[0])
        credentials=storage.get()
        if credentials is None or credentials.invalid:
            credentials=tools.run_flow(flow,storage)
        return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

    def print_response(response):
        print(response)

    # Build a resource based on a list of properties given as key-value pairs.
    # Leave properties with empty values out of the inserted resource.
    def build_resource(properties):
        resource = {}
        for p in properties:
            prop_array = p.split('.')
            ref = resource
            for pa in range(0, len(prop_array)):
                is_array = False
                key = prop_array[pa]

          # For properties that have array values, convert a name like
          # "snippet.tags[]" to snippet.tags, and set a flag to handle
          # the value as an array.
                if key[-2:] == '[]':
                    key = key[0:len(key)-2:]
                    is_array = True

                if pa == (len(prop_array) - 1):
            # Leave properties without values out of inserted resource.
                    if properties[p]:
                        if is_array:
                            ref[key] = properties[p].split(',')
                        else:
                            ref[key] = properties[p]
                elif key not in ref:
            # For example, the property is "snippet.title", but the resource does
            # not yet have a "snippet" object. Create the snippet object here.
            # Setting "ref = ref[key]" means that in the next time through the
            # "for pa in range ..." loop, we will be setting a property in the
            # resource's "snippet" object.
                    ref[key] = {}
                    ref = ref[key]
                else:
            # For example, the property is "snippet.description", and the resource
            # already has a "snippet" object.
                    ref = ref[key]
        return resource

    # Remove keyword arguments that are not set
    def remove_empty_kwargs(**kwargs):
        good_kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.items():
                if value:
                    good_kwargs[key] = value
        return good_kwargs

    def videos_list_most_popular(client, **kwargs):
      # See full sample for function
        kwargs = remove_empty_kwargs(**kwargs)
        response = client.videos().list(**kwargs).execute()
        return response

    """def video_categories_list_for_region(client, **kwargs):
      # See full sample for function
        kwargs = remove_empty_kwargs(**kwargs)
        response = client.videoCategories().list(
        **kwargs).execute()
        return response"""


    if __name__ == '__main__':
        regions=['US']
        for region in regions:
            filename=region+'6'+'.csv'
            with open (filename,'w',newline='') as fp:
                client = get_authenticated_service()
                os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
                url='https://www.youtube.com/watch?v='
                t=datetime.datetime.now()
                str(t)
                time=t.strftime("%Y-%m-%d %H:%M")
                work=csv.writer(fp)
                work.writerow(['title','ChannelTitle','url','published_At','DataGenerated_At','category_Id','category_title','view_Count', 'like_Count', 'dislike_Count', 'favorite_Count', 'comment_Count'])

                '''category_list=video_categories_list_for_region(client,
                part='snippet',
                hl='en_US',
                regionCode='US')'''
                #cate={'1': 'Film & Animation', '2': 'Autos & Vehicles', '10': 'Music', '15': 'Pets & Animals', '17': 'Sports', '18': 'Short Movies', '19': 'Travel & Events', '20': 'Gaming', '21': 'Videoblogging', '22': 'People & Blogs', '23': 'Comedy', '24': 'Entertainment', '25': 'News & Politics', '26': 'Howto & Style', '27': 'Education', '28': 'Science & Technology', '29': 'Nonprofits & Activism', '30': 'Movies', '31': 'Anime/Animation', '32': 'Action/Adventure', '33': 'Classics', '34': 'Comedy', '35': 'Documentary', '36': 'Drama', '37': 'Family', '38': 'Foreign', '39': 'Horror', '40': 'Sci-Fi/Fantasy', '41': 'Thriller', '42': 'Shorts', '43': 'Shows', '44': 'Trailers'}
                cate={'1': 'Film & Animation', '2': 'Autos & Vehicles', '10': 'Music', '15': 'Pets & Animals', '17': 'Sports','19': 'Travel & Events', '20': 'Gaming','22': 'People & Blogs', '23': 'Comedy', '24': 'Entertainment', '25': 'News & Politics', '26': 'Howto & Style', '27': 'Education', '28': 'Science & Technology', '29': 'Nonprofits & Activism'}
                for cate_id,cate_title in cate.items():
                    Res=videos_list_most_popular(client,
                    part='snippet,contentDetails,statistics',
                    chart='mostPopular',
                    regionCode=region,
                    videoCategoryId=cate_id,
                    #maximum is 50
                    maxResults=50)
                    for value in Res['items']:
                            work.writerow([value['snippet']['title'],value['snippet']['channelTitle'],url+value['id'],value['snippet']['publishedAt'],time,cate_id,cate_title]+list(value['statistics'].values())[:])
        print("Imported data successfully from youtube")
Data_pull()
