Developer Workflow Scripts
==========================

The scripts in this directory are intended to improve developer workflow when working with the
Docker toolchain. All scripts contain a help message outlining the purpose and usage of each
script, which can be accessed using the `--help` flag. The Docker ecosystem is vast and can be
quite complex, and these scripts are intended to get you kickstarted, but you likely will need to
use the `docker` and `docker-compose` commands directly at some point in the near future. The
[Docker docs](https://docs.docker.com/reference/) are your friend.

You can configure which Docker services are managed by these scripts by changing the
DEV_DOCKER_WORKFLOW variable in your .env file. Depending on this configuration some scripts will
act differently.

* full - application and dependency services are all run in Docker
* deps - only dependencies are run in Docker, devs are responsible for setting up application
environment
* none - Docker is not used at all, devs are responsible for setting up all dependencies.


setup
-----

This is the script intended to prepare your system by installing the Docker toolchain and building
the images and restoring a fresh database for the project. Due to the installation process for Mac,
you should run `setup_docker` first.

Supported Workflows: `full`, partial for `deps`

setup_docker
------------

This script will install Docker and docker-compose. On Linux systems this is called as part of the
`setup` script and does not need to be run separately. For Mac, this script should be run before
running `setup`.

Supported Workflows: `full`, `deps`

start
-----

This script should be used to launch the services to run the project. The output of the command for
each service will be output together in the resulting screen. Pressing `ctrl-c` will cause all the
services here to be stopped.

You may, optionally, provide service names to only launch specific services.

If you provide the `-d` flag to detach from the services and run them in the background and you'll
be returned to your shell. You can use the `attach` script to connect to all or specific services
at any time. You will need to use the `stop` script to stop services that are detached.

Supported Workflows: `full`, partial for `deps`

stop
----

This script will stop all or specfic services, whether they are detached or attached in another
terminal.

Supported Workflows: `full`, partial for `deps`

update
------

This script is intended to be run when pulling down a large changeset, i.e. pulling a new branch or
latest main branch. It will rebuild your images and containers, install new requirements, and run
migrations.

Supported Workflows: `full`, `deps`, `none`

install
-------

This is intended to abstract away a large number of complexities when working with the project. You
should specify whether you installing a Python (py) or System (apt) package and this script will
take the appropriate steps to make sure the package is installed and added to the correct
requirements file. You can provide the `--dev` and `--no-save` flags to modify this functionality
as needed.

Supported Workflows: `full`, partial for `deps` and `none`

migrate
-------

Use this script to abstract some complexities in managing migrations. When run directly, the `run`
command is assumed and migrations will be run, but you can also use the `make` and `show` commands
to create and list migrations. Most options for equivalent Django commands should translate
directly, when provided after the command.

Supported Workflows: `full`, `deps`, `none`

test
----

This will run the unittesting suite. Any additional args passed to this command are passed directly
to the test runner.

Supported Workflows: `full`, `deps`, `none`

console
-------

This will allow you to connect to the services via the appropriate interactive console. Currently
supported are `bash` to use bash on the primary web service, `sudo` to use bash as sudo, `python`
to use Django's shell_plus command, and `sql` to get a SQL console.

Supported Workflows: `full`, partial for `deps` and `none`

attach
------

This can be used to attach to a specific service's output console. Whether it's running in detached
mode or you simply want to see that services output by itself in a separate terminal.

Supported Workflows: `full`, partial for `deps`

restore_db
----------

This will destroy any existing database container you have running and restore it using restore
files located in `docker/init/db`. The restore files **must** exist for this script to run.

All migrations in your current checkout of the codebase will be run at the end of the restore
unless using the `--no-migrate` flag.

Supported Workflows: `full`, `deps`

manage
------

This is simply a convenience command which calls Django's `manage.py` command in the appropriate
environment based on selected dev workflow and passes all arg to the command.

Supported Workflows: `full`, `deps`, `none`

cleanup
-------

This can be used to cleanup a working environment. It will delete any cache files (.pyc) and drop
the static build and Redis cache volumes, in an attempt to remove anything that may be causing odd
behavior. It's generally better to just run `update` which includes this script, but this can
sometimes be a quick fix for weirdness.

Docker also will also create new images and volumes relatively often. Generally you want to keep
these around for a little so that rebuilding between branches is quicker due to Docker using this
cache. However, this takes up a large amount of space on your system and it's recommended to
occasionally run `cleanup --docker` to also remove any Docker artifacts that are no longer used,
freeing up space on your system

Supported Workflows: `full`, `deps`, partial for `none`

teardown
--------

This will utterly and completely destroy your Docker environment, including all build files and
database volumes. There should never be any side affects outside of that environment, which can be
rebuilt using `setup`, but you will be waiting a while for it to rebuild.

Supported Workflows: `full`, `deps`

tools
-----

This contains several utility functions which are used in most of the other scripts. Nothing of
practical use otherwise.

run_util
--------

This script will allow you to run certain, short lived, utilities that are not strictly needed for
running or developing the application, but can sometimes come in handy. See the help text of this
command to see all available utilities.

### flower

This starts a web-based tool for monitoring Celery. It's recommended that you set `FLOWER_PORT` in
your .env file to expose the service on a non-random port.

Supported Workflows: `full`, `deps`

### dbadmin

Adminer is a web-based tool for monitoring and managing databases. On pageload the default
credentials shoul dbe pre-populated.

Supported Workflows: `full`, `deps`

### dbdump

This will dump the contents of the database to a file. By default it only dumps the `base_app`
database to a gzipped file.

Supported Workflows: `full`, `deps`, `none`
