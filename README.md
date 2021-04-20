# Audiobook Tagger from Calibre Metadata

This is very much a proof of concept script for updating the metadata for audiobook files (currently MP3 and M4B) managed within a Calibre library, for optimal use with the [Audiobook metadata agent for Plex](https://github.com/seanap/Audiobooks.bundle). I would **strongly** recommend not running the script without modifying it to ensure it works with how your library is set up, and of course ensuring that you have all files backed up beforehand. I'll probably make this into a Calibre plugin at some point. Maybe.

## Limitations
* Doesn't handle books with multiple files
* Doesn't handle anything unexpected. At all. Basically it's written to handle the specifics of my library.