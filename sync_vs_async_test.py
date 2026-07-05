import asyncio
import aiohttp

async def get_date(i: int, pat: str):
    url = f'http://127.0.0.1:8000/{pat}/{i}'
    print(f'Начал выполнение {i}')
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(f'Закончил выполнение {i}')

async def main():

    await asyncio.gather(
        *[get_date(i+1, 'sync') for i in range(300)]
    )

if __name__ == '__main__':
    asyncio.run(main())


#Проверка синхронности - в основной код
# import time
# import asyncio
# @app.get('/sync/{id}')
# def sync_func(id: int):
#     с = time.time()
#     print(f'sync. Начал {id}: {с:.2f}')
#     time.sleep(3)
#     print(f'sync. Закончил {id}: {(time.time() - с):.2f}')
#
#
# @app.get('/async/{id}')
# async def async_func(id: int):
#     с = time.time()
#     print(f'async. Начал {id}: {time.time():.2f}')
#     await asyncio.sleep(3)
#     print(f'async. Закончил {id}: {(time.time() - с):.2f}')

