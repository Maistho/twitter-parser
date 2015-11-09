import re
import json
import sys
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Nope')
        sys.exit()

    filename = 'tags/' + sys.argv[1] + '.json'

    with open(filename, 'r') as f:
        with open(filename + '_new.json', 'w') as w:
            text = f.readline()
            while text != '':
                tweet = json.loads(text)
                tags = set()
                for i in tweet['tags']:
                    if i == 2:
                        tags.add(1)
                    elif i == 4:
                        tags.add(0)
                    else:
                        tags.add(i)

                tweet['tags'] = list(tags)

                w.write(json.dumps(tweet) + "\n")
                text = f.readline()

