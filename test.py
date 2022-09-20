

# get address from multimeter
# import visa
# rm = visa.ResourceManager()
# rm.list_resources()
import asyncio
from mfc import FlowController



async def get():
    async with FlowController('169.254.2.100') as fc:
        print(await fc.get())

asyncio.run(get())
# dsfgsdfgsdfgdfsdf