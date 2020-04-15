This is a simple python script that gets the main headlines from a short list of online newspapers: [BBC News](https://www.bbc.com/news), [The New York Times](https://www.nytimes.com/), [La Presse](https://www.lapresse.ca), [Le Devoir](https://www.ledevoir.com). It should be simple enough to add others by inspecting the html contents of their homepage.

Simply run:
> python news.py

Or add `alias news="python [path-to-QuickNews]/news.py"` to `.bash_profile` !
 
Requirements:
Python 3.0+
Modules : requests,lxml,webbrowser
 
The code will stop working if/when the websites significantly change their layout.
