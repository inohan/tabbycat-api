import sys
import os
import asyncio
import dotenv
import tabbycat_api as tabbycat

# Load the environment variables
dotenv.load_dotenv()

TABBYCAT_URL = os.getenv("TABBYCAT_URL")
TABBYCAT_TOKEN = os.getenv("TABBYCAT_TOKEN")
TABBYCAT_SLUG = os.getenv("TABBYCAT_SLUG")

async def main():
    client =tabbycat.Client(
        TABBYCAT_URL,
        TABBYCAT_TOKEN,
        TABBYCAT_SLUG
    )
    pref = await client.get_ballots(round_seq=5, debate_pk=44)
    print(pref)

if __name__ == "__main__":
    asyncio.run(main())