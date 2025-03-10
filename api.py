import asyncio
from autogenstudio.teammanager import TeamManager

async def main():
    manager = TeamManager()

    response = await manager.run(
        team_config="team.json",
        task="Write a short story of bird.",
    )

    print(response)

asyncio.run(main())