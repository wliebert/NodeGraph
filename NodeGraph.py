attrs=["parents","children"]
def linkNodes(parent,child,span):
    parent.children.append((child,span))
    child.parents.append((parent,span))
def unlinkNodes(parent,child,span=None):
    parent.children.remove((child,span))
    child.parents.remove((parent,span))
def mergeLists(lists):
    nodes,spans=zip(*sorted(lists))
    return [(x,spans[nodes.index(x)]) for x in set(nodes)]

class node:
    def __init__(self,children,parents):
        self.parents=[(self,0)]
        self.children=[(self,0)]
        self.outgoing=[]
        self.set(children,0)
        self.set(parents,1)
        self.updateParents()
    def get(self,attr):
        list1=getattr(self,attrs[1-attr])
        for x in list1:
            list2=getattr(x[0],attrs[1-attr])
            for y in list2:
                lists=[self,y[0]]
                if y[0] not in [z[0] for z in list1]:
                    span=x[1]+list2[[a[0] for a in list2].index(y[0])][1]
                    linkNodes(lists[attr],lists[1-attr],span)
                else:
                    span=list1[[z[0] for z in list1].index(y[0])][1]
                    newspan=x[1]+y[1]
                    if newspan < span:
                        unlinkNodes(lists[attr],lists[1-attr],span)
                        linkNodes(lists[attr],lists[1-attr],newspan)
    def set(self,list,attr):
        for x in list:
            node=nodes[x[0]]
            lists=[self,node]
            if node in [y[0] for y in attrs[1-attr]]:
                if x[1] < y[1]:
                    unlinkNodes(lists[attr],lists[1-attr],y[1])
                    linkNodes(lists[attr],lists[1-attr],x[1])
            else:
                linkNodes(lists[attr],lists[1-attr],x[1])
            lists[attr].outgoing.append((lists[1-attr],x[1]))
        self.get(attr)
    def updateNode(self,children,parents):
        self.set(children,0)
        self.set(parents,1)
        self.updateParents()
    def updateParents(self):    
        for x in self.parents:
            for y in self.children:
                if x[0] is not y[0]:
                    if y[0] not in [z[0] for z in x[0].children]:
                        linkNodes(x[0],y[0],y[1]+self.parents[[a[0] for a in self.parents].index(x[0])][1])
                    else:
                        span=x[0].children[[a[0] for a in x[0].children].index(y[0])][1]
                        newspan=y[1]+x[0].children[[a[0] for a in x[0].children].index(self)][1]
                        if newspan < span:
                            unlinkNodes(x[0],y[0],span)
                            linkNodes(x[0],y[0],newspan)

            
if __name__=="__main__":
    nodes=[]
    nodes.append(node([],[]))
    nodes.append(node([(0,6)],[(0,10)]))
    nodes.append(node([(0,4)],[(0,20)]))
    nodes.append(node([(1,1),(2,2)],[(1,2),(2,40)]))
    nodes.append(node([(0,1)],[]))
    nodes.append(node([(4,1)],[(3,1)]))


    for node in nodes:
        print("Node[{}]: {}\n\tChildren (Node,Span):".format(nodes.index(node), node))
        for x in nodes[nodes.index(node)].children:
            print("\t\t({},{})".format(nodes.index(x[0]), x[1]))
        print("\tOutgoing Connections (Node,Span):")
        for x in nodes[nodes.index(node)].outgoing:
            print("\t\t({},{})".format(nodes.index(x[0]), x[1]))