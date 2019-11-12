import wolframalpha
from tokens import WOLFRAM_API_TOKEN

client = wolframalpha.Client(WOLFRAM_API_TOKEN)


class WolfQueryException(Exception):
    pass

def query(quary_string):
    res = client.query(quary_string)
    if res['@success'] == 'false':
        raise WolfQueryException
    text = '\n'.join(['%s:: %s' % (key, value) for (key, value) in res.details.items()])
    img_urls = [item['img']['@src'] for item in res['pod'][1]['subpod']]
    return text, img_urls
