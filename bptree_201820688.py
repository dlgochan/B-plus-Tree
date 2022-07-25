import sys
# from typing import ParamSpec, Pattern


class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []
        
        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees = []
        
        self.parent = None
        self.isLeaf = False
        
        # leaf node has next node pointer
        self.next = None
        self.prev = None
        self.values = []

    def location(self, node, key):####### my function
        if(len(node.keys) == 0):
            return 0
        for i in range(0, len(node.keys)):
            if(key >= node.keys[i]):
                continue
            else:
                return i
        return i+1

    def indexing(self, root):
        q = []
        q.append(root)
        while(len(q) != 0):
            tmp = q.pop(0)
            if(tmp.isLeaf == False):
                for i in range(0, len(tmp.keys)):
                    sub = tmp.subTrees[i+1]
                    while(sub.isLeaf == False):
                        sub = sub.subTrees[0]
                    tmp.keys[i] = sub.keys[0]
                    
            for node in tmp.subTrees:
                if(node == tmp.subTrees[-1]):
                    q.append(node)
                    continue
                q.append(node)
        return

    def indexMerge(self, order, root):
        if(self == root):
            if(len(self.keys) == 0):
                return self.subTrees[0]
            else:
                return root

        # root 가 아니므로 무조건 parent가 존재
        else:
            idx = self.location(self.parent, self.subTrees[0].keys[0])
            if(idx > 0): #left merge
                # print("@@@@@@@@@@@@@ index merge left")
                # merge
                prev = self.parent.subTrees[idx-1]
                prev.keys = prev.keys + self.parent.keys[idx-1:idx] + self.keys
                prev.subTrees = prev.subTrees + self.subTrees
                for sub in self.subTrees:
                    sub.parent = prev

                # del parent key
                self.parent.keys.pop(idx-1)
                self.parent.subTrees.pop(idx)

                if(len(prev.keys) >= order):
                    root = prev.split(order, root)
            else: #right merge
                # print("@@@@@@@@@@@@@ index merge right")
                # merge
                next = self.parent.subTrees[idx+1]
                next.keys = self.keys + self.parent.keys[idx:idx+1] + next.keys
                next.subTrees = self.subTrees + next.subTrees
                for sub in self.subTrees:
                    sub.parent = next

                # del parent key
                self.parent.keys.pop(idx)
                self.parent.subTrees.pop(idx)

                if(len(next.keys) >= order):
                    root = next.split(order, root)
            ###########################################################################
            if(self.parent != None and len(self.parent.keys) < order/2 - 1):
                root = self.parent.indexMerge(order, root)
            


        return root
    def delete(self, k, order, root):
        if(self.isLeaf == False):
            # print("delete error : it is not leaf node")
            return root

        self.keys.remove(k)
        if(self == root):
            return root
        #merge 필요한 경우
        if(len(self.keys) < order/2 - 1):
            #borrow left
            if(self.prev != None and self.prev.parent == self.parent and len(self.prev.keys)-1 >= order/2 - 1):
                # print("@@@@@@@@@@@@@ borrow left")
                k = self.prev.keys[-1]
                self.prev.keys = self.prev.keys[0:-1]
                self.parent.keys[self.location(self.parent, k)] = k
                self.insert(0, k)

            #borrow right
            elif(self.next != None and self.next.parent == self.parent and len(self.next.keys)-1 >= order/2 - 1):
                # print("@@@@@@@@@@@@@ borrow right")
                k = self.next.keys[0]
                self.next.keys = self.next.keys[1:]
                self.parent.keys[self.location(self.parent, k)-1] = self.next.keys[0]
                self.keys.append(k)
            #############################        완료         #############################
            else: # merge
                if(self.prev != None and self.prev.parent == self.parent): #left merge
                    # print("@@@@@@@@@@@@@ merge left")
                    # link leaf
                    self.prev.keys = self.prev.keys + self.keys
                    self.prev.next = self.next
                    if(self.next != None):
                        self.next.prev = self.prev

                    # del parent key
                    i = self.location(self.parent, self.prev.keys[0])
                    self.parent.keys.pop(i)
                    self.parent.subTrees.pop(i+1)

                elif(self.next != None and self.next.parent == self.parent): #right merge
                    # print("@@@@@@@@@@@@@ merge right")
                    # link leaf
                    self.next.keys = self.keys + self.next.keys
                    self.next.prev = self.prev
                    if(self.prev != None):
                        self.prev.next = self.next

                    # del parent key
                    i = self.location(self.parent, self.next.keys[-1])
                    self.parent.keys.pop(i-1)
                    self.parent.subTrees.pop(i-1)

                else:
                    # print("@@@@@ merege error : there is no prev no next ")
                    return root
                ###########################################################################

            # delete 과정 끝났으면 인덱싱
            self.indexing(root)

            ## 머지하니까 부모노드도 머지 필요한 경우 (얘는 인덱싱 필요 없음)
            if(self.parent != None and len(self.parent.keys) < order/2 - 1):
                root = self.parent.indexMerge(order, root)
            
            
        # borrow, merge 필요 없는 경우
        else:
            #indexing 만 하고 끝
            self.indexing(root)

        return root

    
    def insert(self, loc, k):
        if(self.isLeaf == False):
            # print("insert error : it is not leaf node")
            return

        self.keys.insert(loc, k)
        return


    def split(self, order, root):
        i = int(order/2)
        pk = self.keys[i]
        new = Node()
        
        if(self.isLeaf):
            # 다른 node 생성
            new.keys = self.keys[i:]
            self.keys = self.keys[0:i]
            #leaf link
            new.isLeaf = True
            new.next = self.next
            if(self.next != None):
                self.next.prev = new
            self.next = new
            new.prev = self
            
        else:
            new.keys = self.keys[i+1:]
            new.subTrees = self.subTrees[i+1:]
            for sub in self.subTrees[i+1:]:
                sub.parent = new
            self.keys = self.keys[0:i]
            self.subTrees = self.subTrees[0:i+1]

        # 부모 node에 추가
        if(self.parent != None): #부모가 있을 때
            parent = self.parent
            new.parent = parent
            parent.keys.insert(self.location(parent, pk), pk)
            parent.subTrees.insert(self.location(parent, pk), new)
            
            # (leaf 아닌 곳에서 스플릿 일어나는거) 재귀
            if(len(parent.keys) >= order):
                root = parent.split(order, root)

        else: #부모가 없을 때
            parent = Node()
            self.parent = parent
            new.parent = parent
            parent.keys.insert(0, pk)
            parent.subTrees.append(self)
            parent.subTrees.append(new)
            root = parent

        return root
    
    

##################################################################################################

class B_PLUS_TREE:

    def __init__(self, order): #### 약간 수정함
        self.order = order
        n = Node()
        n.isLeaf = True
        self.root  = n
        
        pass      


    def location(self, node, key):####### my function
        if(len(node.keys) == 0):
            return 0
        for i in range(0, len(node.keys)):
            if(key >= node.keys[i]):
                continue
            else:
                return i
        return i+1
        

    def insert(self, k):
        pos = self.root
        
        #알맞은 leaf node 찾기
        while(pos.isLeaf == False):
            pos = pos.subTrees[self.location(pos, k)]

        #알맞은 leaf로 왔음 삽입 시작
        pos.insert(self.location(pos, k), k)
        
        #잘 삽입했는데 order 이상인 경우 : split해줘야함
        if(len(pos.keys) >= self.order):
            self.root = pos.split(self.order, self.root)            



    def delete(self, k):
        pos = self.root
        
        #알맞은 leaf node 찾기
        while(pos.isLeaf == False):
            pos = pos.subTrees[self.location(pos, k)]

        #알맞은 leaf로 왔음 삭제 시작
        self.root = pos.delete(k, self.order, self.root)

        



    
    def print_root(self):
        if(len(self.root.keys)==0):
            print("[]")
            return
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass
    
    def print_tree(self):
        if(self.root.isLeaf):
            self.print_root()
            return
        q = []
        q.append(self.root)
        while(len(q) != 0):
            tmp = q.pop(0)
            if(tmp.isLeaf == False):
                print(str(tmp.keys).replace(" ",""), end='-')
            for node in tmp.subTrees:
                if(node == tmp.subTrees[-1]):
                    print(str(node.keys).replace(" ",""))
                    q.append(node)
                    continue
                print(str(node.keys).replace(" ",""), end=',')
                q.append(node)

        
    def find_range(self, k_from, k_to):
        pos = self.root
        while(pos.isLeaf == False):
            pos = pos.subTrees[self.location(pos, k_from)]
        #알맞은 leaf로 옴

        tmp = []
        if k_from in pos.keys:
            i = pos.keys.index(k_from)
        else:
            i = self.location(pos, k_from)
        while(1):
            if(i < len(pos.keys)):
                if(pos.keys[i] <= k_to):
                    tmp.append(pos.keys[i])
                    i += 1
                else:
                    break
            else:
                if(pos.next == None):
                    break
                else:
                    pos = pos.next
                    i = 0
        
        # range내의 key들 출력
        for key in tmp:
            if(key == tmp[-1]):
                print(key)
                continue
            print(key, end=',')


    def find(self, k):
        result = ""
        pos = self.root
        while(pos.isLeaf == False):
            result += str(pos.keys).replace(" ","") + '-'
            pos = pos.subTrees[self.location(pos, k)]
        
        if k in pos.keys:
            result += str(pos.keys).replace(" ","")
        else :
            print("NONE")
            return

        print(result)


def main():
    myTree = None
    
    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue
        
        print(comm)
        
        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)
            
        elif params[0] == "EXIT":
            return
            
        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)
            
        elif params[0] == "DELETE":
            k = int(params[1])
            myTree.delete(k)            
            
        elif params[0] == "ROOT":            
            myTree.print_root()            
            
        elif params[0] == "PRINT":            
            myTree.print_tree()            
                  
        elif params[0] == "FIND":            
            k = int(params[1])
            myTree.find(k)
            
        elif params[0] == "RANGE":            
            k_from = int(params[1])
            k_to = int(params[2])
            myTree.find_range(k_from, k_to)
        
        elif params[0] == "SEP":
            print("-------------------------")
    
if __name__ == "__main__":
    main()