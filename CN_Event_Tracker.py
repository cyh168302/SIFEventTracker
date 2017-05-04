#!/usr/bin/python
# -*- coding: cp936 -*-
import os
import urllib2,json,time
import hmac
import hashlib
import json
import pycurl
import StringIO
import gzip
import threading
import re
import random
import thread
import matplotlib.pyplot as plt
from Tkinter import *
from tkMessageBox import *
from string import *
from datetime import *
from time import *

global timeaxis
global rank_1
global rank_2
global rank_3
global rank_4
global rank_5
global s_time
global e_time
global r
global r2
global start_time
global end_time
global hour_speed
global s1
global s2
global infolabel
global ival_time
global pt_change
global u_time
global c_pt
global user_token
global user_uid
global event_id
global user_token_input
global user_uid_input
global event_id_input
global ival
global system_logs
global writeflag
global b1
global b2
global e1
global e2
global e3

def sys_clock():
    while 1:
        printinfo(11,time_trans(int(time())))
        sleep(0.2)
        
def syslog(status):
    global system_logs
    if status==1:
        temp="Success!Current time: "+ctime()
        system_logs=system_logs+[temp]
        if len(system_logs)>11:del system_logs[0]
        info2=""
        for i in range(len(system_logs)):info2=info2+system_logs[i]+"\n"
        printinfo(10,info2)
    elif status==2:
        temp="System Acticed!"
        system_logs=system_logs+[temp]
        if len(system_logs)>11:del system_logs[0]
        info2=""
        for i in range(len(system_logs)):info2=info2+system_logs[i]+"\n"
        printinfo(10,info2)
    elif status==3:
        temp="System Paused!"
        system_logs=system_logs+[temp]
        if len(system_logs)>11:del system_logs[0]
        info2=""
        for i in range(len(system_logs)):info2=info2+system_logs[i]+"\n"
        printinfo(10,info2)
    else:
        temp="Request Timed Out!"
        system_logs=system_logs+[temp]
        if len(system_logs)>11:del system_logs[0]
        info2=""
        for i in range(len(system_logs)):info2=info2+system_logs[i]+"\n"
        printinfo(10,info2)

def ChangeInterval():
    global ival
    global r2
    ival=r2.get()

def ChangeUserInfo():
    global user_token
    global user_uid
    global event_id
    global user_token_input
    global user_uid_input
    global event_id_input
    global writeflag
    global b1
    global b2
    global e1
    global e2
    global e3
    event_id=int(event_id_input.get())
    user_token=user_token_input.get()
    user_uid=user_uid_input.get()
    writeflag=1
    b1.config(state=DISABLED)
    b2.config(state=NORMAL)
    e1.config(state=DISABLED)
    e2.config(state=DISABLED)
    e3.config(state=DISABLED)
    syslog(2)

def sys_pause():
    global writeflag
    global b1
    global b2
    global e1
    global e2
    global e3
    writeflag=0
    b1.config(state=NORMAL)
    b2.config(state=DISABLED)
    e1.config(state=NORMAL)
    e2.config(state=NORMAL)
    e3.config(state=NORMAL)
    syslog(3)

def get_help():
    showinfo("How to use...",
             "About the event_id:\n"+
             "     Different event_id represents different events. Do not change unless you know the exact id of an event.\n\n"
             "About the uid and token:\n"+
             "     Every account in the game has an unique uid and token.\n"+
             "     This client use the uid and token to simulate the login operation in the game,And then get the event ranking list and analyze it automaticly to get all statistics.\n"+
             "     Get the uid and token of your account at the website 120.27.114.53/sdoapi\n"+
             "     There's a default account for probation. But it is recommended to use your own account for this client.\n\n"+
             "Tips:\n     Do not login your account during using this client, because it can cause the change of the token.")
    
def sendRequest(body):
	global user_token
	global user_uid
	TM2 = time()
	TM = str(int(TM2))
	TM2 = str(TM2)
	body["timeStamp"]=TM
	body["commandNum"]="923405554." + TM2
	
	conf = {"appid": "626776655", "tZone": "JST", "region": "392", 
	"token": user_token, 
	"nonce": "6", "uid": user_uid, "hmackey": "pwcmuUADRP6A2DcirAo4K+ZLaFg1XEvDpG+Qc0+BjU8"}

	
	conf['rankurl'] = "http://prod.game1.ll.sdo.com/main.php/"+body["module"]+"/"+body["action"]

	

	def get_signature(s):
		hmackey = bytes(conf['hmackey'])
		return hmac.new(hmackey, s, hashlib.sha1).hexdigest()

	def getrankbody():
		return json.dumps(body)

	def get_tcp_header():
		return [
			"Expect: ",
			"API-Model: straightforward",
			"Debug: 1",
			"Bundle-Version: 3.1.2.2",
			"Client-Version: 3.1.79",
			"OS-Version: TianTian TTAndroid unknown",
			"OS: Android",
			"Platform-Type: 2",
			"Application-ID: " + conf['appid'],
			"Time-Zone: " + conf['tZone'],
			"Region: " + conf['region'],
			"Authorize: consumerKey=lovelive_test&timeStamp=" + TM + "&version=1.1&token=" + conf['token'] + "&nonce=" + conf['nonce'],
			"User-ID: " + conf['uid'],
			"X-Message-Code: " + get_signature(getrankbody()),
		]	

	c = pycurl.Curl()
	c.setopt(pycurl.USERAGENT, '')
	c.setopt(pycurl.URL, conf['rankurl'])
	c.setopt(pycurl.HTTPHEADER, get_tcp_header())
	c.setopt(pycurl.CONNECTTIMEOUT, 15)
	c.setopt(pycurl.TIMEOUT, 15)
	c.setopt(pycurl.CUSTOMREQUEST, 'POST')
	c.setopt(pycurl.HTTPPOST, [('request_data', getrankbody())])
	b = StringIO.StringIO()
	c.setopt(pycurl.WRITEFUNCTION, b.write)
	c.perform()
	return json.loads(b.getvalue())

def getdata():#1-5
    f=open("log2.txt","a")
    body = {"module":"ranking", "action":"eventPlayer","rank":1,"limit":5, "event_id": event_id}
    try:
        q = sendRequest(body)
        f.write(str(int(time()))+" ")
        for data in q['response_data']['items']:
                    #print data
                    #print data['rank'], #data['user_data']['name'],
                f.write(str(data['score'])+" ")      
        #print "Success!Current time: "+ctime()
        f.write("\n")
        f.close()
        return 1
    except:
        f.close()
        return 0

def getdata2():#2300  #11500
    f=open("log3.txt","a")
    body = {"module":"ranking", "action":"eventPlayer","rank":2300,"limit":1, "event_id": event_id}
    try:
        q = sendRequest(body)
        f.write(str(int(time()))+" ")
        for data in q['response_data']['items']:
                    #print data
                    #print data['rank'], #data['user_data']['name'],
                f.write(str(data['score'])+" ")
        body = {"module":"ranking", "action":"eventPlayer","rank":11500,"limit":1, "event_id": event_id}
        q = sendRequest(body)
        for data in q['response_data']['items']:
                    #print data
                    #print data['rank'], #data['user_data']['name'],
                f.write(str(data['score'])+" ") 
        #print "Success!Current time: "+ctime()
        f.write("\n")
        f.close()
        return 1
    except:
        f.close()
        return 0
    
def writedata():
    global ival
    global writeflag
    while 1:
        if writeflag:
            a=getdata()
            b=getdata2()
            syslog(a*b)
            sleep(ival-0.352)

def time_trans(time1):
    #时间格式转换
    time_local=localtime(time1)
    time2=strftime("%Y-%m-%d %H:%M:%S",time_local)
    return time2

def printinfo(Label_no,s):
    global infolabel
    infolabel[Label_no]["text"]=s
    

def read_data():
    global timeaxis
    global rank_1
    global rank_2
    global rank_3
    global rank_4
    global rank_5
    global s_time
    global e_time
    global hour_speed
    global s1
    global s2
    global ival_time
    global pt_change
    global u_time
    global c_pt
    
    f=open("log2.txt","r")
    output=f.read()
    events=split(output)
    l=len(events)

    timeaxis=[]
    rank_1=[]
    rank_2=[]
    rank_3=[]
    rank_4=[]
    rank_5=[]

    if s1.get():s_time=int(events[0])
    if s2.get():e_time=2147483647

    u_time=int(events[l-6])
    
    for i in range(l):
        if i%6==0:timeaxis=timeaxis+[int(events[i])-s_time]
        elif i%6==1:rank_1=rank_1+[int(events[i])]
        elif i%6==2:rank_2=rank_2+[int(events[i])]
        elif i%6==3:rank_3=rank_3+[int(events[i])]
        elif i%6==4:rank_4=rank_4+[int(events[i])]
        elif i%6==5:rank_5=rank_5+[int(events[i])]
        
    f.close()

    c_pt=[rank_1[l/6-1],rank_2[l/6-1],rank_3[l/6-1],rank_4[l/6-1],rank_5[l/6-1]]
    
    #时速计算
    i=0
    while timeaxis[i]<timeaxis[l/6-1]-3600:
        i=i+1
    hour_speed[0]=rank_1[l/6-1]-rank_1[i]
    hour_speed[1]=rank_2[l/6-1]-rank_2[i]
    hour_speed[2]=rank_3[l/6-1]-rank_3[i]
    hour_speed[3]=rank_4[l/6-1]-rank_4[i]
    hour_speed[4]=rank_5[l/6-1]-rank_5[i]

    #上次结算以及pt变化计算
    i=0
    while rank_1[i]!=rank_1[l/6-1]:
        i=i+1
    ival_time[0]=timeaxis[l/6-1]-timeaxis[i]
    pt_change[0]=rank_1[l/6-1]-rank_1[i-1]
    
    i=0
    while rank_2[i]!=rank_2[l/6-1]:
        i=i+1
    ival_time[1]=timeaxis[l/6-1]-timeaxis[i]
    pt_change[1]=rank_2[l/6-1]-rank_2[i-1]

    i=0
    while rank_3[i]!=rank_3[l/6-1]:
        i=i+1
    ival_time[2]=timeaxis[l/6-1]-timeaxis[i]
    pt_change[2]=rank_3[l/6-1]-rank_3[i-1]

    i=0
    while rank_4[i]!=rank_4[l/6-1]:
        i=i+1
    ival_time[3]=timeaxis[l/6-1]-timeaxis[i]
    pt_change[3]=rank_4[l/6-1]-rank_4[i-1]

    i=0
    while rank_5[i]!=rank_5[l/6-1]:
        i=i+1
    ival_time[4]=timeaxis[l/6-1]-timeaxis[i]
    pt_change[4]=rank_5[l/6-1]-rank_5[i-1]
    
    #选取时间段
    i=0
    while timeaxis[i]<0:
        i=i+1
    flag_low=i
    while timeaxis[i]<e_time-s_time:
        if i==l/6-1:break
        i=i+1
    flag_high=i+1
    timeaxis=timeaxis[flag_low:flag_high]
    rank_1=rank_1[flag_low:flag_high]
    rank_2=rank_2[flag_low:flag_high]
    rank_3=rank_3[flag_low:flag_high]
    rank_4=rank_4[flag_low:flag_high]
    rank_5=rank_5[flag_low:flag_high]

def GetResult1():
    global rank
    global timeaxis
    global rank_1
    global rank_2
    global rank_3
    global rank_4
    global rank_5
    global s_time
    global e_time

    rank=int(r.get())
    s_time_c=datetime(int(start_time[0].get()),int(start_time[1].get()),int(start_time[2].get()),int(start_time[3].get()),int(start_time[4].get()),int(start_time[5].get()))
    s_time=int(mktime(s_time_c.timetuple()))
    e_time_c=datetime(int(end_time[0].get()),int(end_time[1].get()),int(end_time[2].get()),int(end_time[3].get()),int(end_time[4].get()),int(end_time[5].get()))
    e_time=int(mktime(e_time_c.timetuple()))
    read_data()
    if rank==1:
        plt.plot(timeaxis,rank_1)
        timer=float(timeaxis[len(timeaxis)-1]-timeaxis[0])
        pt_change=rank_1[len(rank_1)-1]-rank_1[0]
        printinfo(6,"Lenth of the selected time zone:  "+str(int(timer))+" s\n"+
                  "average speed per 1h:  "+str(int(pt_change/timer*3600)))
    elif rank==2:
        plt.plot(timeaxis,rank_2)
        timer=float(timeaxis[len(timeaxis)-1]-timeaxis[0])
        pt_change=rank_2[len(rank_2)-1]-rank_2[0]
        printinfo(6,"Lenth of the selected time zone:  "+str(int(timer))+" s\n"+
                  "average speed per 1h:  "+str(int(pt_change/timer*3600)))
    elif rank==3:
        plt.plot(timeaxis,rank_3)
        timer=float(timeaxis[len(timeaxis)-1]-timeaxis[0])
        pt_change=rank_3[len(rank_3)-1]-rank_3[0]
        printinfo(6,"Lenth of the selected time zone:  "+str(int(timer))+" s\n"+
                  "average speed per 1h:  "+str(int(pt_change/timer*3600)))
    elif rank==4:
        plt.plot(timeaxis,rank_4)
        timer=float(timeaxis[len(timeaxis)-1]-timeaxis[0])
        pt_change=rank_4[len(rank_4)-1]-rank_4[0]
        printinfo(6,"Lenth of the selected time zone:  "+str(int(timer))+" s\n"+
                  "average speed per 1h:  "+str(int(pt_change/timer*3600)))
    elif rank==5:
        plt.plot(timeaxis,rank_5)
        timer=float(timeaxis[len(timeaxis)-1]-timeaxis[0])
        pt_change=rank_5[len(rank_5)-1]-rank_5[0]
        printinfo(6,"Lenth of the selected time zone:  "+str(int(timer))+" s\n"+
                  "average speed per 1h:  "+str(int(pt_change/timer*3600)))
    plt.show()
    
def GetResult2():
    global hour_speed
    global ival_time
    global pt_change
    global u_time
    global c_pt
    rank=int(r.get())
    read_data()
    for i in range(5):
        printinfo(i,"Current event pt:  "+str(c_pt[i])+"\n"+
                  "speed in last 1h:  "+str(hour_speed[i])+"\n"+
                  "last live in:  "+str(ival_time[i])+
                  "  sec  ,  event pt change:  "+str(pt_change[i]))
    printinfo(5,"Updated at "+time_trans(u_time))

def GetResult3():
    f=open("log3.txt","r")
    output=f.read()
    events=split(output)
    l=len(events)
    f.close()
    
    timeaxis2=[]
    rank_2300=[]
    rank_11500=[]
    
    for i in range(l):
        if i%3==0:timeaxis2=timeaxis2+[int(events[i])]
        elif i%3==1:rank_2300=rank_2300+[int(events[i])]
        elif i%3==2:rank_11500=rank_11500+[int(events[i])]

    flag=0
    for i in range(l/3):
        if timeaxis2[i]>timeaxis2[l/3-1]-600:break
        flag=i
        
    speed_2300=(float(rank_2300[l/3-1]-rank_2300[flag]))*600/(timeaxis2[l/3-1]-timeaxis2[flag])
    speed_11500=(float(rank_11500[l/3-1]-rank_11500[flag]))*600/(timeaxis2[l/3-1]-timeaxis2[flag])

    printinfo(7,"Current:  "+str(rank_2300[l/3-1])+"\nspeed:  "+str(speed_2300)+"  pt/10min")
    printinfo(8,"Current:  "+str(rank_11500[l/3-1])+"\nspeed:  "+str(speed_11500)+"  pt/10min")
    printinfo(9,"Updated at "+time_trans(timeaxis2[l/3-1]))

writeflag=0
ival=30
event_id=65
user_uid="5260208"
user_token="djT2ED0efqPdQ51dm8ThJh8aY6kepnDy3rHNrCuK0iMGaPz6ZxxO2SzDrsLxsZacSUsf9cZUNSJynmKa0azloAa"

timeaxis=[]
rank_1=[]
rank_2=[]
rank_3=[]
rank_4=[]
rank_5=[]

infolabel=[]
system_logs=[]

ival_time=[0,0,0,0,0]
pt_change=[0,0,0,0,0]
hour_speed=[0,0,0,0,0]
c_pt=[0,0,0,0,0]

root=Tk()
root.title("CN SIF event pt tracker by:@cyh0613")
windowProperty="1024x640"
root.geometry(windowProperty)

user_uid_input=StringVar()
user_token_input=StringVar()
event_id_input=StringVar()
event_id_input.set("65")
user_uid_input.set("5260208")
user_token_input.set("djT2ED0efqPdQ51dm8ThJh8aY6kepnDy3rHNrCuK0iMGaPz6ZxxO2SzDrsLxsZacSUsf9cZUNSJynmKa0azloAa")

Frame(root,width=660,height=170,bd=5,relief="groove").place(x=350,y=175,anchor=NW)
Frame(root,width=213,height=150,bd=5,relief="groove").place(x=350,y=15,anchor=NW)
Frame(root,width=440,height=150,bd=5,relief="groove").place(x=570,y=15,anchor=NW)
Frame(root,width=300,height=260,bd=5,relief="groove").place(x=350,y=355,anchor=NW)
Frame(root,width=335,height=260,bd=5,relief="groove").place(x=675,y=355,anchor=NW)
Frame(root,width=300,height=600,bd=5,relief="groove").place(x=180,y=315,anchor=CENTER)
#设置默认时间
default_time=[localtime().tm_year,localtime().tm_mon,localtime().tm_mday,
 localtime().tm_hour,localtime().tm_min,localtime().tm_sec]
#查询起始时间输入
x1=StringVar()
x1.set(str(default_time[0]))
x2=StringVar()
x2.set(str(default_time[1]))
x3=StringVar()
x3.set(str(default_time[2]))
x4=StringVar()
x4.set("0")
x5=StringVar()
x5.set("0")
x6=StringVar()
x6.set("0")
y1=StringVar()
y1.set(str(default_time[0]))
y2=StringVar()
y2.set(str(default_time[1]))
y3=StringVar()
y3.set(str(default_time[2]))
y4=StringVar()
y4.set(str(default_time[3]))
y5=StringVar()
y5.set(str(default_time[4]))
y6=StringVar()
y6.set(str(default_time[5]))
start_time=[x1,x2,x3,x4,x5,x6]
end_time=[y1,y2,y3,y4,y5,y6]
for i in range (6):
    if i==0:Label(root,text="Year").place(x=i*80+450,y=200,anchor=CENTER)
    elif i==1:Label(root,text="Month").place(x=i*80+450,y=200,anchor=CENTER)
    elif i==2:Label(root,text="Day").place(x=i*80+450,y=200,anchor=CENTER)
    elif i==3:Label(root,text="Hour").place(x=i*80+450,y=200,anchor=CENTER)
    elif i==4:Label(root,text="Minute").place(x=i*80+450,y=200,anchor=CENTER)
    elif i==5:Label(root,text="Second").place(x=i*80+450,y=200,anchor=CENTER)
    Entry(root,textvariable=start_time[i],width=8).place(x=i*80+420,y=220,anchor=NW)
    Entry(root,textvariable=end_time[i],width=8).place(x=i*80+420,y=250,anchor=NW)   
Label(root,text="From:").place(x=360,y=220,anchor=NW)
Label(root,text="To:").place(x=370,y=250,anchor=NW)
Label(root,text="-").place(x=484,y=220,anchor=NW)
Label(root,text="-").place(x=484,y=250,anchor=NW)
Label(root,text="-").place(x=564,y=220,anchor=NW)
Label(root,text="-").place(x=564,y=250,anchor=NW)
Label(root,text=":").place(x=725,y=220,anchor=NW)
Label(root,text=":").place(x=725,y=250,anchor=NW)
Label(root,text=":").place(x=805,y=220,anchor=NW)
Label(root,text=":").place(x=805,y=250,anchor=NW)
#查询排名输入
r=StringVar()
r.set("2")
Radiobutton(root,text="#1",variable=r,value="1").place(x=180,y=80,anchor=CENTER)
Radiobutton(root,text="#2",variable=r,value="2").place(x=180,y=180,anchor=CENTER)
Radiobutton(root,text="#3",variable=r,value="3").place(x=180,y=280,anchor=CENTER)
Radiobutton(root,text="#4",variable=r,value="4").place(x=180,y=380,anchor=CENTER)
Radiobutton(root,text="#5",variable=r,value="5").place(x=180,y=480,anchor=CENTER)
#系统设置
r2=IntVar()
r2.set(30)
Radiobutton(root,text="1s",variable=r2,value=1).place(x=360,y=50,anchor=NW)
Radiobutton(root,text="5s",variable=r2,value=5).place(x=430,y=50,anchor=NW)
Radiobutton(root,text="10s",variable=r2,value=10).place(x=500,y=50,anchor=NW)
Radiobutton(root,text="20s",variable=r2,value=20).place(x=360,y=85,anchor=NW)
Radiobutton(root,text="30s",variable=r2,value=30).place(x=430,y=85,anchor=NW)
Radiobutton(root,text="1min",variable=r2,value=60).place(x=500,y=85,anchor=NW)

Label(root,text="Time interval of sending request").place(x=456,y=33,anchor=CENTER)
Label(root,text="event_id:").place(x=640,y=35,anchor=NE)
Label(root,text="uid:").place(x=830,y=35,anchor=NE)
Label(root,text="token:").place(x=632,y=75,anchor=NE)
e1=Entry(root,textvariable=event_id_input,width=8)
e1.place(x=660,y=35,anchor=NW)
e2=Entry(root,textvariable=user_uid_input,width=8)
e2.place(x=850,y=35,anchor=NW)
e3=Entry(root,textvariable=user_token_input,width=45)
e3.place(x=660,y=75,anchor=NW)

#时间选项
s1=IntVar()
s1.set(0)
Checkbutton(root,variable=s1,text="The earliest time").place(x=940,y=230,anchor=CENTER)
s2=IntVar()
s2.set(1)
Checkbutton(root,variable=s2,text="The current time").place(x=940,y=260,anchor=CENTER)
#执行按钮
Button(root,text="Get Line Chart",command=GetResult1).place(x=510,y=310,anchor=CENTER)
Button(root,text="Refresh",command=GetResult2).place(x=180,y=580,anchor=CENTER)
Button(root,text="Refresh",command=GetResult3).place(x=500,y=580,anchor=CENTER)
Button(root,text="Change",command=ChangeInterval).place(x=456,y=135,anchor=CENTER)
b1=Button(root,text="Comfirm and Start",command=ChangeUserInfo)
b1.place(x=785,y=135,anchor=CENTER)
b2=Button(root,text="Pause",command=sys_pause,state=DISABLED)
b2.place(x=645,y=135,anchor=CENTER)
Button(root,text="Help...",command=get_help).place(x=925,y=135,anchor=CENTER)

#显示信息
Label(root,text="#2300").place(x=500,y=400,anchor=CENTER)
Label(root,text="#11500").place(x=500,y=485,anchor=CENTER)
Label(root,text="System log").place(x=842,y=390,anchor=CENTER)
#no.0-no.4:1-5名信息
for i in range(5):
    temp_label=Label(root,text="")
    temp_label.place(x=180,y=i*100+125,anchor=CENTER)
    infolabel=infolabel+[temp_label]
#no.5:更新时间    
time_label=Label(root,text="")
time_label.place(x=180,y=40,anchor=CENTER)
infolabel=infolabel+[time_label]
#no.6:区间速度显示
label2=Label(root,text="")
label2.place(x=830,y=310,anchor=CENTER)
infolabel=infolabel+[label2]
#no.7:#2300
label3=Label(root,text="")
label3.place(x=500,y=435,anchor=CENTER)
infolabel=infolabel+[label3]
#no.8:#11500
label4=Label(root,text="")
label4.place(x=500,y=525,anchor=CENTER)
infolabel=infolabel+[label4]
#no.9:更新时间2
label5=Label(root,text="")
label5.place(x=500,y=375,anchor=CENTER)
infolabel=infolabel+[label5]
#no.10:系统日志
label6=Label(root,text="")
label6.place(x=703,y=400,anchor=NW)
infolabel=infolabel+[label6]
#no.11:时钟
label7=Label(root,text="")
label7.place(x=842,y=372,anchor=CENTER)
infolabel=infolabel+[label7]

thread.start_new_thread(sys_clock,())
thread.start_new_thread(writedata,())

#初始化
rank=int(r.get())
s_time_c=datetime(int(start_time[0].get()),int(start_time[1].get()),int(start_time[2].get()),int(start_time[3].get()),int(start_time[4].get()),int(start_time[5].get()))
e_time_c=datetime(int(end_time[0].get()),int(end_time[1].get()),int(end_time[2].get()),int(end_time[3].get()),int(end_time[4].get()),int(end_time[5].get()))
s_time=int(mktime(s_time_c.timetuple()))
e_time=int(mktime(e_time_c.timetuple()))

root.mainloop()












