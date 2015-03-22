import re
import json
import sys
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('Nope')
        sys.exit()

    filename = 'tweets/' + sys.argv[1] + '.json'

    with open(filename, 'r') as f:
        with open(filename + '.text', 'w') as w:
            text = f.readline()
            while text != '':
                tweet = json.loads(text)
                if tweet['text'][0:2] != 'RT' and len(tweet['text']) != 0:
                   ctext = re.sub(r"[\r\n]", " ", tweet['text'])
                   w.write(ctext+ "\n")
                text = f.readline()



