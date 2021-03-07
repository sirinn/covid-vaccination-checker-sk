import asyncio
import aiohttp
import json

async def request():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://mojeezdravie.nczisk.sk/api/v1/web/get_all_drivein_times_vacc') as response:

            raw = await response.text()
            payload = json.loads(raw)
            stations = payload['payload']

            for station in stations:
                # 77 is Kosice
                if station['county_id'] == '77':
                    capacity = free_capacity(station)
                    if capacity > 0:
                        print("Found free capacity of size: {} in {} ".format(capacity, station['title']))

def free_capacity(station):
    free = 0
    for date in station['calendar_data']:
        free =+ date['free_capacity']
    return free

async def checker(loop):
    # you could use even while True here
    while loop.is_running():
        await request()
        # sleep for 10 minutes, conservative checking to not spam the server (no rate-limit for some reason)
        await asyncio.sleep(60*10)

async def healthcheck(loop):
    while loop.is_running():
        # healthcheck each 5min
        await asyncio.sleep(60)
        print("Still alive")

ev_loop = asyncio.get_event_loop()
ev_loop.create_task(checker(ev_loop))
ev_loop.create_task(healthcheck(ev_loop))
ev_loop.run_forever()
