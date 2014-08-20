import sys, time, getopt
import random
import thread,urllib2,socket

def get_urls(filename):
    try:
        f =open(filename,'r')
        urls=f.readlines()
        f.close()
    except:
        print "the file does not exist"
    return urls


#def statistics():
#    global total_requests,failed_requests,timeout_requests,total_time 
#    time_constant=time.time()+time_execute
#    for url in urls:
#        while(time_constant>time.time()):
#            total_requests +=1
#            start=time.time()
#            try:
#                webpage=urllib2.urlopen(url)
#                print webpage.geturl()
#                end=time.time()
#                timespan=end-start
#                if webpage.getcode()>400:
#                    failed_requests +=1
#                    continue
#                else:
#                    total_time+=timespan
#                    print "timespan:"+str(timespan)+"\t\t"+"webpage size:"+ webpage.headers["Content-Length"]
#                    
#            except urllib2.URLError:
#                print "time out"
#                timeout_requests +=1
#            
#            break



def connect_test(num,p_detail,urls):
    
    global total_requests,failed_requests,timeout_requests,total_time
    global flag
    
    while flag:
        
        index=random.randint(0,len(urls)-1)
        total_requests+=1
        
        start=time.time()
        
        try:
            webpage=urllib2.urlopen(urls[index])
            end=time.time()
            if p_detail:
                print "This is the thread #"+str(num)
                print webpage.geturl()
            timespan=end-start
            if webpage.getcode()>=400:
                failed_requests+=1
            else:
                total_time+=timespan
                if p_detail:
                    print "timespan:"+str(timespan)+"\t\t"+"webpage size:"+ webpage.headers["Content-Length"]
        except urllib2.URLError:
            if p_detail:
                print webpage.geturl()
                print "connect the url timed out"
            timeout_requests+=1         
    return


if __name__ == '__main__':


    global time_execute
    global flag
    global total_requests,failed_requests,timeout_requests,total_time 
    socket.setdefaulttimeout(3.0) 
    
    time_execute=1
    nThread=3
    p_detail=False

    opts, args = getopt.getopt(sys.argv[1:], "f:t:d", ["thread="])
    for o, value in opts:
        if o in ('-f'):
            print "**********\t"+"file: "+value+"\t**********"
            filename=value
            urls= get_urls(filename)
        elif o in ('-t'):
            print "**********\t"+"time_execute: "+value+'min'+"\t**********"
            time_execute=float(value)*60
        elif o in ("--thread"):
            print "**********\t"+"nThread: "+value+"\t**********"
            nThread=int(value)
        elif o in ('-d'):
            print "**********\t"+"Print the connection detail... "+"\t**********"
            p_detail=True
        
    total_requests=failed_requests=timeout_requests=total_time=0 
    flag=True   #the thread will be terminated when flag is false
    threads=[]  #define the list of thread
    
    print "Testing the website ...."  
    print "---------------------------------------------------------------------------------------------------------"      
    i=0
    while(i<nThread):
        i+=1
        t=thread.start_new_thread(connect_test,(i,p_detail,urls))
        threads.append(t)

    time.sleep(time_execute)
    flag=False
         
    success_requests=total_requests-failed_requests-timeout_requests     
    Average_Response_Time=total_time/success_requests
    
    print "---------------------------------------------------------------------------------------------------------"
    print "**********\t"+"total_requests: "+str(total_requests)+'\t'+"failed_requests: "+str(failed_requests)+'\t'+"timeout_requests: "+str(timeout_requests)+"\t**********"
    print "**********\t"+"Average Response Time: "+str(Average_Response_Time)+'s'+"\t\t**********"


