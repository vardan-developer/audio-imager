import os
import sys
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, APIC, error

def embed_artwork(path):
    for filename in os.listdir(path):
        if filename.lower().endswith('.m4a'):
            file_path = os.path.join(path, filename)
            artwork_filename = f"{os.path.splitext(filename)[0]}.png"
            artwork_file_path = os.path.join(path, artwork_filename)
            
            if os.path.exists(artwork_file_path):
                try:
                    # Open the audio file
                    audio = MP4(file_path)
                    
                    # Read the artwork file
                    with open(artwork_file_path, 'rb') as f:
                        artwork_data = f.read()
                    
                    # Embed the artwork
                    audio['covr'] = [MP4Cover(artwork_data, imageformat=MP4Cover.FORMAT_PNG)]
                    
                    # Save the file
                    audio.save()
                    print(f"Successfully embedded artwork into {filename} using mutagen")
                    
                    # Verify if the artwork is embedded
                    audio_check = MP4(file_path)
                    if 'covr' in audio_check:
                        print(f"Verified: Artwork size {len(audio_check['covr'][0])} bytes")
                    else:
                        print(f"Warning: Artwork not detected after embedding in {filename}")
                        
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            else:
                print(f"No artwork found for {filename}")
        
        elif filename.lower().endswith('.mp3'):
            file_path = os.path.join(path, filename)
            artwork_filename = f"{os.path.splitext(filename)[0]}.png"
            artwork_file_path = os.path.join(path, artwork_filename)
            
            if os.path.exists(artwork_file_path):
                try:
                    # Try to open ID3 tag or create if doesn't exist
                    try:
                        audio = ID3(file_path)
                    except error:
                        print(f"Creating new ID3 tag for {filename}")
                        audio = ID3()
                    
                    # Read the artwork file
                    with open(artwork_file_path, 'rb') as f:
                        artwork_data = f.read()
                    
                    # Add the artwork to the ID3 tag
                    audio['APIC'] = APIC(
                        encoding=3,  # UTF-8
                        mime='image/png',
                        type=3,      # Cover (front)
                        desc='Cover',
                        data=artwork_data
                    )
                    
                    # Save the file
                    audio.save(file_path)
                    print(f"Successfully embedded artwork into {filename} using mutagen ID3")
                    
                    # Verify if the artwork is embedded
                    audio_check = ID3(file_path)
                    if 'APIC:Cover' in audio_check or 'APIC:' in audio_check:
                        print(f"Verified: MP3 artwork embedded successfully")
                    else:
                        print(f"Warning: Artwork not detected after embedding in {filename}")
                        
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
            else:
                print(f"No artwork found for {filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python embed_artwork.py <path_to_audio_files>")
        sys.exit(1)
    
    path = sys.argv[1]
    embed_artwork(path) 