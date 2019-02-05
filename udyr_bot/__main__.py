from .client import create_client
from .constants import DISCORD_BOT_TOKEN


def main():
    print('Creating bot')
    client = create_client()
    print('Starting bot')
    client.run(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    main()
