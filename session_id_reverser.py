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
print(ASCII_ART)
print()

# Get potential values forming the session ID
user_id = input(f"Enter the user ID: ").strip()
user_name = input(f"Enter the username: ").strip()
user_email = input(f"Enter the user email: ").strip()

start_timestamp = int(input(f"Enter the first possible unix timestamp / seqential number: ").strip())
end_timestamp = int(input(f"Enter the last possible unix timestamp / seqential number: ").strip())
print()

# Get the target SessionID to match
target_hash = input(f"Enter the searched SessionID to match: ").strip()
print()

# All petential delimiters for the session ID
delimiters = ", ; . : - _ / \\ ! § $ % & ( ) [ ] { } = ? ' \" + * # @ ~ ^ < > |".split(" ")
delimiters.append("") # Add empty string to delimiters for concatenation without a delimiter

# Generate all possible session IDs based on the user input
for timestamp in range(start_timestamp, end_timestamp + 1):
    print(f"TESTING # {timestamp}", end="\r")
    sys.stdout.flush()

    # Create a list of all value combinations to permute
    all_vals = [] 
    tmp = [user_id, user_name, user_email, str(timestamp)]

    # Single values
    all_vals.append([user_id])
    all_vals.append([user_name])
    all_vals.append([user_email])
    all_vals.append([str(timestamp)])
    
    # Combinations of two values
    for i in range(len(tmp)):
        for j in range(len(tmp)):
            if i != j:
                all_vals.append([tmp[i], tmp[j]])

    # Combinations of three values
    for i in range(len(tmp)):
        for j in range(len(tmp)):
            for k in range(len(tmp)):
                if i != j and j != k and i != k:
                    all_vals.append([tmp[i], tmp[j], tmp[k]])

    # All four values together
    all_vals.append(tmp)

    # Test all permutations of all value combinations with all delimiters
    for vals in all_vals:
        for delimiter in delimiters:
            for perm in permutations(vals):
                session_id = delimiter.join(perm)

                res = check_hashes(session_id)
                if res:
                    print(f"{Fore.GREEN}{res}{Style.RESET_ALL}\n")
                    sys.exit(0)

print(f"TESTING ... DONE! \n\n{Fore.RED}No matching session ID found :({Style.RESET_ALL}")
print()
sys.exit(1)

