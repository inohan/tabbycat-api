import sys
import os
import asyncio
import dotenv
import tabbycat_api as tabbycat
from tabbycat_api.utils.verify_feedbacks import RoundFeedbackOverview

# Load the environment variables
dotenv.load_dotenv()

TABBYCAT_URL = os.getenv("TABBYCAT_URL")
TABBYCAT_TOKEN = os.getenv("TABBYCAT_TOKEN")
TABBYCAT_SLUG = os.getenv("TABBYCAT_SLUG")

async def main():
    client =tabbycat.Client(
        TABBYCAT_URL,
        TABBYCAT_TOKEN,
        TABBYCAT_SLUG,
        cache=tabbycat.SimpleClientCache()
    )
    round_seq = 3
    tournament = await client.get_tournament()
    await client.get_teams()
    await client.get_adjudicators()
    round = await client.get_round(round_seq)
    round_pairings = await round._links.pairing.fetch()
    feedbacks = await client.get_feedbacks([round_seq])
    
    await asyncio.gather(
        tournament._links.preferences.fetch()
    )
    pref_adj_target = next(pref for pref in tournament._links.preferences if pref.identifier=="feedback__feedback_paths")
    pref_team_target = next(pref for pref in tournament._links.preferences if pref.identifier=="feedback__feedback_from_teams")
    overview = RoundFeedbackOverview.get(
        round=round,
        feedbacks=feedbacks,
        pref_teams=pref_team_target.value,
        pref_adjs=pref_adj_target.value
    )
    print("========")
    print(overview.okay)
    for pairing_overview in overview.pairing_statuses:
        print("=========")
        print(pairing_overview.pairing.id)
        print(f"Missing: {pairing_overview.missing}")
        print(f"Extra: {pairing_overview.extra}")
        print(f"Orallist: {pairing_overview.orallist}")
        print(f"Okay: {pairing_overview.okay}")

if __name__ == "__main__":
    asyncio.run(main())