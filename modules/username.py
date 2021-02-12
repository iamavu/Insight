#Username
class userFetcher:
    user = ""
    def getUser():
        global user
        return user
        
    def setUser():
        global user
        user = input("Enter username: ")
        print("\n")