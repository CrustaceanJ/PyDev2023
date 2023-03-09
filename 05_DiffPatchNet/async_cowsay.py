import asyncio
from cowsay import cowsay, list_cows
from collections import defaultdict

clients = {}
clients_cows = {}

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    login = None
    quit = False
    while not reader.at_eof() and not quit:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                result = q.result().decode().strip()
                if result == 'quit':
                    quit = True
                    break
                if result.startswith('login'):
                    _, cowname = result.split()
                    if cowname in list_cows():
                        clients_cows[me] = cowname
                        await clients[me].put(f"{me} has loggined as {cowname}")
                        login = cowname
                    else:
                        await clients[me].put("Unknown cowname")
                elif result == 'who':
                    await clients[me].put(f"Authorized cows: {' '.join([name for name in clients_cows.values()] or ['noone authorized'])}")
                elif login:
                    if result.startswith('say'):
                        _, name, msg = result.split(maxsplit=2)
                        for to, cn in clients_cows.items():
                            if cn == name:
                                await clients[to].put(cowsay(msg, cow=login))
                    elif result.startswith('yield'):
                        _, msg = result.split(maxsplit=1)
                        for out in clients.values():
                            await out.put(cowsay(msg, cow=login))
                else:
                    await clients[me].put(f"You are not authorized. Please use: login cowname")                        
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                result = q.result()
                writer.write(f"{result}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    del clients_cows[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
