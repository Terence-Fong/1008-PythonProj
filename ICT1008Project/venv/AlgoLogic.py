import json
import heapq
import Dataset

def get_jsonRoutes():
    results = json.loads(open("Bus_Route.json").read())
    return results

def get_jsonStops():
    results = json.loads(open("BusStop.json").read())
    return results

routes = get_jsonRoutes()
stops = get_jsonStops()

#print(stops)

code_map = {}
for key, value in stops.items():
    code_map[value['BusStopCode']] = value

route_map = {}
busRoute = []

def calculate_route(start, end): #1

    if start and end:
            #create dictionary to store routes node
            routes_map = {}

            for route in routes:
                #start to create each node in the route and put in dictionary
                key = (route["ServiceNo"], route["Direction"])
                if key not in routes_map:
                    routes_map[key] = []
                routes_map[key] += [route]

            # call the djikstra algorithm and get back the total distance and the shortest route
            distance, path = find_shortest_route(stops[start]["BusStopCode"], stops[end]["BusStopCode"], routes_map)

            #print out the route
            for code, service in path:
                street_name = str(code_map[code]["Description"])

                # print(street_name)

            #store all the data into the strings
            no_of_stops = "The bus trip took " + str(len(path)) + " stops"
            print(no_of_stops)
            return path, len(path)

    else:
        print("Error", "Please enter something")

def find_shortest_route(start,end,routes_map):


    """
    CREATING MAP OF NODES FOR ALL BUS STATIONS IN SINGAPORE
    """
    graph = {}
    for service, path in routes_map.items(): #for each bus service
        for route_index in range(len(path) - 1): #for each route
            key = path[route_index]["BusStopCode"]
            if key not in graph:
                graph[key] = {}
            curr_route_stop = path[route_index] #get current node
            next_route_stop = path[route_index + 1] #get adjacent node
            curr_distance = curr_route_stop["Distance"] or 0
            next_distance = next_route_stop["Distance"] or curr_distance
            distance = next_distance - curr_distance    #calculate the distance from the next node to current
            assert distance >= 0, (curr_route_stop, next_route_stop) #error checking (distance cant be less than 0)
            curr_code = curr_route_stop["BusStopCode"]
            next_code = next_route_stop["BusStopCode"]
            graph[curr_code][(next_code, service)] = distance #store current node and adjacent node


    """
    START OF DIJKSTRA ALGORITHM
    """
    seen = set()
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    heapq.heappush(queue, (0, 0, 0, [(start, None)]))
    while queue:
        # get the first path from the queue
        (curr_cost, curr_distance, curr_transfers, path) = heapq.heappop(queue)

        # get the last node from the path
        (node, curr_service) = path[-1]

        # path found
        if node == end:
            return (curr_distance, path)

        if (node, curr_service) in seen:
            continue

        seen.add((node, curr_service))
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for (adjacent, service), distance in graph.get(node, {}).items():
            new_path = list(path)
            new_path.append((adjacent, service))
            new_distance = curr_distance + distance
            new_cost = distance + curr_cost
            new_transfers = curr_transfers
            if curr_service != service:
                new_cost += 10
                new_transfers += 1
            new_cost += 0.5

            heapq.heappush(queue, (new_cost, new_distance, new_transfers, new_path))


