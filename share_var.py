'''import multiprocessing
  
def func(mydict,mylist):  
    mydict["index1"]="aaaaaa"   #子进程改变dict,主进程跟着改变  
    mydict["index2"]="bbbbbb"  
    mylist.append(11)        #子进程改变List,主进程跟着改变  
    mylist.append(22)  
    mylist.append(33)  
  
if __name__=="__main__":  
    with multiprocessing.Manager() as MG:   #重命名  
        mydict=multiprocessing.Manager().dict()   #主进程与子进程共享这个字典  
        mylist=multiprocessing.Manager().list()   #主进程与子进程共享这个List
  
        p=multiprocessing.Process(target=func,args=(mydict,mylist))  
        p.start()  
        p.join()  
  
        print(mylist)  
        print(mydict)'''


def binary_search(lis, key):
    low = 0
    high = len(lis) - 1
    time = 0

    if key == lis[len(lis)-1]:
        return len(lis)-1

    while low < high:
        time += 1
        mid = int((low + high) / 2)
        if key < lis[mid]:
            high = mid - 1
        elif key > lis[mid]:
            low = mid + 1
        else:
            # 打印折半的次数
            # print("times: %s" % time)
            return mid
    # print("times: %s" % time)
    return False


if __name__ == '__main__':
    LIST = [1, 5, 7, 8, 22, 54, 99, 123, 200, 222, 444]
    result = binary_search(LIST, 222)
    print(result)