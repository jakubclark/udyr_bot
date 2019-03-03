from logging import INFO, basicConfig

from .client import Client
from .constants import DISCORD_BOT_TOKEN


def main():
    client = Client()
    basicConfig(level=INFO,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%d-%m %H:%M:%S')
    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
