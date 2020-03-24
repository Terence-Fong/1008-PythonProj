from onemapsg import OneMapClient
# for authentication
Client = OneMapClient("ibudinsa@gmail.com", "markred29125")

# search for address
print('Enter your starting location to search:')
inputLocation = input()

#inserting the dictionary into store
storeDicOfSearchStart = (Client.search(inputLocation)['results'][0])
startLocation = Client.search(inputLocation)['results'][0]['SEARCHVAL']

# search for destination
print("Enter your location for destination: ")
inputDestination = input()

#inserting the dictionary into store
storeDicOfSearchDestination = (Client.search(inputDestination)['results'][0])
endlocation = Client.search(inputDestination)['results'][0]['SEARCHVAL']
coordinatesOfStart = [storeDicOfSearchStart['LATITUDE'],storeDicOfSearchStart['LONGITUDE']]
coordinatesOfDestination = [storeDicOfSearchDestination['LATITUDE'],storeDicOfSearchDestination['LONGITUDE']]
x = Client.get_public_transport_route(coordinatesOfStart,coordinatesOfDestination,20200430,152030,"BUS")

routesStore = (((((x['plan'])['itineraries'])[0])['legs'])) # this enters the legs list, the 0 means option 1

print("Start location: ",startLocation,"End location: ",endlocation)
print (routesStore)
for i in range(len(routesStore)-1):
    if routesStore[i]['mode'] == 'WALK':
        distanceOf1 = int(routesStore[i]['distance']) # 1st tab of the search
        nameOfLocation1 = routesStore[i]['to']['name']
        timeTaken1 = float((routesStore[i]['duration']) / 60)
        print("Walk for ", distanceOf1, "meters to ", nameOfLocation1, " this will take: ", timeTaken1, " Mins")
    elif routesStore[i]['mode'] == "BUS":
        distanceOf1 = int(routesStore[i]['distance']) # 1st tab of the search
        nameOfLocation1 = routesStore[i]['to']['name']
        timeTaken1 = float((routesStore[i]['duration']) / 60)
        startBusStopNo = routesStore[i]['from']['stopCode']
        endBusStopNo = routesStore[i]['to']['stopCode']
        bustakenNo = routesStore[i]['route']
        busstopName = routesStore[i]['from']['name']
        # print("Take the Bus for", distanceOf1, "meters to ", nameOfLocation1, "(Bus Stop Number):", originBusStopNo,"take bus number:",bustakenNo,
        #       " this will take a total time of:", timeTaken1, " Mins")
        print("Take bus:",bustakenNo,"from bus stop :",busstopName,", Bus Stop number",startBusStopNo,"to",nameOfLocation1,", Bus stop number",endBusStopNo,".","This will take a total of:",timeTaken1,"mins.")
    else:
        print ("error")

# for i in range(len(routesStore)-1):
#     distanceOf1 = int(routesStore[i]['distance']) # 1st tab of the search
#     nameOfLocation1 = routesStore[i]['to']['name']
#     timeTaken1 = float((routesStore[i]['duration']) / 60)
#     try:
#         originBusStopNo = routesStore[i]['to']['stopCode']
#     except:
#         print("Walk for ", distanceOf1, "meters to ", nameOfLocation1," this will take: ", timeTaken1, " Mins")
#         continue
#     print("Walk for ", distanceOf1,"meters to ",nameOfLocation1," Bus Stop Number: ",originBusStopNo," this will take: ",timeTaken1," Mins")



# storeDicOfSearch = Client.search(inputLocation) #inserting the dictionary into store
# totalpage = storeDicOfSearch["totalNumPages"] # extracting value of key "totalNumPages" from dic
# searchResult = storeDicOfSearch['results'] # store list of dictionary search values

# counter =0
# for i in range(totalpage): # Extracting individual list data from each location
#    storeDicOfSearch2 = Client.search(inputLocation,True,True,i+1)
#    searchResult2 = storeDicOfSearch2['results']
#    for x in range(len(searchResult)): # printing each building address individually
#        counter +=1
#        print("Search Result No", counter ," : ",searchResult[x])

# print ("Total number of Results: ", counter)