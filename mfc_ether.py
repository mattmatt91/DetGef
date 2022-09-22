

import asyncio
from mfc import FlowController

ip = '192.168.2.100'
async def get():
    async with FlowController(ip) as fc:
        print(await fc.get())

async def set_gas(val):
    async with FlowController(ip) as fc:
        print(await fc.set_gas(val))
        await fc.open()
        

val  = 10
asyncio.run(set_gas('N2'))
asyncio.run(get())
asyncio.run(set_gas('Air'))
asyncio.run(get())

