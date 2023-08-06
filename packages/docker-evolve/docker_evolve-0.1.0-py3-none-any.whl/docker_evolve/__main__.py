
import argparse
import logging
import subprocess
import docker, docker.errors

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument('--name', help='The container name.', required=True)
parser.add_argument('--base-image', help='The container base image to start from if the container does not already exist.')


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    args, unknown_args = parser.parse_known_args()
    client = docker.Client()
    try:
        client.inspect_container(args.name)
    except docker.errors.NotFound:
        logger.info("Container %s does not exist", args.name)
        if not args.base_image:
            parser.error(f"missing --base-image option because container \"{args.name}\" does not exist")
        image_id = args.base_image
    else:
        logger.info("Commit image from container %s.", args.name)
        image_id = client.commit(args.name, "docker-evolve--" + args.name, "latest", "Evolve docker container.")["Id"]
        logger.info("Commited image ID is %s", image_id)

        logger.info("Stopping container %s.", args.name)
        client.stop(args.name)

        logger.info("Deleting container %s.", args.name)
        client.remove_container(args.name)

    logger.info("Creating new container %s from %s.", args.name, image_id)
    command = ["docker", "run", "-d", "--name", args.name] + unknown_args + [image_id, "tail", "-f", "/dev/null"]
    logger.info("$ %s", command)
    subprocess.check_call(command)


if __name__ == '__main__':
    main()
