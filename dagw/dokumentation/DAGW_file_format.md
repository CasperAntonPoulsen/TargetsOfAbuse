# File Format

This document describes the file format for the Danish Gigaword Corpus.

The philosophy is to present data as plaintext, UTF8, one file per document. Accompanying metadata gives information about (for example) the author, the time or location of the document's creation, an API hook for re-retrieval of the document, among others.

# Corpus Sections

As the corpus many sections, per section, we do the following:

 * Give each corpus section a directory, with an agreed name.
 * Keep all plaintext as one file per document
 * Use a section prefix, underscore, and document identifier as the filename; e.g. "tv2r_01672"
 * Do not use file extensions for the text files
 * Maintain a one-record-per-line JSONL file in the directory, with the same name as the section, and with "jsonl" suffix, e.g., "tv2r.jsonl". The content of this file should follow the JSONL format, see http://jsonlines.org.
 * Each document's metadata is placed as a single JSON record in the JSONL metadata file, with a key "doc_id" matching the filename it describes. Separate entries by line breaks (i.e., one JSON object per line)
 * A `LICENSE` file should be included in each section, stating the license under which the section is distributed. CC and public domain only! Preferably CC0 or CC-BY; CC-NC if we have to. No copyleft licenses - they restrict the use of the data too much, which we are trying to avoid.

Here are the fields for the standoff JSONL metadata file entries:

 * `doc_id`: a string containing the document ID, which is also its filename. Begin with the section prefix, followed by an underscore. `String`. **Required**.
 * `date_published`: the publication date of the source document, including the timezone. If only the year is available, use `year_published` instead. In the Python `strftime()` format, use `"%c %z"`. `String`. *Preferred*.
 * `uri`: the URI from which the document originated; can be an API endpoint that links directly to the data. `String, URI`. *Preferred*.
 * `year_published`: the year CE that the source document was published. `Integer`. Use only as an alternative to `date_published`. *Optional*.
 * `date_collected`: the date at which the source document / API result collection, including the timezone. In the Python strftime() format, use `"%c %z"`. `String`. *Optional*.
 * `date_built`: the date this document was included in the current version of the dataset, including the timezone. In the Python strftime() format, use `"%c %z"`. `String`. *Optional*.
 * `location_name`: the name of the location of the document's origin. `String`. *Optional*.
 * `location_latlong`: latitude and longitude of the document's origin. `List of two floats`. *Optional*.

### Speech transcripts
To represent speakers in the text files, prefix each turn with "TALER 1: " (substituting whatever ID is appropriate). Note: there is no space before the colon; use one space after the colon. It is also OK to include the speaker's name directly if this is publicly known, e.g., "Thomas Helmig: ". 

For multi-speaker corpus sections, an optional `talere.jsonl` file can be included in the section, containing one JSON dictionary that is keyed by speaker ID. Speaker IDs should be consistent through all documents in a section. Speaker IDs need only be unique to speakers in a section, not universally.
