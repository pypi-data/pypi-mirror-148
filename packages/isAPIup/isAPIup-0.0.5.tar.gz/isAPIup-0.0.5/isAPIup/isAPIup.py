import requests
import json
import datetime
import re
import sqlite3



class create:    
    def __init__(self, filename):
        self.filename = filename

        url_db = sqlite3.connect(filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        url_db.execute('''CREATE TABLE IF NOT EXISTS connection_table
                 (id INTEGER NOT NULL PRIMARY KEY,
                 url TEXT NOT NULL,
                 method TEXT DEFAULT GET,
                 headers TEXT DEFAULT NULL,
                 payload TEXT DEFAULT NULL,
                 datetime timestamp NOT NULL,
                 working_response_length TEXT,
                 max_retry INTEGER DEFAULT 10);''')
        print(True)
        
    #insert("http://localhost:5000/test/a","GET",23,100)
    #insert("http://localhost:5000/test/a","GET",23,100,{},{})

    def insert(self,url:str,method:str,working_response_length:int,max_retry:int,headers=None,payload=None):
            url_db = sqlite3.connect(self.filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

            chk_url=url_db.execute("SELECT * FROM connection_table where url='"+url+"'").fetchall()
            if chk_url==[]:

                regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

                url_check=re.match(regex, url) is not None
                if url_check==False:
                        print("Please Enter Valid URL")
                        return False

                if method.upper()!="GET" and method.upper()!="POST":
                        print(method)
                        print("Invalid Method Input")
                        return False

                try:
                        if headers!=None:
                                headers=json.loads(str(headers))
                except:
                        print("Please Input Headers as Json")
                        return False

                try:
                        if payload!=None:
                                payload=json.loads(str(payload))
                except:
                        print("Please Input Payload as Json")
                        return False

                if str(working_response_length).isdigit==False or working_response_length==0:
                        print("Please Input Positive Integer")
                        return False

                if str(max_retry).isdigit==False or max_retry==0:
                        print("Please Input Positive Integer")
                        return False

                url_db.execute("INSERT INTO connection_table(url, method, headers, payload, datetime, working_response_length, max_retry) values(?,?,?,?,?,?,?)" ,(url, method.upper(), str(headers), str(payload),datetime.datetime.now(),working_response_length,max_retry))
                url_db.commit()

                return True
            else:
                print("URL Already Present!!!")
                return False



    def append_new_data(self,url,method,headers,payload,working,current_response_length,working_response_length,max_retry,total_retry=0):
            url_db = sqlite3.connect(self.filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

            temp_url_check=url_db.execute("SELECT * FROM session_table where url='"+url+"'").fetchall()
            if temp_url_check==[]:       
                    url_db.execute("INSERT INTO session_table(url, method, headers, payload, datetime, working, current_response_length, working_response_length,max_retry) values(?,?,?,?,?,?,?,?,?)" ,(url, method, str(headers), str(payload), datetime.datetime.now(), str(working),current_response_length,working_response_length,max_retry))
                    url_db.commit()
                    return True
            else:
                    url_db.execute("UPDATE session_table SET total_retry="+str(total_retry)+", working='"+str(working)+"', current_response_length='"+str(current_response_length)+"', working_response_length='"+str(working_response_length)+"' where url = '"+url+"'")
                    url_db.commit()
                    return True



    def start(self,postfix_url=None,show_logs=False):
            url_db = sqlite3.connect(self.filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

            url_db.execute("DROP TABLE IF EXISTS session_table;")
            url_db.commit()

            url_db.execute('''CREATE TABLE IF NOT EXISTS session_table
                     (id INTEGER NOT NULL PRIMARY KEY,
                     url TEXT NOT NULL,
                     method TEXT DEFAULT GET,
                     headers TEXT DEFAULT NULL,
                     payload TEXT DEFAULT NULL,
                     datetime timestamp NOT NULL,
                     working TEXT,
                     current_response_length TEXT,
                     working_response_length TEXT,
                     max_retry INTEGER DEFAULT 10,
                     total_retry INTEGER DEFAULT 0);''')
            url_db.commit()


            url_data=url_db.execute("SELECT * FROM connection_table").fetchall()
            if url_data==[]:
                    print("No Data Found")
                    exit()


            flag=0                
            for i in url_data:
                    url=i[1]
                    method=i[2]
                    headers=i[3]
                    payload=i[4]
                    working_response_length=i[6]
                    max_retry=i[7]

                    if headers==None or str(headers)=="{}" or str(headers)=="None":
                            headers={}
                    else:
                            headers=json.dumps(headers)
                    if payload==None or str(headers)=="{}" or str(headers)=="None":
                            payload={}
                    else:
                            payload=json.dumps(payload)


                    if postfix_url!=None:
                            url=url+"/"+postfix_url

                    response=requests.request(method,url=url,headers=headers,data=payload)
                    if show_logs==True:
                        print("running for ",url)

                    working=False
                    current_response_length=len(response.text)
                    if current_response_length >= int(working_response_length):
                            working=True
                            flag=flag+1
                    
                    self.append_new_data(url,method,headers,payload,working,current_response_length,working_response_length,max_retry,total_retry=0)

            if flag==0:
                    print('No URL is working Now!!!')
                    return False
            elif flag>=1:
                    print("Total Working: ",flag)
                    return flag





    def execute(self,postfix_url=None,show_logs=True):
            url_db = sqlite3.connect(self.filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

            check_session_table=url_db.execute("SELECT name FROM sqlite_master WHERE name='session_table'").fetchall()
            if check_session_table==[]:
                print('Session is empty!!, Please call start method')
                return False

            url_data=url_db.execute("SELECT * FROM session_table where working='True'").fetchall()
            if url_data==[]:
                    print('No URL is working Now!!!\nScanning from Begining...')
                    status=self.start()
                    if status==False:
                            return False
                            
            flag=0                        
            for i in url_data:
                    url=i[1]
                    method=i[2]
                    headers=i[3]
                    payload=i[4]
                    working_response_length=i[8]
                    max_retry=i[9]
                    total_retry=i[10]

                    if total_retry>=max_retry:
                            print("Max Calling Limit Reached for ",url)
                            continue

                    if headers==None or str(headers)=="{}" or str(headers)=="None":
                            headers={}
                    else:
                            headers=json.dumps(headers)
                    if payload==None or str(headers)=="{}" or str(headers)=="None":
                            payload={}
                    else:
                            payload=json.dumps(payload)

                    if postfix_url!=None:
                            url=url+"/"+postfix_url
                            
                    response=requests.request(method,url=url,headers=headers,data=payload)
                
                    working=False
                    current_response_length=len(response.text)
                    if current_response_length >= int(working_response_length):
                            working=True
                            flag=flag+1
                            self.append_new_data(url,method,headers,payload,working,current_response_length,working_response_length,max_retry,total_retry)
                            if show_logs==True:
                                print("running for ",'url',url,'current_response_length',current_response_length,'working_response_length',working_response_length,'working',working,'total_retry',total_retry)
                            return response
                    else:
                            working=False
                            total_retry=total_retry+1
                            self.append_new_data(url,method,headers,payload,working,current_response_length,working_response_length,max_retry,total_retry)
                            if show_logs==True:
                                print("running for ",'url',url,'current_response_length',current_response_length,'working_response_length',working_response_length,'working',working,'total_retry',total_retry)
                    
            if flag==0:
                    print('No URL is working Now!!!\nScanning from Begining...')
                    status=self.start()
                    if status==False:
                            return False
                    return status
            elif flag>=1:
                    return True


    def deletefromconnection(self,url):
            url_db = sqlite3.connect(self.filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

            chk_url=url_db.execute("SELECT * FROM connection_table where url='"+url+"'").fetchall()
            if chk_url==[]:
                    print('Does Not Found the URL')
                    return False
            url_db.execute("Delete from connection_table where url='"+url+"'")
            url_db.commit()
            print(url+" Deleted")
            return True


    def deletefromsession(self,url):
            url_db = sqlite3.connect(self.filename+'_sqlite3'+'.db' , detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)

            chk_url=url_db.execute("SELECT * FROM session_table where url='"+url+"'").fetchall()
            if chk_url==[]:
                    print('Does Not Found the URL')
                    return False
            url_db.execute("Delete from session_table where url='"+url+"'")
            url_db.commit()
            print(url+" Deleted")
            return True

if __name__ == "__main__":
    pass
