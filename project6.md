# Deliverable

## Features

#### 1. Hosting on DigitalOcean ([online](http://138.197.36.61:8000/))

The site was hosted on DigitalOcean in a droplet. The droplet runs an instance of docker and hosts all containers required to run the site. Initially the smaller droplets were running out of memory, so a larger droplet was used (Ubuntu 16.04.1 2GB Memory / 20GB Disk).

To securely host the site on DigitalOcean, the admin pages were removed and `DEBUG = False` was set on all three apps. A new docker-compose file, [`docker-compose.digital-ocean.yml`](docker-compose.digital-ocean.yml) was created to avoid exposing more than the web port (the exact differences vs the original file can be seen [here](https://www.diffchecker.com/8lrDoG87)).

#### 2. Continuous Integration [![Build Status](https://travis-ci.org/ajvarshneya/nomad.svg?branch=master)](https://travis-ci.org/ajvarshneya/nomad)

Travis CI was configured for the project to run tests in the model, exp, and web layers (including the Selenium tests) on each push. The full configuration is in the [`.travis.yml`](.travis.yml) file. To allow the fixture data to be fully loaded into the database and elastic search, a 60 second wait was added to `before_script`.

To help keep a (semi) clean git history, the base `.travis.yml` file was created in [another repository](https://github.com/sdgennari/cs4501-isa-project) so that the [many initial failures](https://travis-ci.org/sdgennari/cs4501-isa-project/builds) from Travis and Docker config issues would not be present in the build history.

#### 3. Integrations Tests (Selenium)

Integration tests were added with Selenium. The web container linked to a standalone selenium container running a Chrome browser. This allowed the [unit tests in the web app (in the `tests.py` file)](web-app/nomad/web/tests.py) to access Selenium.

The relevant lines in `docker-compose.yml` were:
```yaml
web:
    links:
        - selenium
        ...
    ...
    environment:
        SELENIUM_HOST: http://selenium:4444/wd/hub
        TEST_SELENIUM: 'yes'

selenium:
    image: selenium/standalone-chrome
    ports:
        - "4444:4444"
```

## Updated docker-compose

There were two major updates to `docker-compose.yml`: the addition of a selenium container for testing and the creation of a deployment docker-compose file, `docker-compose.digital-ocean.yml`. The details of each update are described above in the [Features](#features) section above.


## Link to github code

The relevant git commits for Project 6 are: `33731f0` - `219f2e6`. Again, the primary code changes are broken down by feature above in the [Features](#features) section above.


## Sample output

The continuous integration output logs are available on [Travis CI](https://travis-ci.org/ajvarshneya/nomad/builds/180229656).


## Command lines

The integration tests were added to the `web` container, so they can be run in the container via the standard `python manage.py test` command.

## DigitalOcean link

The DigitalOcean droplet can be accessed [here](http://138.197.36.61:8000/).