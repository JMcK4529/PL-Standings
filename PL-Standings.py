print("                   Copyright (C) 2022 Joseph McKeown               ")
print("")
print("This program is free software: you can redistribute it and/or modify")
print("it under the terms of the GNU General Public License as published by")
print("the Free Software Foundation, either version 3 of the License, or")
print("(at your option) any later version.")
print("")
print("This program is distributed in the hope that it will be useful,")
print("but WITHOUT ANY WARRANTY; without even the implied warranty of")
print("MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the")
print("GNU General Public License for more details.")
print("")
print("You should have received a copy of the GNU General Public License")
print("along with this program.  If not, see <http://www.gnu.org/licenses/>.")
print("")
print("---------------------------------------------------------------------")
print("")
###############################################################################

#SerpAPI is designed for web scraping!
from serpapi import GoogleSearch

#append_to_output will collate data into a list of dictionaries (in Pre_Output)
#also keeps track of what data has been gathered so far (in Check_Set)
def append_to_output(some_results_dict):
    global Pre_Output, position, Check_Set    
    for result in some_results_dict["sports_results"]["league"]["standings"]:
        if result['team']['name'] not in Check_Set:
            Pre_Output.append({"Pos" : position, "Name" : result['team']['name'], "Played" : result['mp'],
                               "W" : result['w'], "D" : result['d'], "L" : result['l'],
                               "GF" : result['gf'], "GA" : result['ga'], "GD" : result['gd'], "Points" : result['pts']})
            Check_Set.add(result['team']['name'])
        position = len(Check_Set)+1

#perform_next_search goes looking for bits of the Premier League table that are hidden below "See More"
#achieved by altering the query (and therefore which section of the table appears)
def perform_next_search():
    global Pre_Output, Check_Set, position
    params = {
        "api_key": my_api_key,
        "engine": "google",              
        "q": first_query + Pre_Output[-1]['Name'],
        "gl": "uk",
        }
    search = GoogleSearch(params)
    results = search.get_dict()
    append_to_output(results)

#An API key generated by signing up for an account with SerpAPI
my_api_key = "810d4ad27dd194bfabfd0bf820da8bddac181c094586c4a4c6c9fcd5d84c1957"

#The initial search term for getting the PL table (returns a page with the top 5 teams)
first_query = "premier league standings"

#Parameters to pass to the first instance of the GoogleSearch class (below)
params = {
    "api_key": my_api_key,
    "engine": "google",              # serpapi parsing engine
    "q": first_query,                      # search query
    "gl": "uk",                      # country from which search comes
}

#Initialising global variables
Pre_Output = []
Check_Set = set()
position = len(Check_Set)+1

#Keeping the user updated, as the script is quite slow...
print("Getting data...\n")

#Initial web scrape for the top 5 PL teams!
top_5_search = GoogleSearch(params)
top_5_results = top_5_search.get_dict()
append_to_output(top_5_results)

#...and now for all the other PL teams.
while position < 21:
    perform_next_search()

#Making the data easier to print nicely.
list_of_headers = []
for key in Pre_Output[0]:
    list_of_headers.append(key)
data_array = []
for dictionary in Pre_Output:
    row = []
    for key in dictionary:
        row.append(dictionary[key])
    data_array.append(row)

#Printing data nicely.
print("{:<8} {:<15} {:<8} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format("Pos", "Name", "Played", "W", "D", "L", "GF", "GA", "GD", "Points"))
for row in data_array:
    pos, name, played, w, d, l, gf, ga, gd, points = row
    print("{:<8} {:<15} {:<8} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(pos, name, played, w, d, l, gf, ga, gd, points))
