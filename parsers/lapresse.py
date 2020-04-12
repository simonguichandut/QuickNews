"""
In La Presse, there is a url->string beginning with "Source ID"->Article title structure.
To get the title we can simply get the text exactly one depth after "Source ID".
There are duplicates or urls, we can just remove them. We also get urls of sections like
sports, and not full articles.  We can just make sure there is at least say 5 digits in the url
"""

num_digits = lambda s: sum(i.isdigit() for i in s)

def parse(tree,titles,urls,save_next=0):

    for subtree in tree.iterchildren():
        
        t = subtree.text
        if t!=None:
            # print(t)

            if save_next: # found Source ID last time which means this time is the article title
                titles.append(t)
                save_next=False

            if "Source ID" in t:
                save_next = True
            
        if 'href' in subtree.keys():
            url = subtree.get('href')
            # print('URL HERE:',subtree.get('href'))
            if num_digits(url)>=5:
                urls.append(url)
            
        parse(subtree,titles,urls,save_next=save_next)

    return titles,urls


def get(tree):

    subtree = tree.xpath("/html/body/div[4]/div[3]/div[1]/section")[0]  # path to headlines specific to lapresse
    titles,urls = parse(subtree,[],[])

    # Remove duplicate urls but preserve order
    seen = set()
    urls_final = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            urls_final.append(url)

    return titles,urls_final


## Test
# import requests
# from lxml import html
# url = "https://www.lapresse.ca"
# page = requests.get(url)
# tree = html.fromstring(page.content)
# titles,urls=get(tree)
# for t,u in zip(titles,urls):
#     print(t)
#     print(url+u)
#     print('\n')