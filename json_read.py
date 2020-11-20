# approach #2
# scrape non-JSON out of the file and then import it as valid JSON.
# Hope, this approach will allow us to apply a JSON schema to simplify the checks I want to employ

import json
from egs_read import ALine

sources = "TESTDATA\\Config_Example.ecf",


with open(sources[0]) as f:
    raw = f.read()
    raw_lines = raw.split('\n')

    clean_lines = ["   "]
    for line in raw_lines:
        clean_lines.append ( str(ALine(line)))
    for i in range(20):
        print(f"{i+1} {clean_lines[i]}")
    data = json.loads("\n".join(clean_lines))

    print(data)