#!/usr/local/bin/python
import argparse
import requests
import sys
from os import environ

OMDB_URL = "http://www.omdbapi.com/"
OMDB_TIMEOUT = 10

def get_rotten_tomatoes_rating(api_key, title, year=None):
    # search for the movie
    request_params = {"apikey": api_key, "v": 1, "type": "movie", "t": title}
    if year:
        request_params["y"] = year

    response_data = omdb_data(request_params)

    # was the movie found
    if response_data['Response'] == 'True':
        # get the Rotten Tomatoes rating
        rt_rating = None
        if 'Ratings' in response_data:
            for rating in response_data['Ratings']:
                if rating['Source'] == 'Rotten Tomatoes':
                    rt_rating = rating['Value']

        return rt_rating
    else:
        if response_data['Error'] == 'Movie not found!':
            if year:
                fatal("We're sorry, but a movie by that name ({}) in that year ({}) was not found".format(title, year))
            else:
                fatal("We're sorry, but a movie by that name ({}) was not found".format(title))


def fatal(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def omdb_data(params):
    # try to make the request
    try:
        r = requests.get(OMDB_URL, params=params)
    except requests.exceptions.Timeout:
        fatal("Sorry, we timed out trying to reach the OMDB API. Please check your network connection and try again later.")
    except requests.exceptions.ConnectionError:
        fatal("Sorry, we are having trouble reaching the OMDB API. Please check your network connection and try again later.")
    except requests.exceptions.RequestException as e:
        fatal("Sorry, an unrecoverable error occurred: {}".format(e))

    # handle some known error codes
    if r.status_code == 401:
        # handle 401s (bad api-key)
        fatal("Sorry, your API Key was not valid. Please check it and try again.")
    elif r.status_code == 503:
        fatal("Sorry, it seems like OMDB is busy. Please try again later.")
    elif r.status_code != 200:
        fatal("Sorry, there was some error communicating with the OMDB API: Error Code {}".format(r.status_code))

    # sanity check the response data
    response_data = r.json()
    if 'Response' not in response_data:
        fatal("Sorry, but the response from OMDB did not contain the expected data")

    return response_data


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--title', help='The title of the movie being looked up', required=True)
    arg_parser.add_argument('--year', help='The year of the movie: useful if multiple movies with the title exist', required=False, type=int)
    arg_parser.add_argument('--api-key', help='An OMDB API key. If not specified, will use the OMDB_API_KEY env variable', required=False)
    args = arg_parser.parse_args()

    # make sure we have an API key
    api_key = args.api_key
    if not api_key:
        if environ.get('OMDB_API_KEY') is not None:
            api_key = environ.get('OMDB_API_KEY')
        else:
            fatal("You must provide an --api-key or have OMDB_API_KEY set in your environment")

    rating = get_rotten_tomatoes_rating(api_key, args.title, args.year)
    if rating:
        print(rating)
    else:
        fatal("No Rotten Tomatoes rating was found for this movie")
