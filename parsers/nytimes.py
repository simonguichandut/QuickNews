"""
In the NYT, the tree is url->title->abstract. We can just store the title right after a url appears. However sometimes
the url appears again to link to another image. So we skip a url if it's already saved. There's some additional problems
like the "LIVE" tag appearing first and stuff which is hard to explain, but it works currently.
"""

contains_letters = lambda s: s.upper().isupper() or s.lower().islower()
# ban titles/urls if they contain certain strings
allowed = lambda url: not any(x in url for x in ("LIVE","commentsContainer","/interactive/","{","==="))

def parse(tree,titles,urls,save_next=False,verbose=False):

    for subtree in tree.iterchildren():
        
        # interactive content on nytimes messes everything up. this might work to avoid it 
        if 'class' in subtree.keys():
            if "interactive-content" in subtree.get('class'):
                return titles,urls

        t = subtree.text
        if t!=None:
            if verbose: print(t)
            if save_next and len(titles)==len(urls)-1:
                if verbose: print('TITLE:',t,'\n')
                titles.append(t)
                save_next=False
            else:
                if verbose:
                    print('wont save this title')
                    print(len(titles),len(urls))

            
        if 'href' in subtree.keys():
            url = subtree.get('href')
            if verbose: print(url)

            if url not in urls and len(url)>10 and allowed(url):

                if len(url)==len(titles)+1: # if we get here it means we couldn't find a title for previous url, so just remove
                    del url[-1]
                    if verbose: print('deleting past url')

                if verbose: print('URL:',url)
                urls.append(url)
                save_next=True
            
        parse(subtree,titles,urls,save_next=save_next,verbose=verbose)

    return titles,urls


def get(tree,verbose=False):
    subtree = tree.xpath("//*[@id='site-content']/div/div[1]/div[2]/section/div/div/div[1]")[0] # path to headlines specific to nytimes
    return parse(subtree,[],[],verbose=verbose)


## Test
# import requests
# from lxml import html
# url = "https://www.nytimes.com"
# page = requests.get(url)
# tree = html.fromstring(page.content)
# titles,urls=get(tree,verbose=True)
# for t,u in zip(titles,urls):
#    print('TITLE :',t)
#    print('LINK :',u)
#    print('FULL URL :',url+u)
#    print('\n')
