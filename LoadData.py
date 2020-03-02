class Movie:
    '''Movie Object, contains ID, Name, Year, Genre-Vector and List, a rating if used in an User Object, and a List of users who watched that movie'''
    def __init__(self, ID, name, year, genre, rating=0):
        '''Constructor'''
        self.__ID = ID #Movie ID
        self.__name = self.__adjustMovieName(name) #Movie Name, also removes the Year and puts the THE in front of the Name
        self.__year = year #Year of the Movie
        self.__genre = genre #The 0 and 1 List from the input file
        self.__rating = int(rating) #A variable for the rating, in userList it is used for that users rating, in movie list for its average rating
        self.__genreNameList = self.__movieGenreDataToNames(genre) #List of the names of the movie genres, used for Jaccard and makes it easier to display
        self.__usersWatched = list() #Empty list that is filled with the users who watched that movie later on
        
        
    def __str__(self):
        '''To String function: Print the useful information of the movie object'''
        return self.__ID + ", " + self.__name + ", " + self.__year + ", " + " ".join(self.__genreNameList) + ", " + str(self.__rating)
    
    def getID(self):
        '''Returns that movies ID'''
        return self.__ID
    
    def getName(self):
        '''Returns that movies Name'''
        return self.__name
    
    def getYear(self):
        '''Returns the year that movie got released'''
        return self.__year
    
    def getGenreVector(self):
        '''Returns the 0 and 1 vector with the genre data'''
        return self.__genre
    
    def getGenreNameList(self):
        '''Returns the list of genre names of that movie'''
        return self.__genreNameList
    
    def getRating(self):
        '''Returns the rating-variable'''
        return self.__rating
    
    def setRating(self, rating):
        '''Set the rating variable'''
        self.__rating = rating
    
    def getUsersWatched(self):
        '''Returns a list of users who watched that movie, with the rating they gave that movie'''
        return self.__usersWatched
    
    def addUsersWatched(self, userID, rating):
        '''Add a user to the list of users who watched that movie, the rating of that user is used to calculate the average rating'''
        self.__usersWatched.append((userID, rating))

    def calculateAverageRating(self):
        '''Calculate the Average Rating for that movie, depending on the ratings from the UsersWatched list'''
        avgRating = 0 #rating variable
        userList = self.getUsersWatched() #get the list of users who watched that movie with ratings
        if  not len(userList) == 0: #Check if any user watched that movie
            for user in userList: #Go over all users
                avgRating += int(user[1]) #Add up all ratings
            avgRating /= len(userList) #Calculate the average
            self.__rating = avgRating #Save the average in the rating field
        else:
            self.__rating = 0 #If nobody rated the movie, 0 will be in the rating field
    
    
    def __movieGenreNumberToGenreName(self, num):
        '''Enter the position of the Genre in the GenreData Block of the item.data file and get the genre name'''
        switcher = { #Simple Switch Case
            0: "Action",
            1: "Adventure",
            2: "Animation",
            3: "Children's",
            4: "Comedy",
            5: "Crime",
            6: "Documentary",
            7: "Drama",
            8: "Fantasy",
            9: "Film-Noir",
            10: "Horror",
            11: "Musical",
            12: "Mystery",
            13: "Romance",
            14: "Sci-Fi",
            15: "Thriller",
            16: "War",
            17: "Western"
        }
        return switcher.get(num, "Invalid input: "+str(num))

    def __movieGenreDataToNames(self, genreData):
        '''Enter the genredata block of a movie from the item.data file and get a list of all its genres'''
        result = [] #Empty List for the result
        for i in range(len(genreData)): #Loop over all values
            if genreData[i] == 1: #If a value is one, add the genre name to the list
                result.append(self.__movieGenreNumberToGenreName(i))
        return result #Return the list

    def __adjustMovieName(self, movieName):
        '''Check if there is a ", The" at the end of the name and put it infront.'''
        if ", The" in movieName: #Check for The
            movieName = movieName[:-5] #Remove it
            movieName = "The "+movieName #Place it at the front
        return movieName #Return new movieName
    
class User:
    '''User Class, contains ID, and a movie list, with ratings'''
    def __init__(self, ID):
        '''Constructor'''
        self.__ID = ID #User ID
        self.__watchedMovies = list() #Empty list for all the movies that user has watched
        
    def __str__(self):
        '''To String: Print all the useful information of the User'''
        temp = ""
        for movie in self.__watchedMovies: #Add up the data of all the movies that user watched
            temp += str(movie) 
            temp += '\n'
        return self.__ID + '\n' +temp #Add the userID and return the string
    
    def addMovie(self, movie):
        '''Adds a movie to the watched movie list'''
        self.__watchedMovies.append(movie)
        
    def setWatchedMoviesList(self, movieList):
        '''Put a new list in the Watched Movie variable'''
        self.__watchedMovies = movieList
        
    def getID(self):
        '''Return the ID'''
        return self.__ID
    
    def getWatchedMovies(self):
        '''Return the list of watched movies'''
        return self.__watchedMovies
        
def loadMovies():
    '''Create a list of Movie objects containing all movies'''
    movieList = list() #Setup List containing all movies
    try:
        f = open(r"movies\u.item", 'r') #Open the movie dataset
    except:
        print('File "u.item" could not be found.')
        raise
    line = f.readline() #Read the first line
    while line: #Loop over all lines
        try:
            temp = line.split('|') #Split at Pipe
            mID = temp[0] #Get ID
            mName = (temp[1])[0:-7] #Remove year from title, and save name
            mYear = (temp[1])[-5:-1] # Save year
            mGenre = temp[-18:] #Save Genre Data
            mGenre[-1] = mGenre[-1].rstrip() #Remove the \n at the end
            mGenre = list(map(int, mGenre)) #Cast the strings to ints
            movieList.append(Movie(mID, mName, mYear, mGenre)) #Add a new Movie Object to the List
        except:
            continue #If there is a problem with the line, skip it
        line = f.readline() #Read the next line
        
    return movieList #Return the List

def loadUsers(movieList):
    f = None
    try:
        f = open(r"movies\u.data", 'r') #Open the user file
    except:
        print('File "u.data" could not be found.')
        raise
    
    line = f.readline() #Read the first line of the dataset

    userList = list() #List for all the user objects
    i = 1 #Debug variable
    while line: #Loop over all lines
        
        try:
            temp = line.split('\t') #Split the line at the tabs, this return an array => (userID, movieID, rating, timestamp)
            
            user = next((x for x in userList if x.getID() == temp[0]), None) #Check if the user ID is already in the list
            
            if user == None: #If not add a new user object, with that movie and rating to the list
                tempUser = User(temp[0])
                tempUser.addMovie((temp[1],temp[2]))
                userList.append(tempUser)
            else:
                user.addMovie((temp[1], temp[2])) #if it is already in the list, add that movie and rating to the users watched list            
        except:
            print("ERROR")
            continue #If the line is not in the correct format skip it
        
        #Debug Message, so I know if the program crashed or just loads
        if i%10000 == 0:
            print("Line:",i)
        i+=1
        
        line = f.readline() #Read the next line
    f.close() #Close the userdata file
    
    
    
    for user in userList: #Go through the user list and change the movie ID rating tuples to a list of movie objects
        movies = user.getWatchedMovies() #get the movie ids and ratings
        tempMovieList = list() #new list for the movie objects
        for movie in movies:
            m = next((x for x in movieList if x.getID() == movie[0]), None) #check if that movie is already in the list
            if not m == None: #If not add it and set the rating correctly
                newMovie = Movie(m.getID(), m.getName(), m.getYear(), m.getGenreVector(), movie[1]) #Create a new movie object with the checked movies data
                tempMovieList.append(newMovie)
        user.setWatchedMoviesList(tempMovieList) #set that users watched movies list to the newly created one
    userList.sort(key = lambda x: x.getID(), reverse = True)
    return userList #return the list of users

def loadUsersWatched(userList, movieList):
    '''Add the users who watched a movie to that movies list of users who watched it'''
    for user in userList: #Loop over all users
        tempList = user.getWatchedMovies() #Add the movies that user watched to a temporary list
        for movie in tempList: #Loop over that list
            movieList[int(movie.getID()) - 1].addUsersWatched(user.getID(),movie.getRating()) #Add that user and its rating to the list of users who watched that movie
    
def generateAverageRatings(movieList):
    '''Invoke the Calculate Average Rating function of all movie objects in the list'''
    for movie in movieList: #Loop over all movies
        movie.calculateAverageRating() #Invoke the function
    
def loadData():
    '''Load movie and user data'''
    movieList = loadMovies() #Generate the list of all movie objects
    print("Loading Movie List finished.")
    userList = loadUsers(movieList) #Generate the list of all user objects
    print("Loading User Data finished")
    loadUsersWatched(userList, movieList) #Generate the user list for all the movie objects in the movie list
    print("Loading Users Watched finished.")
    generateAverageRatings(movieList) #Calculate all the average Ratings
    print("Calculating Average Rating finished")
    return (userList, movieList) #Return the final lists of users and movies

