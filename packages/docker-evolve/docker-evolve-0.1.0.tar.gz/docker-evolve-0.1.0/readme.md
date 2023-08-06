# docker-evolve

Keep evolving a container's state to effectively use it as a constant subsystem.

## Usage

Start with a new container:

    $ docker-evolve –-name ubuntu --base-image ubuntu -v $PWD:/host

Connect to the container as usual:

    $ docker exec -it ubuntu bash

After making changes that you want to persist but you need to update the container
configuration, for example to expose a port, pass the parameters to `docker-evolve`:

    $ docker-evolve --name ubuntu -v $PWD:/host -p 8090:8090

This will commit the container's current state and re-create it using the new image
and the specified arguments. Note how you can now skip the `--base-image` argument
because the container already exists.
