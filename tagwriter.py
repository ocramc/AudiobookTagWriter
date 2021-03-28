import os, eyed3, pathlib, logging, untangle, mutagen, argparse, sys
logging.getLogger().setLevel("ERROR")
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="set working directory",
                    dest="suppliedPath")

args = parser.parse_args()

if args.suppliedPath != None:
    logging.debug("Setting path to " + args.suppliedPath)
    rootDir = args.suppliedPath
else:
    logging.debug("Setting path to " + os.getcwd())
    rootDir = os.getcwd()

if not os.path.exists(rootDir):
    logging.error("Path " + rootDir + " not found")
    sys.exit("Path doesn't exist")

if not os.path.isdir(rootDir):
    logging.error("The specified path is not a directory")
    sys.exit("Directory not specified")

if not os.path.exists(os.path.join(rootDir , "metadata.db")):
    logging.error("The specified directory is not a Calibre library")
    sys.exit("Directory not Calibre library")

reply = ""
while reply != "y":
    reply = str(input("Do you wish to update the metadata in " + rootDir + " (y/n): ")).lower().strip()
    if reply == "y":
        logging.debug("User confirmed metadata update")
    elif reply == "n":
        logging.debug("User cancelled metadata update")
        sys.exit("Metadata update cancelled")
    else:
        print("Please specify either (y)es or (n)o to proceed")

totalCount = 0
fileCount = 0

fileTypes = [".mp3", ".m4b"]

for dirName, subdirList, fileList in os.walk(rootDir):
     for fileName in fileList:
        filePath = os.path.join(dirName , fileName)
        fileExtension = pathlib.Path(filePath).suffix
        if fileExtension in fileTypes:
            totalCount += 1

logging.debug(totalCount + "files to be updated")

for dirName, subdirList, fileList in os.walk(rootDir):
    for fileName in fileList:
        filePath = os.path.join(dirName , fileName)
        fileExtension = pathlib.Path(filePath).suffix
        if fileExtension in fileTypes:
            fileCount += 1
            print("Updating file " + str(fileCount) + " of " + str(totalCount) + " - " + fileName, end="\r")
            metadataFile = os.path.join(dirName, "metadata.opf")
            with open(metadataFile, "r", encoding="utf-8") as fd:
                metadata = untangle.parse(fd.read())

                try:
                    bookTitle = metadata.package.metadata.dc_title.cdata
                    bookAuthor = metadata.package.metadata.dc_creator.cdata

                except:
                    logging.error("Unable to grab metadata for " + fileName)
                    pass
                else:
                    if fileExtension == ".mp3":
                        try:
                            audioFile = eyed3.core.load(filePath)
                            audioFile.initTag()
                            audioFile.tag.artist = bookAuthor
                            audioFile.tag.album = bookTitle
                            audioFile.tag.save()
                            logging.info("Updated metadata for " + fileName)
                            pass

                        except:
                            logging.error("Unable to update metadata for " + fileName)

                    elif fileExtension == ".m4b":
                        try:
                            audioFile = mutagen.File(filePath, easy=True)
                            audioFile['artist'] = bookAuthor
                            audioFile['album'] = bookTitle
                            audioFile.save(filePath)
                            logging.info("Updated metadata for " + fileName)
                            pass

                        except:
                            logging.error("Unable to update metadata for " + fileName)
