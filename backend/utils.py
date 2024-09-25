import hashlib
import os

def create_hash(text):
    """Generate a unique hash value for the given text data."""
    
    # Convert the string into bytes
    text_bytes = text.encode('utf-8')
    
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256()
    
    # Update the hash object with the bytes
    hash_object.update(text_bytes)
    
    # Get the hexadecimal representation of the hash
    hash_hex = hash_object.hexdigest()
    
    return hash_hex


def check_file_exists(folder, filename):
    """Check if a certain file exists in the given folder."""
    
    # Create the full file path
    file_path = os.path.join(folder, filename)
    
    # Check if the file exists
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return True
    else:
        return False
    
def save_to_cache(filename, data, CACHE_DIR):
    """Save the given string to a text file acting as a cache."""
    
    # Create cache directory if it doesn't exist
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    
    # Create the full file path
    file_path = os.path.join(CACHE_DIR, filename)
    
    # Write data to the file
    with open(file_path, 'w') as file:
        file.write(data)

def read_from_file(CACHE_DIR, filename):
    """Read the content of a text file and return it as a string."""
    # Create the full file path
    file_path = os.path.join(CACHE_DIR, filename)
    
    with open(file_path, 'r') as file:
        data = file.read()
    
    return data

# Example usage
text_data = "This is some text data to hash"
hash_value = create_hash(text_data)
print(f"Hash value: {hash_value}")