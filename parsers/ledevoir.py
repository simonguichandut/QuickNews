"""
In Le Devoir, the tree is url->title->abstract. We can just store the title right after a url appears. We just 
have to skip empty strings, just make sure there are letters.
"""

contains_letters = lambda s: s.upper().isupper() or s.lower().islower()

def parse(tree,titles,urls,save_next=0):

    for subtree in tree.iterchildren():
        
        t = subtree.text

        if t!=None and contains_letters(t) and save_next:
            # print(t)
            titles.append(t)
            save_next=False
            
        if 'href' in subtree.keys():
            url = subtree.get('href')
            # print('URL HERE:',url)
            urls.append(url)
            save_next=True
            
        parse(subtree,titles,urls,save_next=save_next)

    return titles,urls


def get(tree):
    subtree = tree.xpath("//*[@id='articles']/div[1]/div[1]/div/div[1]")[0]  # path to headlines specific to ledevoir
    return parse(subtree,[],[])


## Test
# import requests
# from lxml import html
# url = "https://www.ledevoir.com"
# page = requests.get(url)
# tree = html.fromstring(page.content)
# titles,urls=get(tree)
# for t,u in zip(titles,urls):
#     print(t.split())
#     print(url+u)
#     print('\n')