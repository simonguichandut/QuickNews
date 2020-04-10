import requests
from lxml import html
import webbrowser

def fix(s): # replace some html ugliness
    s=s.replace("\n","") # line breaks
    s=s.replace("  ","") # excessive whitespace
    s=s.replace("\xa0"," ") # space after number
    return s

broken_msg = "I think this website has changed and I can no longer read it :("

links = []
count = 1

### La Presse
print('\nLa Presse')
url = "https://www.lapresse.ca"

try: 
    page = requests.get(url)
    tree = html.fromstring(page.content)
    man = tree.xpath("/html/body/div[4]/div[3]/div[1]/section")[0] # path to manchettes

    # Une
    print('[%d] \t '%count, fix(man[1][0][0].get('alt')))
    links.append(url+man[1][0].get('href'))
    # Trio
    for i in range(3):
        print(('[%d] \t '%(i+1+count)), fix(man[3][i][2][0][1].text))
        links.append(url+man[3][i][0].get('href'))

    count+=4
except:
    print(broken_msg)
    exit


### Le Devoir
print('\nLe Devoir')
url = "https://www.ledevoir.com"

try: 
    page = requests.get(url)
    tree = html.fromstring(page.content)
    man = tree.xpath("//*[@id='articles']/div[1]/div[1]/div/div[1]")[0] # path to manchettes

    for i in range(2):
        print(('[%d] \t '%(i+count)), fix(man[i][0][0][0][1].text))
        links.append(url+man[i][0][0][0].get('href'))

    print(('[%d] \t '%(count+2)), fix(man[2][0][0][0][0].text))
    links.append(url+man[2][0][0][0].get('href'))

    count+=3
except:
    print(broken_msg)
    exit







### Command-line interface

print("\nEnter [id] of article(s) to open web pages, or nothing to exit.")
# print("Please disable your adblocker :)")
x=input()
if x=="0" or x==None or x=="":
    print('\n')
else:
    for id in (eval(i) for i in x.split(" ")):
        if id<0 or id>len(links):
            print('Give valid id')
        else:
            webbrowser.open(links[id-1])
