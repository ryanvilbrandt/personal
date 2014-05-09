agents = [None,
          [1,1,1,1,1,1,1,1],    # 1
          [2,2,2,2,1,1,1,1],    # 2
          [3,3,3,3,2,2,2,2],    # 3
          [4,4,4,4,3,3,3,3],    # 4
          [5,5,4,4,4,4,3,3],    # 5
          [6,6,5,5,4,4,4,4],    # 6
          [7,6,6,5,5,4,4,4],    # 7
          [8,7,6,6,5,5,4,4]     # 8
          ]

levels = {}

NUM_RESONATORS = 8
MIN_AGENT_LEVEL = 6
MAX_AGENT_LEVEL = 8
MIN_PORTAL_LEVEL = 7

def AddSetToListOfSets(new_item, item_list):
    """
    @param new_item - set(), the item to be checked if it exists in list
    @param item_list - list, list of sets
    If there is a set in item_list that is the subset of new_item
    do not add new_item to item_list.
    If new_item is a subset of a set in item_list, remove that set
    from item_list and add new_item
    @return list, Updated list of sets
    """

    for s in item_list:
        if s.issubset(new_item):
            return item_list
        elif new_item.issubset(s):
            item_list.remove(s)
            item_list.append(new_item)
            return item_list

    return item_list
        
            

def ResosRecurse(agent_tracker=[], resos=[]):
    global agents
    global levels
    for i in xrange(MIN_AGENT_LEVEL,MAX_AGENT_LEVEL+1):
        a = agents[i]
        for j in xrange(8,0,-1):
            temp = resos+a[:j]
            if len(temp) < NUM_RESONATORS:
                ResosRecurse(agent_tracker+[i], temp)
            elif len(temp) == NUM_RESONATORS:
                avg = int(sum(temp)/float(len(temp)))
                if avg >= MIN_PORTAL_LEVEL:
                    new_agents = set(agent_tracker+[i])
                    r = levels.get(avg,set())
                    levels[avg] = AddSetToListOfSets(new_agents, r)
            else:
                pass

ResosRecurse()
sorted_keys = sorted(levels.keys())
for k in sorted_keys:
    print k
    for d in levels[k]:
        print "\t",d
            
            
