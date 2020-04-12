"""
In the NYT, the tree is url->title->abstract. We can just store the title right after a url appears. However sometimes
the url appears again to link to another image. So we skip a url if it's already saved. There's some additional problems
like the "LIVE" tag appearing first and stuff which is hard to explain, but it works currently.
"""

contains_letters = lambda s: s.upper().isupper() or s.lower().islower()

def parse(tree,titles,urls,save_next=False):

    for subtree in tree.iterchildren():
        
        t = subtree.text

        if t!=None:
            # print(t)
            if save_next and len(titles)==len(urls)-1 and t!='LIVE':
                # print('\nTITLE:',t)
                titles.append(t)
                save_next=False
            
        if 'href' in subtree.keys():
            url = subtree.get('href')
            # print(url)
            if url not in urls and len(urls)<=len(titles)+2 and "commentsContainer" not in url:
                # print('\nURL:',url)
                urls.append(url)
                save_next=True
            
        parse(subtree,titles,urls,save_next=save_next)

    return titles,urls


def get(tree):
    subtree = tree.xpath("//*[@id='site-content']/div/div[1]/div[2]/section")[0] # path to headlines specific to nytimes
    return parse(subtree,[],[])


## Test
# import requests
# from lxml import html
# url = "https://www.nytimes.com/"
# page = requests.get(url)
# tree = html.fromstring(page.content)
# titles,urls=get(tree)
# for t,u in zip(titles,urls):
#     print(t)
#     print(url+u)
#     print('\n')