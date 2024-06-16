import include.Inbox as Inbox
import asyncio


async def main():
    await Inbox.add_message(
        email="sanjaysagarlearn@gmail.com",
        title="This is a Big mail",
        message="hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inboxhey can you see the message 1 in inboxhey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inboxhey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inboxhey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox hey can you see the message 1 in inbox",
    )


asyncio.run(main())
