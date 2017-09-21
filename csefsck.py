from time import time
from sys import exit
BLOCK_SIZE=4096
DEVICE_ID=20
PTRS_PER_BLCK=400
FREE_START=1
FREE_END=25
ROOT=FREE_END+1
BLOCKS_IN_FREE=400
MAX_FILE_SIZE=1638400
MAX_NUM_BLOCKS=10000
FILES_DIR="/Users/preeti/Desktop/FS"



# 1 Check DeviceId id correct
def checkDeviceId():
 superPath=FILES_DIR+"/fusedata.0"
 superblock=open(superPath,'r+')
 contents=superblock.read()
 contents=contents.strip()
 fileList=contents.split(',')
 deviceIdList=fileList[2].split(':')
 deviceIdTest=deviceIdList[1]
 deviceIdStr=deviceIdTest.strip()
 deviceIdnumber=int(deviceIdStr)
    
 if(DEVICE_ID!=deviceIdnumber):
    print ("Device ID is incorrect.\n")
    exit(1)
    	
    superblock.seek(0)
    superblock.truncate()
    superblock.write(contents)
    superblock.close()
    
# 2. All times are in the past, nothing is in the future.
def checkTimes(t, type, num):
 superPath = FILES_DIR + "/fusedata.0"
 superblock = open(superPath, 'r+')
 contents = superblock.read()
 contents = contents.strip()
 fileList=contents.split(',')
    
 if(type=='f'):
  if(contents.count('{') != 1 and contents.count('}') !=1):
          print ("fusedata %d does not contain inode data.\n" %num)
          #return
  atime=4
  ctime=5
  mtime=6
 else:
     if(contents.count('{') != 2 and contents.count('}') !=2):
             print ("fusedata.%d does not contain directory data.\n" %num)
             #return
     atime=5
     ctime=6
     mtime=7
 atimeList=fileList[atime].split(':')
 ctimeList=fileList[ctime].split(':')
 mtimeList=fileList[mtime].split(':')
 atimeTest=atimeList[1]
 atimeStr=atimeTest.strip()
 atimenumber=int(atimeStr)
 ctimeTest=ctimeList[1]
 ctimeStr=ctimeTest.strip()
 ctimenumber=int(ctimeStr)
 mtimeTest=mtimeList[1]
 mtimeStr=mtimeTest.strip()
 mtimenum=int(mtimeStr)

 updated = False
 if(t<atimenumber):
         updated = True
         print ("atime in fusedata.%d was in future and is updated now to the current time\n" % num)
         fileList[atime] = fileList[atime].replace(atimeStr,str(t))
 if(t<ctimenumber):
         updated = True
         print ("ctime in fusedata.%d was in future and is updated now to the current time\n" % num)
         fileList[ctime] = fileList[ctime].replace(ctimeStr,str(t))
 if(t<mtimenumber):
         updated = True
         print ("mtime in fusedata.%d was a in future and is updated now to the current time\n" % num)
         fileList[mtime] = fileList[mtime].replace(mtimeStr,str(t))
 if(updated):
         contents = ','.join(fileList)
    
 block.seek(0)
 block.truncate()
 block.write(contents)
 block.close()
       
if(type == 'd'):
         fileList = contents.split('{')
         inodeList = fileList[2].split('}')
         inodeList = inodeList[0].split(',')
         for entry in inodeList:
                 entry = entry.strip()
                 inode = entry.split(':')
                 if(inode[1] != '.' and inode[1] != '..'):
                         checkTimes(t, inode[0], int(inode[2]))
        
        
def checkTimesCall():
    timeSinceEpoch=int(time())
    checkTimes(timeSinceEpoch, 'd', ROOT)

def checkInode(num,inUse):
    block1 = FILES_DIR + "/fusedata." + str(num)
    block = open(block1, 'r+')
    contents = block.read()
    if(contents.count('{') != 1 and contents.count('}') != 1):
        print ("Corrupted inode metadata in fusedata.%d and does match the format.")
        return -1
    contents = contents.strip()
    fileList = contents.split(',')
    
    sizeOfData=fileList[0]
    sizeOfList=sizeOfData.split(':')
    sizeStr=sizeOfList[1].strip()
    sizenumber=int(sizeStr)    

    linkData=fileList[4]
    linkList=linkData.split(':')
    linkStr=linkList[1].strip()
    linknumber=int(linkStr)
    if (linknumber < 1):
        fileList[4]=fileList[4].replace(linkStr, '1')
    indirectLocData=fileList[8]
    indirectLocList=indirectLocData.split(' ')
    indirectList=indirectLocList[1].split(':')
    indirectStr=indirectList[1].strip()
    locData=indirectLocList[2]
    locData=locData.rstrip('}')
    locList=locData.split(':')
    locStr=locList[1].strip()
    locnumber=int(locStr)

    inUse.append(locnumber)
    locPath=FILES_DIR + "/fusedata." + locStr
    locOfFile=open(locPath, 'r+')
    locContents = locOfFile.read()
    locOfFile.seek(0)
    testData=locContents.split(',')
    is_array=True
    test_array=[]
    for i in testData:
            i=i.strip()
            if (not i.isdigit()):
                    is_array = False
                    break
            test_array.append(int(i))
    if(not is_array):
            FileList[8]=fileList[8].replace(indirectStr, '0')
            locContents=locContents[0:(BLOCK_SIZE - 1)]
            fileList[0]=fileList[0].replace(sizeStr,str(len(locContents)))
            locOfFile.seek(0)
            locOfFile.truncate()
            locOfFile.write(locContents)
            print ("The size at fusedata.%d is %d bytes.\n" % (num,len(locContents)-1))
    else:
            fileList[8]=fileList[8].replace(indirectStr,'1')
            if(sizenumber>BLOCK_SIZE*len(test_array)):
                    print ("Size at the file inode located on fusedata.%d is too large.\n" % num)
            elif(sizenumber < BLOCK_SIZE * (len(test_array) - 1)):
                    print ("Size at the file inode located on fusedata.%d is too small.\n" % num)
            else:
                    print ("The size at fusedata.%d is %d bytes and therefore the inode points to %d data blocks.\n" % (num, sizenumber, len(test_array)))
            for i in test_array:
                    inUse.append(i)
    contents = ','.join(fileList)
    block.seek(0)
    block.truncate()
    block.write(contents)
    block.close()
def checkSuperTime(t,fileList):
        ctimeList=fileList[0].split(':')
        ctimeTest=ctimeList[1]
        ctimeStr =ctimeTest.strip()
        ctimeNumber = int(ctimeStr)
        if(t<ctimeNumber):
                print ("Time in the superblock was a future value and is now the current time\n")
                fileList[0] = fileList[0].replace(ctimeStr, str(t))
def checkSuperblockData(t,fileList):
        dataList=[]
        for i in range(3,7):
                dataList.append(fileList[i].split(':'))
        for j in range(0,4):
                testData=dataList[j][1]
                dataStr=testData.strip()
                if(j==3):
                        dataStr=dataStr.rstrip('}')
                dataNumber=int(dataStr)
                if (j==0):
                        if(dataNumber!=FREE_START):
                                print ("freeStart in the superblock was incorrect and has been corrected\n")
                                fileList[3]=fileList[3].replace(dataStr,str(FREE_START))
                elif (j==1):
                        if(dataNumber!=FREE_END):
                                print("freeEnd in the superblock was incorrect and has been corrected\n")
                                fileList[4]=fileList[4].replace(dataStr,str(FREE_END))
                elif (j==2):
                        if(dataNumber!=ROOT):
                                print ("root in the superblock was incorrect and has been corrected\n")
                                fileList[5] = fileList[5].replace(dataStr, str(ROOT))
                else:
                        if(dataNumber!=MAX_NUM_BLOCKS):
                                print ("maxBlocks in the superblock was incorrect and has been corrected\n")
                                fileList[6] = fileList[6].replace(dataStr,str(MAX_NUM_BLOCKS))
    

def checkSuper(t):
    superPath=FILES_DIR+"/fusedata.0"
    superblock=open(superPath, 'r+')
    contents=superblock.read()
    contents=contents.strip()
    fileList=contents.split(',')
    checkSuperTime(t, fileList)
    checkSuperblockData(t,fileList)
    contents=','.join(fileList)
    superblock.seek(0)
    superblock.truncate()
    superblock.write(contents)
    superblock.close()
    
''' def checkDict(fileList, num, parent, inUse):
        orgList=fileList[2].split('}')
        entry1=orgList[0].split(',')
        temp=[]
        for i in range(0, len(entry1)):
                list1 = entry1[i].strip()
                list1 = list1.split(':')
                temp.append(list1)

        dot1 = False
        dot2 = False
        for entry in temp:
                if (entry1[0]=='d'):
                       if(entry1[1]=='.'):
                                dot1 = True
                                if (int(entry1[2])!=num):
                                        entry1[2]=str(num)
                       elif(entry1[1]=='..'):
                                dot2 = True
                                if(int(entry1[2])!=parent):
                                        entry1[2]=str(parent)
                       else:
                                checkDir(int(entry1[2]),num,inUse)
                                inUse.append(int(entry1[2]))
                else:
                         inUse.append(int(entry1[2]))
                         checkInode(int(entry1[2]), inUse)

        if(not dot1):
                temp.append(['d', '.', str(num)])
        if(not dot2):
                temp.append(['d', '..', str(parent)])
    
        list1=[]
        for entry in temp:
                temp1=':'.join(entry1)
                list1.append(temp1)
                orgList[0]=', '.join(list1)
                fileList[2]='}'.join(entry1)
        return len(list1)
    
def checkDir(num,parent,inUse):
        block1 = FILES_DIR + "/fusedata." + str(num)
        block = open(block1, 'r+')
        contents = block.read()
        if (contents.count('{')!= 2 and contents.count('}') != 2):
                print ("Corrupted directory metadata in fusedata.%d and does match the format.\n" % num)
                return -1
        contents=contents.strip()
        fileList=contents.split('{')
        linkcount=checkDict(fileList,num,parent,inUse)
        fileData=fileList[1].split(',')
        linkData=fileData[7]
        linkList=linkData.split(':')
        linkStr=linkList[1].strip()
        fileData[7]=fileData[7].replace(linkStr,str(linkcount))
        fileList[1]=','.join(fileData)
        contents = '{'.join(fileList)
        block.seek(0)
        block.truncate()
        block.write(contents)
        block.close() '''
    
def freeBlockList(freeBlocks):
    blockFile = {}
    tempFree = []
    index = 0
    for i in range(FREE_START,FREE_END+1):
        block1 = "%s/fusedata.%d" %(FILES_DIR,i)
        blockFile[index] = block1
        index+= 1
        tempFree.append([])
    
    for k in freeBlocks:
        index = int(k/BLOCKS_IN_FREE)
        tempFree[index].append(str(k))
        
        path="%s/fusedata.%d"%(FILES_DIR,k)
        f=open(path,'w')
        f.close()
    
    for l in range(0,len(tempFree)):
        freeStr=', '.join(tempFree[l])
        f=open(blockFile[l], 'w')
        f.write(freeStr)
        f.close()
            
def getFreeblocks():
    list1=[]
    for i in range(ROOT+1,MAX_NUM_BLOCKS):
        list1.append(i)
    return list1


def updateFreeblockList(used):
    all= getFreeblocks()
    used.sort()
    freeBlocks=[]
    for i in all:
        if(used.count(i)==0):
            freeBlocks.append(i)
    
    freeBlockList(freeBlocks)

    
def main():
    checkDeviceId()
    checkSuper(int(time()))
    inUse=[]
 #   checkDir(ROOT,ROOT,inUse)
    updateFreeblockList(inUse)
    checkTimesCall()

if __name__ == "__main__":
    main()
    
    
