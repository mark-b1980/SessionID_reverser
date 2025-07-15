import sys
import base64
import hashlib

from urllib.parse import quote
from colorama import Fore, Style
from itertools import permutations

ASCII_ART = f"""{Fore.RED}
 (                         (   (                                           
 )\ )                      )\ ))\ )                                        
(()/(   (      (          (()/(()/(    (     (   )     (  (        (  (    
 /(_)) ))\(  ( )\  (   (   /(_))(_))   )(   ))\ /((   ))\ )(  (   ))\ )(   
(_))  /((_)\ )((_) )\  )\ |_))(_))_   (()\ /((_|_))\ /((_|()\ )\ /((_|()\  
/ __|(_))((_|(_|_)((_)_(_/(_ _||   \   ((_|_)) _)((_|_))  ((_|(_|_))  ((_) 
\__ \/ -_|_-<_-< / _ \ ' \)) | | |) | | '_/ -_)\ V // -_)| '_(_-< -_)| '_| 
|___/\___/__/__/_\___/_||_|___||___/  |_| \___| \_/ \___||_| /__|___||_|   {Style.RESET_ALL}v.1.0
================================================================================
"""


def check_hashes(session_id):
    global ALLOWED_HASHES
    global target_hash

    for algo in ALLOWED_HASHES:
        try:
            hash_obj = hashlib.new(algo)
            hash_obj.update(session_id.encode('utf-8'))
            if hash_obj.hexdigest() == target_hash:
                return f'Found matching session ID: {algo}("{session_id}") == {target_hash}'
        except:
            pass
    
    # Check if hex encode of the session ID matches the target hash
    if session_id.encode('utf-8').hex() == target_hash:
        return f'Found matching session ID: HEX("{session_id}") == {target_hash}'

    # Chech if the session ID matches the ord numers for the target hash
    hash_obj = "".join([str(ord(c)) for c in target_hash])
    if session_id == hash_obj:
        return f'Found matching session ID: ORD("{session_id}") == {target_hash}'
    
    # Check if base64 encode of the session ID matches the target hash
    try:
        b64_encoded = base64.b64encode(session_id.encode('utf-8')).decode('utf-8')
        if b64_encoded == target_hash:
            return f'Found matching session ID: BASE64("{session_id}") == {target_hash}'
    except:
        pass

    # Check if urlencoding speciffic characters if the session ID matches the target hash
    try:
        url_encoded = quote(session_id)
        if url_encoded == target_hash:
            return f'FOUND MATHCING SESSION ID: URLENCODE("{session_id}") == {target_hash}'
    except:
        pass

    return False


# List all available algorithms in hashlib
ALLOWED_HASHES = hashlib.algorithms_available
print(ASCII_ART, end="\n\n")

# Get potential values forming the session ID
user_id = input(f"Enter the user ID: ").strip()
user_name = input(f"Enter the username: ").strip()
user_email = input(f"Enter the user email: ").strip()

start_timestamp = int(input(f"Enter the first possible unix timestamp / seqential number: ").strip())
end_timestamp = int(input(f"Enter the last possible unix timestamp / seqential number: ").strip())
print()

# Get the target SessionID to match
target_hash = input(f"Enter the searched SessionID to match: ").strip()

# All petential delimiters for the session ID
delimiters = ", ; . : - _ / \\ ! § $ % & ( ) [ ] { } = ? ' \" + * # @ ~ ^ < > |".split(" ")
delimiters.append("") # Add empty string to delimiters for concatenation without a delimiter

# Generate all possible session IDs based on the user input
for timestamp in range(start_timestamp, end_timestamp + 1):
    print(f"TESTING # {timestamp}", end="\r")
    sys.stdout.flush()

    vals = [user_id, user_name, user_email, str(timestamp)]
    for delimiter in delimiters:
        for perm in permutations(vals):
            session_id = delimiter.join(perm)

            res = check_hashes(session_id)
            if res:
                print(f"{Fore.GREEN}{res}{Style.RESET_ALL}\n")
                sys.exit(0)

print(f"{Fore.RED}TESTING ... DONE, no matching session ID found.{Style.RESET_ALL}")
sys.exit(1)

