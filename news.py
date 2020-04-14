import requests
from lxml import html
import webbrowser

from parsers import bbcnews,nytimes,lapresse,ledevoir

broken_msg = "I think this website has changed and I can no longer read it."

Names = ["BBC News","The New York Times","La Presse","Le Devoir"]
URLs = ["https://www.bbc.com/news","https://www.nytimes.com","https://www.lapresse.ca","https://www.ledevoir.com"]
Parsers = [bbcnews,nytimes,lapresse,ledevoir]

def clean(s): # replace some html ugliness
    s=s.replace("\n","") # line breaks
    s=s.replace("  ","") # excessive whitespace
    s=s.replace("\xa0"," ") # space after number
    return s

Links = []
i = 1
max_per_journal = 3

for name,url,parser in zip(Names,URLs,Parsers):

    print('\n'+name)

    try:
        page = requests.get(url,timeout=0.5)

    except:
        print('Request timed out')
        
    else:
        # print('connection succesful')

        tree = html.fromstring(page.content)
        try:
            titles,links = parser.get(tree)
        except:
            print('Parser broken')

        else:
            for k in range(min(max_per_journal,len(titles))):
                print('[%d] \t '%i, clean(titles[k]))

                if url in links[k]: # this happens sometimes for nytimes
                    Links.append(links[k])
                else:
                    Links.append(url+links[k])
                    
                i+=1



### Command-line interface
print("\nEnter [id] of article(s) to open web pages, or nothing to exit.")
# print("Please disable your adblocker :)")
x=input()
if x==None or x=="":
    print('\n')
else:
    for id in (eval(i) for i in x.split(" ")):
        if id<0 or id>len(Links):
            print('Give valid id')
        else:
            webbrowser.open(Links[id-1])
