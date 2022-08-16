
#import ijson
import ijson.backends.yajl2 as ijson
import json
import wikipedia
import time
wikipedia.set_lang("da")



with open("wikidata-20220307-all.json", "rb") as file:
    danishTitles = ijson.items(file, "item.sitelinks.dawiki.title")
    count = 0
    with open("DanishWikiData.ndjson", "a", encoding="utf-8") as outputfile:
        for idx, title in enumerate(danishTitles):
            if idx < 76032:
                count +=1
                print(count, end="\r")
                continue
            while True:
                try:
                    wikiDataDict = {
                        "title":title,
                        "pagecontent":wikipedia.page(title=title).content
                    }
                except (wikipedia.DisambiguationError, wikipedia.PageError, json.JSONDecodeError) as e:
                    # Since we are parsing the entirety of wikipedia, we know we are going to reach all of the suggested pages at some point so we just skip if the title is ambiguas 
                    break
                except (wikipedia.WikipediaException, TimeoutError, ConnectionError):
                    # This is the exception thrown if the call engine is currently busy
                    print("Too busy right now, retrying in 5 seconds")
                    time.sleep(5)
                    continue


                outputfile.write(json.dumps(wikiDataDict)+"\n")
                count +=1
                print(count, end="\r")
                break

