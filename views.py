from django.shortcuts import render, redirect
from markdown2 import markdown
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# display requested page
def entry(request, page):

    #gets user entry from URL
    userentry = util.get_entry(page)

    #checks for valid request
    if userentry is None: #need to resolve this
        return render(request, "encyclopedia/noentry.html")
    else:
        #converts MD to HTML
        MD = markdown(userentry) 
        return render(request, "encyclopedia/entry.html", {
            "title": userentry, 
            "MD": MD
        })


#implementing the search function
def search(request):
    #gets input string from search bar
    search_request = request.POST.get('q')
    result = util.get_entry(search_request)

    #returns a match or gives alternative options
    if result:
        MD = markdown(result)
        return render(request, "encyclopedia/entry.html", {
            "title": result, 
            "MD": MD
        })

    else:
        entries = util.list_entries()
        result = []

        for results in entries:
            if search_request.lower() in results.lower():
                result.append(results)
        return render (request, "encyclopedia/search.html",{
            'result':result
            })

def create(request):
    # variable will act as a control for blank or duplicate fields
    control = "control"

    if request.method == "POST":
        #gets user inputs and cleans it
        title = request.POST.get('title').strip().capitalize()
        content = request.POST.get('content').strip().capitalize()


        #checks for input validity
        if not content or not title:
            control='blank'
        elif title in util.list_entries():
            control='duplicate'
        else:
                util.save_entry(title, content)
                MD = markdown(content)
                return render(request, "encyclopedia/entry.html", {
                "title": title, 
                "MD": MD
                })
        #return to the HTML the control value
        return render(request,'encyclopedia/create.html',{
            'control':control
        })

    else:
        #sends user to page
        return render(request,'encyclopedia/create.html',{
            'control':control
        })

def edit (request, title):

    if request.method == 'POST':
        new = util.get_entry(title)
        edited = util.save_entry(title, new)
        MD = markdown(edited)
        return render(request, "encyclopedia/entry.html", {
        "title": title, 
        "MD": MD
        })
    else:
        return render(request, 'encyclopedia/edit.html')
    
    

def random_selection (request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    choice = util.get_entry(random_entry)
    MD = markdown(choice) 
    return render(request, "encyclopedia/entry.html", {
    "title": random_entry, 
    "MD": MD})