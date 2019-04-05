#!/usr/local/bin/python
""" This script uses the OMDB API to print the Rotten Tomatoes score for a given movie"""
import argparse
import sys
from os import environ
import requests

OMDB_URL = "http://www.omdbapi.com/"
OMDB_TIMEOUT = 10

def get_rotten_tomatoes_rating(api_key, title, year=None):
    """Make get the rating from the OMDB data"""
    # search for the movie
    request_params = {"apikey": api_key, "v": 1, "type": "movie", "t": title}
    if year:
        request_params["y"] = year

    response_data = omdb_data(request_params)

    # was the movie found
    rt_rating = None
    if response_data['Response'] == 'True':
        # get the Rotten Tomatoes rating
        if 'Ratings' in response_data:
            for rating in response_data['Ratings']:
                if rating['Source'] == 'Rotten Tomatoes':
                    rt_rating = rating['Value']

    else:
        if response_data['Error'] == 'Movie not found!':
            if year:
                fatal("We're sorry, but a movie by that name ({}) in that year ({}) was not found".format(title, year))
            else:
                fatal("We're sorry, but a movie by that name ({}) was not found".format(title))

    return rt_rating


def fatal(msg):
    """Print the message to STDERR and then exit with non-zero error code"""
    print(msg, file=sys.stderr)
    sys.exit(1)

def omdb_data(params):
    """Make the API request to OMDB and return the JSON data"""
    # try to make the request
    try:
        req = requests.get(OMDB_URL, params=params)
    except requests.exceptions.Timeout:
        fatal("Sorry, we timed out trying to reach the OMDB API. Please check your network connection and try again later.")
    except requests.exceptions.ConnectionError:
        fatal("Sorry, we are having trouble reaching the OMDB API. Please check your network connection and try again later.")
    except requests.exceptions.RequestException as ex:
        fatal("Sorry, an unrecoverable error occurred: {}".format(ex))

    # handle some known error codes
    if req.status_code == 401:
        # handle 401s (bad api-key)
        fatal("Sorry, your API Key was not valid. Please check it and try again.")
    elif req.status_code == 503:
        fatal("Sorry, it seems like OMDB is busy. Please try again later.")
    elif req.status_code != 200:
        fatal("Sorry, there was some error communicating with the OMDB API: Error Code {}".format(req.status_code))

    # sanity check the response data
    response_data = req.json()
    if 'Response' not in response_data:
        fatal("Sorry, but the response from OMDB did not contain the expected data")

    return response_data


if __name__ == "__main__":
    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('--title', help='The title of the movie being looked up', required=True)
    ARG_PARSER.add_argument('--year', help='The year of the movie: useful if multiple movies with the title exist', required=False, type=int)
    ARG_PARSER.add_argument('--api-key', help='An OMDB API key. If not specified, will use the OMDB_API_KEY env variable', required=False)
    ARGS = ARG_PARSER.parse_args()

    # make sure we have an API key
    API_KEY = ARGS.api_key
    if not API_KEY:
        if environ.get('OMDB_API_KEY') is not None:
            API_KEY = environ.get('OMDB_API_KEY')
        else:
            fatal("You must provide an --api-key or have OMDB_API_KEY set in your environment")

    RATING = get_rotten_tomatoes_rating(API_KEY, ARGS.title, ARGS.year)
    if RATING:
        print(RATING)
    else:
        fatal("No Rotten Tomatoes rating was found for this movie")
