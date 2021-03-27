import os, eyed3, pathlib, logging, untangle, mutagen
logging.getLogger().setLevel("ERROR")
rootDir = os.getcwd()
totalCount = 0
fileCount = 0

fileTypes = ['.mp3', '.m4b']

for dirName, subdirList, fileList in os.walk(rootDir):
    for fileName in fileList:
        filePath = dirName + "\\" + fileName
        fileExtension = pathlib.Path(filePath).suffix
        if fileExtension in fileTypes:
            totalCount += 1

for dirName, subdirList, fileList in os.walk(rootDir):
    for fileName in fileList:
        filePath = dirName + "\\" + fileName
        fileExtension = pathlib.Path(filePath).suffix
        if fileExtension in fileTypes:
            fileCount += 1
            print("Updating file " + str(fileCount) + " of " + str(totalCount) + " - " + fileName, end="\r")
            metadataFile = dirName + "\\metadata.opf"
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
