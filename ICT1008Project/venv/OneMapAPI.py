from onemapsg import OneMapClient
import json

Client = OneMapClient("ibudinsa@gmail.com", "markred29125") # for authentication

print('Enter your Location to search:')
inputLocation = input() # search for address

storeDicOfSearch = Client.search(inputLocation) #inserting the dictionary into store

totalpage = storeDicOfSearch["totalNumPages"] # extracting value of key "totalNumPages" from dic
searchResult = storeDicOfSearch['results'] # store list of dictionary search values

counter =0
for i in range(totalpage): # Extracting individual list data from each location
    storeDicOfSearch2 = Client.search(inputLocation,True,True,i+1)
    searchResult2 = storeDicOfSearch2['results']
    for x in range(len(searchResult)): # printing each building address individually
        counter +=1
        print("Search Result No", counter ," : ",searchResult[x])

print ("Total number of Results: ", counter)
x = OneMapClient.get_public_transport_route([1.378509975,103.84980279999999],[1.3694385619999998,103.8493344],20200430,152030,"BUS")
print (x)