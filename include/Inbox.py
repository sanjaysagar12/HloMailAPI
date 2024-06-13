from .MongoDB import MongoDB
import asyncio
import uuid
import json

# Initialize the database connection
db = MongoDB("admin", "users")
collection = db.get_connection()

# Function to add a message to the inbox
async def add_message(email, title, message):
    message_id = str(uuid.uuid4())
    result = await collection.update_one(
        {"email": email},
        {
            "$push": {
                "inbox": {
                    "_id": message_id,
                    "title": title,
                    "message": message,
                    "readed": False,
                }
            }
        },
    )
    return (
        {"added": True, "message_id": message_id}
        if result.modified_count > 0
        else {"added": False, "error": "no documents updated"}
    )

# Function to delete a message from the inbox
async def delete_message(email, message_id):
    result = await collection.update_one(
        {"email": email}, {"$pull": {"inbox": {"_id": message_id}}}
    )
    return (
        {"deleted": True}
        if result.modified_count > 0
        else {"deleted": False, "error": "no documents updated"}
    )

# Function to update the readed status of a message
async def update_readed_status(email, message_id, readed_status=True):
    result = await collection.update_one(
        {"email": email, "inbox._id": message_id},
        {"$set": {"inbox.$.readed": readed_status}},
    )
    return (
        {"updated": True}
        if result.modified_count > 0
        else {"updated": False, "error": "no documents updated"}
    )

# Function to get all messages in the inbox
async def get_all_messages_in_inbox(email):
    user = await collection.find_one({"email": email}, {"_id": 1, "inbox": 1})
    if user and "inbox" in user:
        return user["inbox"]
    else:
        return []

# Function to get message IDs and titles of all messages in the inbox
async def get_all_message_titles(email):
    user = await collection.find_one({'email': email}, {'_id': 1, 'inbox._id': 1, 'inbox.title': 1,'inbox.readed': 1})
    if user and 'inbox' in user:
        messages = [{'message_id': msg['_id'], 'title': msg['title'],'readed': msg['readed']} for msg in user['inbox']]
        return messages
    else:
        return []

# Function to get a particular message by message_id
async def get_message_by_id(email, message_id):
    user = await collection.find_one(
        {"email": email, "inbox._id": message_id},
        {"_id": 0, "inbox": {"$elemMatch": {"_id": message_id}}}
    )
    if user and "inbox" in user:
        return user["inbox"][0]
    else:
        return {}
# # Example usage
# async def main():
#     email = 'sanjaysagarlearn@gmail.com'  # Replace with the actual user email

#     # Add messages to the inbox
#     print(await add_message(email, "Test1", "Hello, this is a new message! T1"))
#     print(await add_message(email, "Test2", "Hello, this is a new message! T2"))
#     print(await add_message(email, "Test3", "Hello, this is a new message! T3"))
    
#     # Get all messages in the inbox
#     inbox = await get_all_messages_in_inbox(email)
#     print("Inbox:", inbox)

#     # Get only titles and message IDs of all messages in the inbox
#     message_titles = await get_all_message_titles(email)
#     print("Message Titles:", message_titles)

# # Run the example usage
# asyncio.run(main())
