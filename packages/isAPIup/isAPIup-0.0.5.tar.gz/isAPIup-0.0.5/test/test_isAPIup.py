import isAPIup

#This will create sqlite3 db on current path
obj=isAPIup.create("temp123")

#This will insert the url and other parameters
obj.insert("http://localhost:5000/test/a","GET",23,100)
obj.insert("http://localhost:5000/test/b","GET",23,100)
obj.insert("http://localhost:5000/test/c","GET",23,100)

tt=obj.start()


response=obj.execute()
print(response.text)
