import json
import os
import stat
import platform

# Define the cache file name - hidden on Windows with dot prefix
CACHE_FILE = ".cache.json"

def get_cache_path(folder_path):
    """
    Get the full path to the cache file in the specified folder
    """
    return os.path.join(folder_path, CACHE_FILE)

def make_file_hidden(file_path):
    """
    Make the file hidden based on the platform
    """
    if platform.system() == "Windows":
        try:
            import ctypes
            # Set file as hidden on Windows
            ctypes.windll.kernel32.SetFileAttributesW(file_path, 2)  # 2 = FILE_ATTRIBUTE_HIDDEN
            print(f"Successfully made file hidden: {file_path}")
        except Exception as e:
            print(f"Warning: Failed to make file hidden: {e}")
    # On Unix/Linux/Mac, files starting with '.' are already hidden by convention

def load_cache(folder_path):
    """
    Load cached data from the cache file in the specified folder
    Returns an empty dict if the file doesn't exist or can't be read
    """
    cache_path = get_cache_path(folder_path)
    print(f"Loading cache from: {cache_path}")
    
    # Check for the main cache file
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                data = json.load(f)
                print(f"Successfully loaded cache data: {data}")
                return data
        except Exception as e:
            print(f"Error loading main cache file: {e}")
            # Continue to check for temp file
    
    # If main file doesn't exist or couldn't be read, try the temp file
    temp_cache_path = cache_path + ".tmp"
    if os.path.exists(temp_cache_path):
        print(f"Main cache file not found, trying temp file: {temp_cache_path}")
        try:
            with open(temp_cache_path, 'r') as f:
                data = json.load(f)
                print(f"Successfully loaded cache data from temp file: {data}")
                
                # Try to recover by saving this data to the main cache file
                try:
                    with open(cache_path, 'w') as main_f:
                        json.dump(data, main_f, indent=2)
                    print("Recovered cache data by copying from temp file to main file")
                except Exception as e:
                    print(f"Could not recover cache file: {e}")
                
                return data
        except Exception as e:
            print(f"Error loading temp cache file: {e}")
    
    # If we get here, neither file could be read successfully
    print("No valid cache file found, returning empty dict")
    return {}

def save_cache(folder_path, data):
    """
    Save data to the cache file in the specified folder
    Makes the file hidden if it's newly created
    """
    try:
        os.makedirs(folder_path, exist_ok=True)  # Ensure folder exists
        cache_path = get_cache_path(folder_path)
        is_new_file = not os.path.exists(cache_path)
        print(f"Saving cache to: {cache_path}")
        print(f"Cache data: {data}")
        
        # First try to write to a temporary file, then rename it
        # This is more atomic and can prevent corruption
        temp_path = cache_path + ".tmp"
        with open(temp_path, 'w') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())  # Ensure data is written to disk
        
        # Replace the old file with the new one
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
            except (IOError, PermissionError) as e:
                print(f"Warning: Could not remove old cache file: {e}")
        
        # Rename the temporary file to the actual cache file
        try:
            os.rename(temp_path, cache_path)
            print(f"Successfully renamed temp file to {cache_path}")
        except (IOError, PermissionError) as e:
            print(f"Error renaming temp file: {e}")
            # Try copying content instead if rename fails
            try:
                with open(temp_path, 'r') as src, open(cache_path, 'w') as dst:
                    dst.write(src.read())
                os.remove(temp_path)  # Remove temp file after copying
                print(f"Successfully copied content to {cache_path}")
            except Exception as e2:
                print(f"Error copying content to final file: {e2}")
                return False
        
        # Make the file hidden if it's newly created
        if is_new_file:
            make_file_hidden(cache_path)
        
        print(f"Successfully saved cache to {cache_path}")
        return True
    except Exception as e:
        print(f"Error saving cache: {e}")
        # Try an alternative approach - write directly to the file
        try:
            if not os.path.exists(folder_path):
                print(f"Creating directory: {folder_path}")
                os.makedirs(folder_path, exist_ok=True)
                
            cache_path = get_cache_path(folder_path)
            print(f"Trying direct write to: {cache_path}")
            with open(cache_path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Alternative save method succeeded for {cache_path}")
            
            # Also try to remove any lingering temp file
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
                
            return True
        except Exception as e2:
            print(f"Alternative save method also failed: {e2}")
            return False

def get_component_cache(folder_path, component_name, default_values=None):
    """
    Get cached data for a specific component
    Returns default_values if the component data doesn't exist
    """
    cache = load_cache(folder_path)
    
    # Verify we have data for this component
    if component_name not in cache:
        print(f"No cache data found for component {component_name}")
        return default_values or {}
    
    result = cache.get(component_name, default_values or {})
    
    # Verify data structure
    if not isinstance(result, dict):
        print(f"Warning: Cache for {component_name} is not a dictionary. Got {type(result)}")
        return default_values or {}
    
    print(f"Got component cache for {component_name}: {result}")
    
    # Special validation for ImageTitleFormatter to ensure font_size is properly handled
    if component_name == "ImageTitleFormatter" and "font_size" in result:
        try:
            # Ensure font_size is a number and convert if needed
            if isinstance(result["font_size"], str):
                result["font_size"] = int(float(result["font_size"]))
            else:
                result["font_size"] = int(result["font_size"])
            print(f"Validated font_size for {component_name}: {result['font_size']}")
        except (ValueError, TypeError) as e:
            print(f"Error validating font_size: {e}")
            
    return result

def update_component_cache(folder_path, component_name, component_data):
    """
    Update the cache with new component data
    """
    cache = load_cache(folder_path)
    cache[component_name] = component_data
    print(f"Updating cache for {component_name} with: {component_data}")
    return save_cache(folder_path, cache)

