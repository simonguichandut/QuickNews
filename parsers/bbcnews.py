"""
On BBCnews, it goes url->article. There are extra urls with no numbers, just make sure there are numbers so it's an article
Also some links are just "Video", remove those.
"""

num_digits = lambda s: sum(i.isdigit() for i in s)

def parse(tree,titles,urls,save_next=False):

    for subtree in tree.iterchildren():
        
        t = subtree.text

        if t!=None:
            # print(t)
            if save_next and len(titles)==len(urls)-1 and t!="Video" and t!="Live":
                # print('TITLE:',t)
                titles.append(t)
                save_next=False
            
        if 'href' in subtree.keys():
            url = subtree.get('href')
            # print(url)
            if url[5:] not in urls and num_digits(url)>=5:
                # print('\nURL:',url)
                urls.append(url[5:])    # remove the initial '/news' because the website is already loaded as .com/news
                save_next=True
            
        parse(subtree,titles,urls,save_next=save_next)

    return titles,urls


def get(tree):
    subtree = tree.xpath("//*[@id='news-top-stories-container']")[0] # path to headlines specific to bbc
    return parse(subtree,[],[])


## Test
# import requests
# from lxml import html
# url = "https://www.bbc.com/news"
# page = requests.get(url)
# tree = html.fromstring(page.content)
# titles,urls=get(tree)
# for t,u in zip(titles,urls):
#     print(t)
#     print(url+u)
#     print('\n')