# Rehydrating tweets

Tweets in The Danish Gigaword (DAGW) are stored only using their IDs. DAGW does not distribute the text content of tweets. Therefore, to use the text of tweets, you must retrieve their contents from Twitter using tweet IDs. This process is called *rehydration*.

We recommend the open-source tool [twarc](https://github.com/DocNow/twarc) to rehydrate tweets in DAGW. Once you install and set up `twarc`, rehydration is as simple as calling `twarc` on the raw tweet ID file. For example, for the `datwitter` section:

```bash
twarc hydrate \
    datwitter/raw_data/da_all_150420-260520.txt > datwitter/raw_data/hydrated_tweets.txt
```


## Converting hydrated tweets to the DAGW format
To convert the rehydrated tweets to the DAGW format, run the script included in `scripts/twitter_expander` on the JSONL file you created during rehydration. Following with the example for `datwitter`:

```bash
python scripts/twitter_expander.py \
    --input datwitter/raw_data/hydrated_tweets.txt \
    --section_name datwitter \
    --output sektioner/datwitter
```

