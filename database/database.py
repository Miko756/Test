import asyncio
import motor.motor_asyncio
from time import time
from config import DB_URL, DB_NAME

# Concurrency control
semaphore = asyncio.Semaphore(10)



# Rate limiting tracker
user_requests = {}

# MongoDB client setup
try:
    dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
    database = dbclient[DB_NAME]
except Exception as e:
    print(f"Database connection error: {e}")

user_data = database['users']
admin_data = database['admins']
link_data = database['links']

async def rate_limit(user_id, limit_time=60):
    now = time()
    if user_id not in user_requests or now - user_requests[user_id] > limit_time:
        user_requests[user_id] = now
        return True
    return False

async def handle_file_request(user_id, hash):
    # Rate limiting check
    if not await rate_limit(user_id):
        return "Rate limit exceeded. Please try again later."

    # Concurrency control
    async with semaphore:
        await inc_count(hash)  # Increment click count safely
        # Fetch or generate file link
        return await get_file_link(hash)  # Function to retrieve the file link

# Example function to increment click count for a file
async def inc_count(hash: str):
    data = await link_data.find_one({'hash': hash})
    if data is None:
        return
    await link_data.update_one({'hash': hash}, {'$inc': {'clicks': 1}})
    
# Default verification status
default_verify = {
    'is_verified': False,
    'verified_time': 60,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

# Links

# Function to create a new link object
async def new_link(hash: str):
    return {
        'clicks': 0,
        'hash': hash
    }

# Function to generate a new count for a link
async def gen_new_count(hash: str):
    data = await new_link(hash)
    await link_data.insert_one(data)

# Function to check if a hash exists
async def present_hash(hash: str):
    found = await link_data.find_one({"hash": hash})
    return bool(found)

# Function to increment the click count for a hash
async def inc_count(hash: str):
    data = await link_data.find_one({'hash': hash})
    if data is None:
        return  # Handle case where the hash is not found
    clicks = data.get('clicks', 0)
    await link_data.update_one({'hash': hash}, {'$inc': {'clicks': 1}})

# Function to get the number of clicks for a hash
async def get_clicks(hash: str):
    data = await link_data.find_one({'hash': hash})
    if data is None:
        return 0  # Return 0 if the hash is not found
    return data.get('clicks', 0)

# Users

# Function to check if a user exists
async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

# Function to add a new user
async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)

# Function to get the verification status of a user
async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

# Function to update the verification status of a user
async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

# Function to get the full list of user IDs
async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

# Function to delete a user
async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})

# Admins

# Function to check if an admin exists
async def present_admin(user_id: int):
    found = await admin_data.find_one({'_id': user_id})
    return bool(found)

# Function to add a new admin
async def add_admin(user_id: int):
    user = new_user(user_id)
    await admin_data.insert_one(user)
    async with admins_lock:  # Ensure thread-safe operation on ADMINS
        ADMINS.append(int(user_id))

# Function to remove an admin
async def del_admin(user_id: int):
    await admin_data.delete_one({'_id': user_id})
    async with admins_lock:  # Ensure thread-safe operation on ADMINS
        ADMINS.remove(int(user_id))

# Function to get the full list of admin IDs
async def full_adminbase():
    user_docs = admin_data.find()
    user_ids = [int(doc['_id']) async for doc in user_docs]
    return user_ids
