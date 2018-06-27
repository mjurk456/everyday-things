"""MP3 ORGANIZER
adds tags to MP3 files basing on filenames
"""


import sys
import os
import glob
from mp3_tagger import MP3File, VERSION_2
from unidecode import unidecode



def main():
    
    # getting folder given in arguments
    if len(sys.argv) > 1:
        mp3FolderPath = sys.argv[1]
    else:
        mp3FolderPath = input("Input a path to a folder with MP3 files: ? ")

    # checking if the folder exists
    while not(os.path.exists(mp3FolderPath)):
        mp3FolderPath = input("The folder does not exist, choose another folder or END to quit: ? ")
        if mp3FolderPath.upper() == "END":
            return None

    #looping through all mp3 files
    os.chdir(mp3FolderPath)
    logFile = open("log.txt", "w")
    for file in glob.glob("*.mp3"):
        print("Processing file {0}".format(file))
        try:
            mp3Author, mp3Name = file[:-4].split("-")
        except ValueError:
            logFile.write(file + "\n")
            continue

        currentMP3 = MP3File(file)
        currentMP3.set_version(VERSION_2)
        try:
            currentMP3.artist = mp3Author.strip()
            currentMP3.song = mp3Name.strip()
        except UnicodeEncodeError:
            currentMP3.artist = unidecode(mp3Author.strip())
            currentMP3.song = unidecode(mp3Name.strip())
            logFile.write(file + "\n")
            print("Unicode symbols error, continued without diacritics")
        finally:
            currentMP3.save()
    logFile.close()
    print("Tags have been changed. Names of unprocessed files have been added to log.txt")

if __name__ == "__main__":
    main()
