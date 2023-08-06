import asyncio
import math

MAX_IPs_PER_BATCH = 100

# API says max is 15 every 60 seconds, which translates to 1 every 4 seconds. Using 5 just to have some wiggle room.
SECONDS_BETWEEN_REQUESTS = 5


async def worker(id, seconds_before_wake):
    await asyncio.sleep(seconds_before_wake)
    print(f"Worker {id} working!")
    return

async def sleeper_runner(tasks_needed):
    tasks = []
    seconds_before_wake = 0
    for id in range(tasks_needed):
        tasks.append(asyncio.create_task(worker(id+1, seconds_before_wake)))
        seconds_before_wake += SECONDS_BETWEEN_REQUESTS
    print(f"Starting workers")
    await asyncio.gather(*tasks)

def main(ips=100):
    queries_needed = math.ceil(ips / MAX_IPs_PER_BATCH)
    print(f"About to run with {ips} IPs. Going to need {queries_needed} queries")
    asyncio.run(sleeper_runner(queries_needed))

if __name__ == "__main__":
    main()