from django.shortcuts import render

from . import util

from markdown2 import Markdown
markdowner = Markdown()

from django import forms    #for new and edit

import random


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title:  ")
    descr = forms.CharField(widget=forms.Textarea, label="Description, below:  ") 


class EditForm(forms.Form):
    title = forms.CharField(label="Title:  ")
    descr = forms.CharField(widget=forms.Textarea, label="Description, below:  ")


def index(request): # includes search / partial match
    entries=util.list_entries() # get list of entries
    if request.method=="GET":
        search_text = request.GET.get("q", None) # retrieves value, if any from search box
        if search_text:
            results=[]
            for entry in entries: # retrieves every entry that contains the search text (case insensitive)
                if search_text.lower() in entry.lower():
                    results.append(entry)
            if len(results)>0:
                return render(request, "encyclopedia/search.html", {'results': results})
            else:
                return render(request, "encyclopedia/error.html") # page not found
        else:
            return render(request, "encyclopedia/index.html", {"entries": entries})
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": entries})


def entry(request, title): # displays a single entry
    entries=util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        converted_page = markdowner.convert(page) # converts MD file to HTML
        return render(request, "encyclopedia/entry.html", {'converted_page': converted_page, 'title': title})
    else:
        return render(request, "encyclopedia/error.html") # page not found


def add(request): # adds a new entry
    entries=util.list_entries()
    if request.method == "GET":
        addform = NewEntryForm()
        return render(request, "encyclopedia/add.html", {'addform': addform})
    else:
        addform = NewEntryForm(request.POST)
        if addform.is_valid():
            title = addform.cleaned_data["title"]
            #print(title)
            descr = addform.cleaned_data["descr"]
            print(descr)
            dup = 0 # checking for duplicates, that is, existing enttry with the same name
            for entry in entries:
                if title.lower() == entry.lower():
                    dup = dup + 1
                #print(dup)
            if dup > 0:
                return render(request, "encyclopedia/error2.html") # title already exists
            else:
                util.save_entry(title, descr) # saves the entry and displays it
                page = util.get_entry(title)
                converted_page = markdowner.convert(page)
                return render(request, "encyclopedia/entry.html", {'converted_page': converted_page, 'title': title})
        else:
            return render(request, "encylcopedia/add.html", {'addform': addform})

def edit(request, title): # edits an existing entry
    page = util.get_entry(title)
    editform = EditForm(initial={'title': title, 'descr': page}) # opens existing form to allow editing
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {'editform': editform})
    else:
        editform = EditForm(request.POST) # saves and displays the edited entry
        if editform.is_valid():
            descr = editform.cleaned_data["descr"]
            util.save_entry(title, descr)
            page = util.get_entry(title)
            converted_page = markdowner.convert(page)
            return render(request, "encyclopedia/entry.html", {'converted_page': converted_page, 'title': title})
        else:
            return render(request, "encyclopedia/edit.html", {'editform': editform})


def randomp(request): # displays a random page
    entries = util.list_entries()
    x = random.randrange(0, len(entries)-1) # random number
    title = entries[x] # to select a random entry
    page = util.get_entry(title)
    converted_page = markdowner.convert(page)
    return render(request, "encyclopedia/entry.html", {'converted_page': converted_page, 'title': title})


    