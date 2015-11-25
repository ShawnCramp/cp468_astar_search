""" ---------------------------------------------------------
Author: Shawn Cramp
ID: 111007290
Author: Edward Huang
ID: 100949380
Author: Bruno Salapic
ID: 100574460
Author: Konrad Bania
ID: 110447960

Description: CP468 Final Assignment
Date: November, 13th, 2015
-------------------------------------------------------------
Assignment Task:

The purpose of this CP468 term project is to design and implement an 
A*-based algorithm to solve a path planning problem. You can use
 the programming language of your choice
 
Consider a Museum room that is patrolled by N robots at night.
At a pre-determined time, the robots are supposed to rendezvous
at a given point R in the room. The robots move inside the room,
and the room contains obstacles, such as chairs and benches for
the visitors, paintings, sculptures etc. The robots are supposed
to know the locations of the obstacles in the room. Implement an
A*-based algorithm to compute the path of each robot, from its
initial position to the given rendezvous point R.
-------------------------------------------------------------
Import Declarations ------------------------------------- """
import heapq
import math
import copy


""" ---------------------------------------------------------
Class Declarations -------------------------------------- """


class PriorityQueue:
    def __init__(self):
        self._values = []
        
    def empty(self):
        return len(self._values) == 0
    
    def length(self):
        return len(self._values)
    
    def put(self, item, priority):
        heapq.heappush(self._values, (priority, item))
        
    def get(self):
        return heapq.heappop(self._values)[1]


class Map:
    """
    Map object for holding all nodes in the map, as well as
    children to each node
    """
    def __init__(self, width, height, rendezvous, robots, layout, node_dict):
        self.width = width
        self.height = height
        self.rendezvous = rendezvous
        self.robots = robots
        self.layout = layout
        self.nodes = node_dict

    def children(self, node):
        return self.nodes[node]
    

class Robot:
    """
    Robot object for holding robot paths and locations
    """
    def __init__(self, start, finish, came_from, cost_so_far, path_cost):
        self.start = start
        self.finish = finish
        self.path_cost = path_cost
        self.came_from = came_from
        self.cost_so_far = cost_so_far
        
    def path(self, node_map):
        distance = copy.deepcopy(self.path_cost)
        node = copy.deepcopy(self.finish)
        pathing = [node]
        while distance != -1:
            node = pathing[-1]
            # print('Checking Children of Node: {}'.format(node))
            # print('Distance: {}'.format(distance))
            children = node_map.children(node)
            # print('Node Children: {}'.format(children))
            for child in children:
                if child in self.cost_so_far.keys():
                    # print('Child Cost: {}: {}'.format(child, self.cost_so_far[child]))
                    if self.cost_so_far[child] == distance:
                        # print('If Check: Passed')
                        pathing.append(child)
                        break
                    else:
                        pass
                        # print('If Check: Failed')
            distance -= 1
            # print('-'*18)
        
        return list(reversed(pathing))
        
    def pprint(self, layout):
        print('Node Costs')
        for key, val in self.cost_so_far.iteritems():
            print('{}: {}'.format(key, val))
            layout[key] = val
        
        array = []
        for i in range(0, 20):
            temp = []
            for j in range(0, 30):
                temp.append(9)
            array.append(temp)
            
        for i in array:
            print(i)
        
        for key, val in layout.iteritems():
            print('{}: {}'.format(key, val))
            array[key[0]][key[1]] = val
        
        print('Layout Map by Cost')
        print('#: Wall     . : UnExplored Floor Space\n')
        for i in array:
            print('{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}{:>3}'.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],i[10], i[11], i[12], i[13], i[14], i[15], i[16], i[17], i[18], i[19],i[20], i[21], i[22], i[23], i[24], i[25], i[26], i[27], i[28], i[29]))


""" ---------------------------------------------------------
Function Declarations ----------------------------------- """


def valid_coordinate(node_set, x, y, shift):
    """
    Check if node at node_set[x][y] is a valid node for robots
    to travel.

    :param node_set:
    :param x:
    :param y:
    :return:
    """
    valid = False
    new_x = x + shift[0]
    new_y = y + shift[1]

    if (new_x >= 0 and new_x < len(node_set)) and (new_y >= 0 and new_y < len(node_set[0])):
        if node_set[new_x][new_y] == 0:
            valid = True
        else:
            pass
    else:
        pass

    return valid


def get_children(node_set, x, y):
    """
    Using 2D list of all nodes in the map and an x and y coordinate
    in the map.  Get the child nodes attached to the x and y
    coordinate parameter.

    :param node_set:
        2D array of all nodes in the map
    :param x:
        x coordinate of current node
    :param y:
        y coordinate of current node
    :return children:
        dictionary of key node and children
    """
    temp = []
    neighbours = ((1, 0), (0, 1), (-1, 0), (0, -1))

    for shift in neighbours:
        #  check = node_set[x + value[0]][y + value[1]]
        if valid_coordinate(node_set, x, y, shift):
            temp.append((x + shift[0], y + shift[1]))
            #  print(temp)

    children = {(x, y): temp}
    return children


def build_dictionary(node_set):
    """
    Build the dictionary of valid nodes and their explorable children.

    :param node_set:
    :return:
    """
    nodes = {}
    layout = {}

    for x, x_line in enumerate(node_set):
        for y, y_line in enumerate(x_line):      
            if node_set[x][y] == 0:
                layout[(x, y)] = '.'  # for drawing
                children = get_children(node_set, x, y)
                nodes.update(children)
            elif node_set[x][y] == 1:
                layout[(x, y)] = '#'  # for drawing

    return nodes, layout


def map_coordinates(map_handle):
    """
    Create Map object with all coordinates and neighbours

    :param map_handle:
        File handle for Map
    :return:
        Coordinates List
    """

    ''' List of Robots '''
    robots = []
    
    ''' Initial Declarations.  These will be overwritten '''
    node_dict = {}
    width = 0
    height = 0
    rendezvous = (0, 0)

    ''' 2D Array to initialize nodes '''
    temp = []
    
    ''' Build Map Object '''
    for i, line in enumerate(open(map_handle)):
        
        if i == 0:  # when i is 0
            line = line.strip().split(" ")
            width = line[0]
            height = line[1]
            
        elif i == 1:  # when i is 1
            line = line.strip().split(" ")
            robot_count = int(line[0])
            
        elif i - 2 < robot_count:
            robots.append(tuple(map(int, line.strip().split(" "))))
            
        elif i == 2 + robot_count:
            rendezvous = tuple(map(int, line.strip().split(" ")))
            
        else:
            temp.append(map(int, line.strip()))

    node_dict, layout = build_dictionary(temp)

    return Map(width, height, rendezvous, robots, layout, node_dict)


def heuristic(g, h, distance):
    """
    A* Heuristic
    f(n) = g(n) + h(n)

    :param g:
        Cost to reach node from start
        Eg. (2, 1)
    :param h:
        Estimated cost to get from n to goal
        Eg. (4, 7)
    :return f(n):
        Estimated total cost of cheapest
        solution through n
    """
    return math.sqrt((abs(h[0] - g[0]) ** 2) + (abs(h[1] - g[1]) ** 2)) + distance


def a_star(coordinates, robot, rendezvous):
    """
    Complete A* Search Algorithm.

    :param coordinates:
        Map Coordinates Object
    :param rendezvous:
        Where the Robots meet.  (Ending Node Node)
        Eg. (5, 7)
    :param robot:
        Location of Robot.
        Eg. (2, 1)
    :return found:
        True if Robot is found, else False.
    :return cost:
        Cost of Path to Robot
    """

    ''' Cost of Initial Node '''
    priority = 0

    ''' Priority Queue for evaluating locations '''
    frontier = PriorityQueue()

    ''' Put Root node into Queue '''
    frontier.put(robot, priority)

    ''' Initialize '''
    came_from = {}
    cost_so_far = {}
    came_from[robot] = None
    cost_so_far[robot] = 0

    ''' Loop through Queue '''
    while not frontier.empty():
        current_node = frontier.get()

        ''' If current node is robot node,
        break and return true -------- '''
        if current_node == rendezvous:
            break

        ''' Evaluate neighbouring nodes to current node '''
        for node in coordinates.children(current_node):
            # print('Current: {}'.format(current_node))
            # print('Currently Evaling Child: {}'.format(node))
            new_cost = cost_so_far[current_node] + 1
            # print('New Cost for Node: {}'.format(new_cost))
            if node not in cost_so_far or new_cost < cost_so_far[node]:
                # print('If Check: Passed')

                cost_so_far[node] = new_cost
                priority = new_cost + heuristic(node, rendezvous, new_cost)

                frontier.put(node, priority)

                # print('Node Priority: {}'.format(priority))
                # print('Frontier Size: {}'.format(frontier.length()))

                came_from[node] = current_node
                # print('-'*9)
            else:
                pass
                # print('If Check: Failed')
                # print('Frontier Size: {}'.format(frontier.length()))
                # print('-'*9)

    return came_from, cost_so_far


def pretty(d, indent=0):
    """
    Print Dictionary to console in a readable fashion

    :param d:
        Dictionary to print
    :param indent:
    :return:
    """
    for key, value in d.iteritems():
        print '\t' * indent + str(key)
        if isinstance(value, dict):
            pretty(value, indent+1)
        else:
            print '\t' * (indent+1) + str(value)


def init_robots(node_map):
    robots = []
    for robot_start in node_map.robots:
        came_from, cost_so_far = a_star(node_map, robot_start, node_map.rendezvous)
        robots.append(Robot(robot_start, node_map.rendezvous, came_from, cost_so_far, cost_so_far[node_map.rendezvous]))

    return robots


def main():
    """
    Main Loop of Program

    :return:
    """
    
    ''' Create Map Object '''
    map_handle = 'layoutmap4.txt'
    
    ''' 2D Array of nodes in Map '''
    node_map = map_coordinates(map_handle)
    print('Mapping Data: \n')
    print('Width: {:>10}'.format(node_map.width))
    print('Height: {:>10}'.format(node_map.height))
    print('Rendezvous: {:>10}'.format(node_map.rendezvous))
    print('Robots: {:>10}'.format(node_map.robots))
    print('Dictionary:')
    pretty(node_map.nodes)
    print('-'*40 + '\n')
    print('Performing A* Search...')
    print('-'*40)
    robots = init_robots(node_map)
    print('...')
    print('-'*40)
    print('A* Complete...')
    print('Robot being Evaluated: {}'.format(node_map.robots[0]))
    print('Rendezvous Node: {}'.format(node_map.rendezvous))
    print('-'*40)

    for guy in robots:
        print('Evaluating Robot: {} -> {}'.format(guy.start, guy.finish))
        temp = copy.deepcopy(node_map.layout)
        # guy.pprint(temp)
        temp = copy.deepcopy(node_map)
        print('One Optimal Path:')
        print(guy.path(temp))
        # print(guy.cost_so_far.keys())
        print('-'*18)
    

""" Launch Main Program """
main()
