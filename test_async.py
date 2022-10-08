import asyncio
from time import sleep



async def main():
    print( 'starting')
    task = asyncio.create_task(foo(1))
    # await task # waits until task is finished
    value = await task
    print( 'finished', value)

async def foo(num):
    # print(num)
    await asyncio.sleep(1)
    return num*5

asyncio.run(main())
# print('finished')