# -*- coding: utf-8 -*-

# since wx was not recognized by git during deployment, changed it back to tkinter
# this is the latest


# streamlit application : Attendance automation v4
# added: 
# i) looping to process multiple input files
# ii) check if an input file has already been processed

import streamlit as st
from PIL import Image
# import wx

import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

import pandas as pd
import os
import time
import datetime
import warnings
warnings.filterwarnings('ignore')
import re

# streamlit run D:\stackroute\2_AI-assisted-programming\learning_requirements\1_AI_GenAI\useCases\niit\projects\2.1_attendance\code\sl\attendance-v4.py

# ============
# page design
# ============
st.set_page_config(layout='wide')

with st.container():
    mc1,mc2,mc3,mc4 = st.columns(4)
    mc4.write("Today is : " + datetime.datetime.today().strftime("%A") + ", " + time.strftime("%d-%B-%Y"))

# =====================
# session state values
# =====================
if 'flg_config' not in st.session_state:
    st.session_state['flg_config'] = True

if "source" not in st.session_state:
    st.session_state['source'] = None

if "destination" not in st.session_state:
    st.session_state['destination'] = None
    
if "processed" not in st.session_state:
    st.session_state['processed'] = None
    
if "config" not in st.session_state:
    st.session_state["config"] = None
    
if "df_config" not in st.session_state:
    st.session_state["df_config"] = pd.DataFrame()
    
if "total_duration" not in st.session_state:
    st.session_state["total_duration"] = 0
    
if "present_flags" not in st.session_state:
    st.session_state["present_flags"] = True

if "fdp" not in st.session_state:
    st.session_state["fdp"] = 0.0
    
if "hdp" not in st.session_state:
    st.session_state["hdp"] = 0.0
    
if "absent" not in st.session_state:
    st.session_state["absent"] = 0.0
    
if "attendanceclick" not in st.session_state:
   st.session_state['attendanceclick'] = False
   
if "showconfig" not in st.session_state:
    st.session_state['showconfig'] = 0

if "viewattendance" not in st.session_state:
    st.session_state["viewattendance"] = 0

# ===============
# local variables
# ===============
# bg = "D:/stackroute/2_AI-assisted-programming/learning_requirements/1_AI_GenAI/useCases/niit/projects/2.1_attendance/dataset/att.jpg"
# att_config = "D:/config/attendance.csv"

bg = "D:/stackroute/2_AI-assisted-programming/learning_requirements/1_AI_GenAI/useCases/niit/projects/2.1_attendance/img/att.jpg"
att_config = "D:/stackroute/2_AI-assisted-programming/learning_requirements/1_AI_GenAI/useCases/niit/projects/2.1_attendance/config/attendance.csv"

# select the input file path, output file and processed file path

# ===================
# funciton: homepage
# ===================
def homepage():
    st.header("Attendance System")
    c1,c2 = st.columns([0.5,0.5])
    c1.image(Image.open(bg)) #,caption="Participant's Attendance marking system")
    c2.write("Automatically update participant attendance")
    c2.write("View participant attendance details")

# # ===================
# # funciton: clearkeys
# # ===================
# def clearkeys():
#     if (len(st.session_state.keys()) > 0):
#         for k in st.session_state.keys():
#             del st.session_state[k]

# ==========================
# funciton: selectfilefolder
# ==========================
# def selectfilefolder(which):
    # app = wx.App()
    # path = None
    
    # if (which == "file"):
        # wildcard = "CSV files |*.csv"
        # with wx.FileDialog(None,"Select files", wildcard=wildcard, style=wx.FD_OPEN) as dlg:
            # if dlg.ShowModal() == wx.ID_OK:
                # path = dlg.GetPaths()
            # else:
                # path = None
    # elif (which == "folder"):
        # with wx.DirDialog (None, "Choose directory", "", wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dlg:
            # if dlg.ShowModal() == wx.ID_OK:
                # path = dlg.GetPath()
            # else:
                # path = None
            
    # return(path)    

# ==========================
# funciton: selectfilefolder
# ==========================
def selectfilefolder(which):
    
    if (which == "folder"):
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory(master=root)
        root.destroy()
        st.write(path)
    elif (which == "file"):
        path = askopenfilename()
        st.write(path)

    return(path)    


# ========================
# funciton: showconfig
# ========================
def showconfig():
    df_config = pd.read_csv(att_config)
    
    st.session_state["source"] = df_config.source.values[0]
    st.session_state["destination"] = df_config.destination.values[0]
    st.session_state["processed"] = df_config.processed.values[0]
    
    st.session_state["fdp"] = df_config.full_att.values[0]
    st.session_state["hdp"] = df_config.half_att.values[0]
    st.session_state["absent"] = df_config.absent.values[0]

    st.session_state["df_config"] = df_config
    
    # if loc!="start":
    #     if st.session_state['flg_config']:
    #         st.dataframe(st.session_state['df_config'].T)


# ========================
# funciton: configurepaths
# ========================
def configurepaths():
    st.header("Configure File and Directory paths")
    st.divider()
    
    # st.subheader("Current Configurations")
    # showconfig()
    # st.divider()

    # c1,c2,c3,c4,c5,c6 = st.columns([0.25,0.25,0.25,0.08,0.08,0.08])
    
    c1,c2,c3,c4,c5,c6 = st.columns(6)

    b1 = c1.button(":file_folder:",help="Select Source Directory") #,help=st.session_state['source'])
    if b1:
        path = selectfilefolder("folder")
        if path is not None:
            path = path + "\\"
            st.session_state['source'] = path

    b2 = c2.button(":card_index_dividers:",help="Select Destination File") #,help=st.session_state['destination'])
    if b2:
        path = selectfilefolder("file")
        if path is not None:
            st.session_state['destination'] = path
        # st.write(path[0])

    b3 = c3.button(":wastebasket:",help="Select Processed Directory") #,help=st.session_state['processed'])
    if b3:
        path = selectfilefolder("folder")
        if path is not None:
            path = path + "\\"
            st.session_state['processed'] = path
        # st.write(path)
    
    b4 = c4.button(":writing_hand:",help="Configure Attendance cut-offs")
    if b4:
        st.session_state['attendanceclick'] = True
        # st.write(st.session_state['attendanceclick'])
        # time.sleep(10)
    
    if st.session_state['attendanceclick']:
        if "b4btn" not in st.session_state:
            st.session_state['b4btn'] = False
    
        if b4 or st.session_state['b4btn']:
            st.session_state['b4btn'] = True
        
        pc = st.empty()
        with pc.form("b4form"):
            lc1,lc2,lc3,lc4,lc5 = st.columns(5)
            fdp = lc1.number_input("Full day Present",min_value=0.7,max_value=1.0)
            hdp = lc2.number_input("Half-day Present",min_value=0.4,max_value=0.69)
            absent = lc3.number_input("Absent",min_value=0.0,max_value=0.25)
            savechanges = lc4.checkbox("Save changes")
            submitted = lc5.form_submit_button(":large_green_circle:",help="Save/Discard settings and Close")
            
            if submitted:
                # st.write('submitted true')
                # time.sleep(10)
                if (savechanges):
                    st.session_state["fdp"] = fdp
                    st.session_state["hdp"] = hdp
                    st.session_state["absent"] = absent
                
                st.session_state['attendanceclick'] = False
                pc.empty()
                
               
    # save configurations
    b5 = c5.button(":key:",help="Save configurations")
    if (b5):
        src = st.session_state['source']
        dest = st.session_state['destination']
        proc = st.session_state['processed']
        fdp = st.session_state["fdp"]
        hdp = st.session_state["hdp"]
        absent = st.session_state["absent"]
        
        df = pd.DataFrame({'source':[src],'destination':[dest],'processed':[proc],
                               'full_att':[fdp],'half_att':[hdp],'absent':[absent] })
        # st.write(df)
        df.to_csv(att_config,index=False)
        
    if c6.button(":arrow_double_up:",help="Show / Hide configurations"):
        if st.session_state['showconfig']%2 == 0:
            st.write()
            st.subheader("Current Configurations")
            showconfig()
            if st.session_state['flg_config']:
                st.dataframe(st.session_state['df_config'].T)
        else:
            st.write()
        st.session_state['showconfig']+=1
        
#    if c7.button(":arrow_double_down:",help="Hide configurations"):
#        st.write()


# ===================
# funciton: getdata
# ===================
def getdata(file):
 try:
    fp = open(file,'r')
    content = fp.read()
    fp.close()
    
    if "\t" in content:
        # print("file has tabs. Fixing ...!!!")
        data = ''
        spchar = ['ÿ','þ','\x00']
        for i in range(len(content)):
            # time.sleep(0.01)
            if content[i] in spchar:
                continue
            else:
                data+=content[i].encode('utf-8','ignore').decode('utf-8')
        
        data = data.replace("\t",',')
        content = data
    
    # get the overall meeting duration from the input file
    # this is used to calculate per used attendance %
    s_duration = "Meeting duration"
    begin = content.find(s_duration) + len(s_duration) + 1
    total_duration = content[begin:begin+10]
    _,total_duration_seconds = formattime(total_duration)
    
    st.session_state["total_duration"] = total_duration_seconds
    
    # extract the participant attendance data between the strings "Participants" and "3. In-Meeting Activities"
    start = "Participants"
    len_start = len(start)
    end = "3. In-Meeting Activities"
   
    pos_start = content.find(start) + len_start
    pos_end = content.find(end)
    
    # print("start = ",pos_start, " end = ", pos_end)
    
    attendance_data = content[pos_start:pos_end]
    attendance_data_list = attendance_data.split("\n")
    
    # clean up the list
    ndx = []
    for i in range(len(attendance_data_list)):
        row = attendance_data_list[i]
        
        if len(row) <= 0:
            ndx.append(i)
            
        if row.startswith(","):
             ndx.append(i)
    
    res_list = [value for idx,value in enumerate(attendance_data_list) if idx not in ndx]
    
    # return(content,attendance_data_list)
    # return(res_list)
    
    df_attendance_data = pd.DataFrame()

    for i in range(len(res_list)):
        row = res_list[i]
        values = row.split(",")
            
        if values[0].startswith("Name"):
            cols = values
        else:
            split1 = row.split('"')
            
            data = []
            for sp in split1:
                if sp.endswith("AM") or sp.endswith("PM"):
                    data.append(sp.strip())
                else:
                    split2 = sp.split(",")
                    for s in split2:
                        if len(s) > 0:
                            data.append(s)
            
            df_attendance_data = pd.concat([df_attendance_data,pd.DataFrame(data).T])
        
    # new column names
    cols = ["name","firstjoin","lastleave","duration","email","upn", "role"]
    
    df_attendance_data.columns = cols
    df_attendance_data = df_attendance_data.reset_index(drop=True)
    df_attendance_data['total_duration'] = total_duration_seconds # to calculate the attendance %
    
    # return(res_list,df_attendance_data,cols)
    return(1,df_attendance_data)

 except Exception as e:
     return(-1,e)


# ===================================================================
# function: formatdestfile
# description: change the data types of some columns to the right type
# ====================================================================
def formatdestfile(df_out):
 try:
    # replace all null column values with 0
    if df_out.isna().any().sum() > 0:
        df_out = df_out.fillna(0)

    # change the data types for the following columns to integer
    cols_to_int = ['planned_training','trg_compl', 'rem_days', 'trg_conducted','trg_attended']
    df_out[cols_to_int] = df_out[cols_to_int].astype(int)
    
    return(1,df_out)
 
 except Exception as e:
     return(-1,e)

# ======================================================
# function : formattime
# description : format the time and convert into seconds
# ======================================================
def formattime(duration):
    
    component = ["h","m","s"]
    timeval = []
    totalseconds = 0
    
    # st.write("in format time. Duration = ", duration)
    
    for c in component:
        pos = duration.find(c)
        if pos >= 0:
            value = duration[0:pos]
            duration = duration[pos+1:].strip()
            if len(value) < 2:
                value = "0" + value
        else:
            value = "00"
        
        timeval.append(value)
        
        # convert each time component to seconds
        if c == "h":
            factor = 3600
        elif c == "m":
            factor = 60
        else:
            factor = 1
            
        totalseconds = totalseconds + (factor * int(value))
        
    return(":".join(timeval),totalseconds)


# ==========================================================
# function: updateattendance
# description: update attendance tracker for each participant
# ===========================================================
def updateattendance(src,dest,processed):
 try:
    
    # leave cutoff values
    fdp = st.session_state["fdp"]
    hdp = st.session_state["hdp"]
    absent = st.session_state["absent"]
    
    ctr = 1
    
    mybar = st.progress(ctr,"Attendance update in progress ...")
    time.sleep(2)
    
    # update the destination file with the daily attendance status for each participant
    df_out = pd.read_csv(dest)
    
    ctr+=1
    mybar.progress(ctr,"Formatting output data ...")
    time.sleep(0.5)
    ret,df_out = formatdestfile(df_out)
    if(ret==-1):
        return(ret,df_out)

    
    # process every file from the input directory
    allfiles = os.walk(src)
    for path,_,files in allfiles:
        for file in files:
            filename = path + file
            ctr+=10
            mybar.progress(ctr,"Processing input data. " + file)
        
            # extract the attendace details from the input file
            time.sleep(1)
            ret,df_in = getdata(filename)
            if(ret==-1):
                return(ret,df_in)
        
            # check if this file has been already processed and marked for attendance
            # if yes, stop, else proceed
            trg_date = df_in.firstjoin[0].split(",")[0]
            trg_date = datetime.date.strftime(datetime.datetime.strptime(trg_date,"%m/%d/%y").date(),"%d/%m/%Y")
        
            if trg_date in df_out.columns:
                errmsg = "WARNING: Attendance for the specified date '{}' has already been marked. Skipping file ...".format(trg_date)
                os.rename(filename,processed+file)
                mybar.progress(0,'Skipping file ...')
                st.write(errmsg)
                time.sleep(0.5)
                # return(-1,errmsg)
                continue
        
            ctr+=2
            mybar.progress(ctr,"Performing updates...")
            time.sleep(0.5)
    
            # actual training duration 
            act_dur = st.session_state["total_duration"]
        
            ctr+=1
            # add the new date column for which the attendance have to be marked for each participant
            df_out[trg_date] = ''
            mybar.progress(ctr,"Performing updates...")
            time.sleep(0.5)
    
            # for each participant, mark the daily attendace as P or A, based on the total hours attended for the day
            # the ID for each participant is the email
    
            # the output file will have all the mail IDs of registered learners
            # match the out.emailID with the in.emailID
            ctr+=1
            mybar.progress(ctr,"Performing updates...")
            time.sleep(0.5)
    
            emails = df_out.email.values
            act_dur = df_in.total_duration.unique()[0] # get it one time to calculate the attendance %
    
            for email in emails:
                email = email.strip()
        
                # get the duration from the daily attendance status sheet for each ID
                user_dur = df_in.duration[df_in.email == email].values
            
                if len(user_dur) > 0:
                    user_dur = user_dur[0]
                    _,user_dur = formattime(user_dur)
                    perc = user_dur / act_dur
                    
                    if (perc > fdp):
                        # 'training completed' and 'training attended' updated only for participants who are 'Present' 
                        df_out[trg_date][df_out.email == email] = "P"
                    elif ( (perc > hdp) and (perc < fdp) ):
                        df_out[trg_date][df_out.email == email] = "H"
                    elif (perc < absent):
                        df_out[trg_date][df_out.email == email] = "A"
                    else:
                        df_out[trg_date][df_out.email == email] = "UNK"
                else:
                    # if no participant records are found, mark as absent
                    df_out[trg_date][df_out.email == email] = "A"
    
            # common metrics applicable to all participants
            df_out.trg_compl = df_out.trg_compl+1   # training completed
            df_out.trg_attended = df_out.trg_attended+1 # training attended
            df_out.trg_conducted+=1 # training conducted
            df_out.rem_days = df_out.planned_training - df_out.trg_compl # remaining days
            df_out.attendance = round(df_out.trg_attended / df_out.trg_conducted,2) * 100 # attendance %
            
            ctr+=1
            mybar.progress(ctr,"Finished Processing input data. " + file)
            
            # after the input file is processed and updated, move it to the 'Processed' folder
            os.rename(filename,processed+file)
            mybar.empty()
    
    # update the destination attendance file with the day's attendance details
    time.sleep(0.5)
    mybar.progress(90,"Writing output ...")
    df_out.to_csv(dest,index=False)
    time.sleep(0.5)
    mybar.progress(100,"Job complete...")
    
    return(1,'Successfully processed attendance data')

 except Exception as e:
     return(-1,e)


# =====================
# function: getreport()
# =====================
def getreport(data,reptype,cols,names=None,status=None):
    
    if (reptype=="daywise"):
        df1 = pd.DataFrame({'Day':[],'P':[],'H':[],'A':[], 'Total participants':[]})
        
        for c in cols:
            P = len(data[data[c] == "P"])
            H = len(data[data[c] == "H"])
            A = len(data[data[c] == "A"])
            
            df2 = pd.DataFrame({'Day':[c],'P':[P],'H':[H],'A':[A], 'Total participants':[P+H+A]})
            df1 = pd.concat([df1,df2])
        
        df1 = df1.reset_index(drop=True)
        df1[['P','H','A','Total participants']] = df1[['P','H','A','Total participants']].astype(int)

    elif (reptype == "namewise"):
        df1 = data[cols][data.fullname.isin(names)]
        
    return df1       
    
# ===================
# Function: reports()
# ===================
def reports():
    showconfig()
    data = pd.read_csv(st.session_state["destination"])
    
    c1,c2 = st.columns([0.2,0.8])
    # show = c1.checkbox("Display dataset")
    # if show:
    #     c2.dataframe(data)
    # else:
    #     c2.write()
    
    cols = data.columns
    reports = ["None","Day wise attendance", "Name & Date wise attendance"]
    opt = c2.radio("Click to view report",reports)
        
    # select only the date columns
    datecols = [c for c in cols if len(re.findall("\d+",c)) == 3]
    
    if opt == "Day wise attendance":
        report = getreport(reptype="daywise",data=data,cols=datecols)
        c2.write(report)
    elif opt == "Name & Date wise attendance":
        n1,n2,n3 = c2.columns(3)
        fullnames = data.fullname
        status = ["P","H","A"]
        
        names = n1.multiselect("Select names (blank for all names)",fullnames)
        dates = n2.multiselect("Select date(s) (blank for all dates)",datecols)
        # att_status = n3.multiselect("Select status (blank for all status)",status)
        namesbtn = n3.button(":dizzy:",help="Get Report")
        
        if namesbtn:
            if len(names) <= 0:
                # st.error("Select a name")
                # return(-1)
                names = fullnames
            
            if len(dates) > 0:
                datecols = dates
            
            # datecols.insert(0,"fullname")
            report = getreport(reptype="namewise",data=data,cols=["fullname"]+datecols,names=names)
            report[['P','H','A','Total training days']] = [0,0,0,0]
            for name in names:
                total = 0
                att_status = list(report[datecols][report.fullname == name].values[0])
                att_code = ['P','H','A']
                for ac in att_code: 
                    report[ac][report.fullname == name] = att_status.count(ac)
                    total+= att_status.count(ac)
                report['Total training days'][report.fullname == name] = total
           
            c2.write(report)
        

# ==============================================
# calling each function based on the click value
# ==============================================
# main menu settings
options=[":house:",":memo:",":lower_left_fountain_pen:",":chart_with_upwards_trend:",":red_circle:"]
captions=['Home','Configuration',"Attendance","Quick Report","Close Application"]
nav = st.sidebar.radio("Select Option",options,captions=captions)
ndx = options.index(nav)

if (ndx==0):
    homepage()

if (ndx==1):
    configurepaths()
    
if (ndx==2):
    st.header("Attendace Tracker")
    st.divider()
    
    ret = 1
    
    showconfig()
    
    # check if the files and directories have been configured
    if st.session_state['source'] is None:
        st.error("ERROR: Select the source directory of your input data")
        ret = -1
    elif st.session_state['destination'] is None:
        st.error("ERROR: Select the destination file to update the daily attendance details")
        ret = -1
    elif st.session_state['processed'] is None:
        st.error("ERROR: Select a folder to move all processed input files")
        ret = -1

    # display a message to show number of files currently in the input directory
    src = st.session_state['source']
    files = os.walk(src)
    for path,_,file in files:
        files_count = len(file)
        st.success("There is/are currently {" + str(files_count) + "} files for processing")

    if ret == 1:
        c1,c2,c3 = st.columns(3)
        
        btn_c1 = c1.button(":white_check_mark:",help="Mark attendance")
        # btn_c2 = c2.button(":smiley:",help="View / Hide Attendance data")
        # btn_c3 = c3.button(":sleeping:",help="Close Attendance data")
        
        if (btn_c1):
            try:
                if files_count > 0:
                    ret,data = updateattendance(st.session_state['source'],st.session_state['destination'], st.session_state['processed'])
                    if (ret==1):
                        st.success(data)
                    elif (ret==-1):
                        st.error(data)
            except Exception as e:
                st.error(e)
                
        # btn = c2.button("View Attendance data")
        # if (btn_c2):
        #     if st.session_state["viewattendance"]%2==0:
        #         att_data = pd.read_csv(st.session_state['destination'])
        #         st.divider()
        #         st.subheader("Participant attendance details as on today")
        #         st.dataframe(att_data)
        #     else:
        #         st.write()
        #     st.session_state["viewattendance"]+=1

if (ndx==3):
    st.header("Quick Reports")
    reports()
    
if (ndx==4):
    st.header("Close Application")
    st.divider()
    st.subheader("Are you sure you want to terminate this session ?")
    st.write("\n")
    c1,c2 = st.columns(2)
    btn_close = c1.button(":eject:",help="Close Application")
    btn_cancel = c2.button(":black_right_pointing_triangle_with_double_vertical_bar:",help="Cancel")
    
    if btn_close:    
        with (st.spinner("Closing application ...")):
            time.sleep(3)
                
            import keyboard,psutil
            
            keyboard.press_and_release('ctrl+w')
            pid = os.getpid()
            p = psutil.Process(pid)
            p.terminate()
