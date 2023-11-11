import asyncio
import aiohttp
from more_itertools import chunked
from models import init_db, People, Session
import datetime

CHUNK_SIZE = 10


async def get_url(url, key, session):
    async with session.get(f'{url}') as response:
        data = await response.json()
        return data[key]


async def get_urls(urls, key, session):
    tasks = (asyncio.create_task(get_url(url, key, session)) for url in urls)
    for task in tasks:
        yield await task


async def get_data(urls, key, session):
    data_list = []
    async for el in get_urls(urls, key, session):
        data_list.append(el)
    return ', '.join(data_list)


async def paste_to_db(people):
    async with Session() as session:
        async with aiohttp.ClientSession() as as_session:
            for item in people:

                if item is not None:
                    person = People(
                                    # id=int(item['url'].split('/')[-2]),
                                    birth_year=item.get('birth_year'),
                                    eye_color=item.get('eye_color'),
                                    films=await get_data(item['films'], 'title', as_session),
                                    gender=item.get('gender'),
                                    hair_color=item.get('hair_color'),
                                    height=item.get('height'),
                                    homeworld=item.get('homeworld'),
                                    mass=item.get('mass'),
                                    name=item.get('name'),
                                    skin_color=item.get('skin_color'),
                                    species=await get_data(item['species'], 'name', as_session),
                                    starships=await get_data(item['starships'], 'name', as_session),
                                    vehicles=await get_data(item['vehicles'], 'name', as_session))
                    session.add(person)
                    await session.commit()


async def get_people(id, session):
    response = await session.get(f'https://swapi.dev/api/people/{id}')
    json = await response.json()
    if json == {'detail': 'Not found'}:
        return
    return json


async def main():

    await init_db()

    async with aiohttp.ClientSession() as session:

        for people_id_chunk in chunked(range(1, 100), CHUNK_SIZE):
            coros = [get_people(people_id, session) for people_id in people_id_chunk]

            result = await asyncio.gather(*coros)
            # await paste_to_db(result)

            asyncio.create_task(paste_to_db(result))

    tasks_to_await = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks_to_await)


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)



