# movie_rating.py

Get the Rotten Tomatoes raiting for a movie

## Getting Started

With Docker installed, executing is as simple as building the container
and then running it:

    docker build -t movie_rating .

    docker run movie_rating --title 'Napoleon Dynamite' --api-key 'XXXXXX'

### OMDB API

This program using the OMDB API (http://www.omdbapi.com/) and needs an
API Key to work. Once you have an API key from OMDB you can make it
available to the program in 2 ways:

#### Environment Variable

If you set the `OMDB_API_KEY` environment variable in your shell, then
you can docker to use it when it runs the container:

    export OMDB_API_KEY=XXXXXX
    docker run -e OMDB_API_KEY movie_rating --title 'Guardians of the Galaxy'

#### Command Line Option

Or you can pass the API Key as part of the command line options:

    docker run movie_rating --title 'Shawshank Redemption' --api-key 'XXXXXX'

## Options

The following options can be passed on the command line:

### title (required)

This is the title of the movie you are trying to find the rating of.

### year

This is the year of the movie in case there are multiple movies with the
same title.

### api-key

If you don't specify the API key in the environment, then it must be
given here.

## Running the tests

Just like running the movie_rating program, except you must pass the
API Key as an environment variable. Then you override the entrypoint to
be `pytest`

    docker run -e OMDB_API_KEY --entrypoint pytest movie_rating

## Development

While developing the movie_rating, it's useful to be able to run the
script in a shell in the container. This is done easily enough with
`docker run`:

    docker run -it --rm --entrypoint /bin/sh -e OMDB_API_KEY -v $PWD:/usr/src/app move_ratings
    /usr/src/app # ./movie_rating.py --title 'Guardians of the Galaxy'

## Built With

* Python3
* Docker

## Authors

* **Michael Peters** - [mpeters](https://github.com/mpeters)

## License

This project is licensed under the MIT License.

