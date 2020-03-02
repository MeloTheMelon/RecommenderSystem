import math #Math is mostly needed for the POW and SQRT function
from scipy.spatial import distance #Used for the similarity Functions
from scipy import stats

def compareUsers(user1, user2, simFunction=0):
    '''Compare how similar two users are, will return value between 0 and 1, SimFunction values: 
    0...Euclidean
    1...Cosine
    2...Pearson
    3...Jaccard
    4...Manhatten'''
    
    moviesUser1 = user1.getWatchedMovies() #Get movies for first user
    moviesUser2 = user2.getWatchedMovies() #Get movies for second user
    
    incommon1 = list() #List of ratings of incommon movies for user1
    incommon2 = list() #List of ratings of incommon movies for user2

    for movie in moviesUser1: #Loop over all movies the first user watched
        for movie2 in moviesUser2: #Loop over all movies the second user watched
            if movie.getID() == movie2.getID(): #If both users watched a movie, add the ratings to the lists
                incommon1.append(int(movie.getRating()))
                incommon2.append(int(movie2.getRating()))
                break #Break once a movie is in both and look for the next one, saves computation time
                
    
    if len(incommon1) == 0: #If the two users have nothing incommon, the similarity will always be 0
        return 0
    
    if simFunction == 0: #Choose between which similarity function is to be used
        sim = euclideanSimilarityScore(incommon1, incommon2) #Calculate Similarity
    elif simFunction == 1:
        sim = cosineSimilarityScore(incommon1, incommon2) #Calculate Similarity
    elif simFunction == 2:
        sim = pearsonSimilarityScore(incommon1, incommon2) #Calculate Similarity
    elif simFunction == 3:
        sim = jaccardSimilarityScore(incommon1, incommon2) #Calculate Similarity
    elif simFunction == 4:
        sim = manhattenSimilarityScore(incommon1, incommon2) #Calculate Similarity
    else:
        print("ERROR - SimilarityFunction Value unknown")
        return 0
    
    return sim #Return the result
    
def compareMoviesByGenre(movie1, movie2, simFunction = 0):
    '''Compare two movies by the similarity of their genres, will return a value between 0 and 1, SimFunction values: 
    0...Euclidean
    1...Cosine
    2...Pearson
    3...Jaccard
    4...Manhatten'''
    
    movieGenres1 = movie1.getGenreVector() #Get List of Genres of that movie
    movieGenres2 = movie2.getGenreVector() #Get List of Genres of that movie
    

    if simFunction == 0: #Selected the wanted similarity function
        sim = euclideanSimilarityScore(movieGenres1, movieGenres2) #Calculate Similarity
    elif simFunction == 1:
        sim = cosineSimilarityScore(movieGenres1, movieGenres2) #Calculate Similarity
    elif simFunction == 2:
        sim = pearsonSimilarityScore(movieGenres1, movieGenres2) #Calculate Similarity
    elif simFunction == 3:
        movieGenres1 = movie1.getGenreNameList() #Get List of Genre-Names of that movie
        movieGenres2 = movie2.getGenreNameList() #Get List of Genre-Names of that movie
        sim = jaccardSimilarityScore(movieGenres1, movieGenres2) #Calculate Similarity
    elif simFunction == 4:
        sim = manhattenSimilarityScore(movieGenres1, movieGenres2) #Calculate Similarity
    else:
        print("ERROR - SimilarityFunction Value unknown")
        return 0

    return sim #Return the result 
    
def compareMoviesByUsersWatched(movie1, movie2, simFunction = 0):
    '''Given the movieGenresWatchers dictonary and two movieNames, return two vectors over all userIDs that watched both movies, with a 1 if that user watched it the movie and a 0 if not
    SimFunction values: 
    0...Euclidean
    1...Cosine
    2...Pearson
    3...Jaccard
    4...Manhatten'''
    #Could have just made this function for one movie and use a vector over all userIDs, but that would take loads of memory and a lot of useless data.
    #These vectors are only used for the comparison between two movies, so all lines of users who didn't watch either one of the movies would be useless.
    #This way I get two vectors with the same length, only containing the users who watched at least one of the two movies.
    
    userList1 = [i[0] for i in movie1.getUsersWatched()] #Get the list of users who watched the first movie and remove the rating data
    userList2 = [i[0] for i in movie2.getUsersWatched()] #Get the list of users who watched the second movie and remove the rating data
    
    userVector1 = [] #Will contain 1 if the user watched movie1 and 0 if not
    userVector2 = [] #Will contain 1 if the user watched movie2 and 0 if not
    
    #For Jaccard just skip all that
    if not simFunction == 3:
        
        for i in range(len(userList1)): #Loop over all users in userList1
            userVector1.append(1) #Add a 1 to userVector1, obviously they watched the first movie, because they are in the list of the users who watched the first movie
            if userList1[i] in userList2: #If that userID is also in the list that watched the second movie
                userVector2.append(1) #Add a 1 to vector2 as well
            else:
                userVector2.append(0)#If they didn't watch the second movie, add a 0 to the second vector
        for i in range(len(userList2)): #Loop over all users who watched the second movie
            if not userList2[i] in userList1: #If they are not in the list of users who watched the first movie, we covered all the users who watched the first movie or both in the first loop
                userVector2.append(1) #Add a 1 to the second vector
                userVector1.append(0) #And aad a 0 to the first vector
                
    if simFunction == 0: #Choose between the similarity functions
        sim = euclideanSimilarityScore(userVector1, userVector2) #Calculate Similarity
    elif simFunction == 1:
        sim = cosineSimilarityScore(userVector1, userVector2) #Calculate Similarity
    elif simFunction == 2:
        sim = pearsonSimilarityScore(userVector1, userVector2) #Calculate Similarity
    elif simFunction == 3:
        sim = jaccardSimilarityScore(userList1, userList2) #Calculate Similarity
    elif simFunction == 4:
        sim = manhattenSimilarityScore(userVector1, userVector2) #Calculate Similarity
    else:
        print("ERROR - SimilarityFunction Value unknown")
        return 0            

    return sim #Return the result

def euclideanSimilarityScore(vector1, vector2):
    '''Given two vectors, calculate the euclidean similarity'''
    dis = distance.euclidean(vector1, vector2) #Calculate euclidean distance
    return 1/(1+dis) #Calculate the similarity and return the results

def cosineSimilarityScore(vector1, vector2):
    '''Given two vectors, calculate the cosine similarity'''
    dis = distance.cosine(vector1, vector2) #Calculate cosine distance
    sim = 1 - dis #Similarity = 1 - cosine distance
    if math.isnan(sim): #Check for nan
        return 0
    return sim #Return result

def pearsonSimilarityScore(vector1, vector2):
    '''Given two vectors (same length), calculate the pearson similarity'''
    sim = stats.pearsonr(vector1, vector2)[0] #Calculate distance
    if math.isnan(sim): #Check if it is nan
        return 0
    return 1-abs(sim) #return similarity

def jaccardSimilarityScore(vector1, vector2):
    '''Given two vectors (same length), calculate the jaccard similarity'''
    #Jaccard had errors from when used from the library, this implementation works, so I kept mine
    combined = list(dict.fromkeys(vector1 + vector2)) #Unique variables in both vectors
    unique = list(set(vector1) - set(vector2)) #Unique variables in vector1 that are not in vector2
    return len(unique)/len(combined) #Similarity
    
def manhattenSimilarityScore(vector1, vector2):
    '''Given two vectors (same length), calculate the manhatten similarity'''
    return 1/(1+distance.cityblock(vector1, vector2))

def similarMovies(targetMovie, movieList, recommendationAmount, simFunction = 0, compareMovieGenres = True):
    '''This will return a List of similar movies for the target movie
    SimFunction values: 
    0...Euclidean
    1...Cosine
    2...Pearson
    3...Jaccard
    4...Manhatten
    
    Compare Movie Genres = True ... Movies will be compared by their genres'''
    
    recList = list() #List for all the recommendation tuples (movie name, simScore, average rating)
    
    for movie in movieList: #Loop over all movies
        if not movie.getID() == targetMovie.getID(): #Skip the target
            simScore = 0 #Variable for the similarity score
            if compareMovieGenres: #Compare either by Genres or Users who watched that movie
                simScore = compareMoviesByGenre(targetMovie, movie, simFunction)
            else:
                simScore = compareMoviesByUsersWatched(targetMovie, movie, simFunction)
            recList.append((movie.getName(), simScore, movie.getRating())) #Add the tuple to the list
    recList.sort(key = lambda x: (x[1],int(x[2])), reverse = True) #Sort the final list
    return recList[:recommendationAmount] #Return the amount of asked for recommendations

def recommendMovies(targetUser, userList, movieList, recommendationAmount, simFunction = 0, compareMovieGenres = True, recommendUsers = False):
    '''This will return a List of Movie-Recommendations for the target User
    SimFunction values: 
    0...Euclidean
    1...Cosine
    2...Pearson
    3...Jaccard
    4...Manhatten
    
    Compare Movie Genres = True ... Movies will be compared by their genres
    Compare Movie Genres = False ... Movies will be compared by the users who watched and rated them
    recommendUsers = False ... Recommend Movies, if True it will return closest users'''
    
    
    userSimList = list() #List for tuples of userID and the similarity to the target user
    
    for user in userList: #Loop over all users
        if not user.getID() == targetUser.getID(): #Ignore the target user
            simScore = compareUsers(targetUser, user, simFunction) #Calculate the similarity between the users
            userSimList.append((user.getID(), simScore)) #Add the tuple to the list
            
    userSimList.sort(key = lambda x: x[1], reverse = True) #Sort the list by the similarity score
    moviesTarget = targetUser.getWatchedMovies() #Get the movies the target user watched
    recommendedMovieList = list() #List for all the recommended movies
    userList.sort(key = lambda x: int(x.getID())) #Sort the user list by ID, just makes it easier to find specific users
    
    if recommendUsers: #If it should recommend users
        return userSimList[:recommendationAmount] #Return the n most similar users
    
    for tup in userSimList: #Loop over all tuples
        movies = userList[int(tup[0])-1].getWatchedMovies() #Get the movies that user watched
        notSeen = movies #Variable for all the movies that user watched that the target user hasn't seen
        for movie in moviesTarget: #Loop over all movies the target has seen
            for otherMovie in movies: #Loop over all movies the user has seen
                if movie.getID() == otherMovie.getID(): #If a movie is in both remove it
                    movies.remove(otherMovie) #Remove the movie
                    break #Once removed, break out of that loop and look for the next movie
        for potMovie in notSeen: #Loop over all potential movies
            sim = 0 #Variable for the similarity
            if int(potMovie.getRating()) >= 4: #Ignore all movies the user rated lower than a 4, considering that those might fit, but are also just bad
                for seenMovie in moviesTarget: #Compare the movie to all movies the target has seen and calculate an average similarity
                    if compareMovieGenres: #Choose if to compare the by genre or users who watched it
                        sim += compareMoviesByGenre(seenMovie, potMovie, simFunction) #Calculate the similarity
                    else:
                        sim += compareMoviesByUsersWatched(movieList[int(seenMovie.getID())-1], movieList[int(potMovie.getID())-1], simFunction) #Calculate the similarity
                sim /= len(moviesTarget) #Calculate the average similarity score
                temp = [item for item in recommendedMovieList if item[0] == potMovie.getName()] #If the movie is already in the list of recommendations
                if len(temp) == 0:
                    recommendedMovieList.append((potMovie.getName(), sim, float(movieList[int(potMovie.getID())].getRating())))
        if len(recommendedMovieList) >= int(recommendationAmount) or len(recommendedMovieList) == len(movieList): #Once enough movies are in the recommendations, stop the loop
            break
    recommendedMovieList.sort(key = lambda x: (x[1], x[2]), reverse = True) #Sort the list by similarity and average rating
    return recommendedMovieList[:recommendationAmount] #Return the asked for amount of recommendations

def customSimilarity(targetUser, userList, movieList, recommendationAmount, recUsers = False):
    '''A recommendation function using a custom similarity, just curious how it will do'''
    
    #This works pretty much the same as the recommendation function, so I won't comment everything except the parts that are different
    
    moviesTarget = targetUser.getWatchedMovies() #Get movies for the target user
    
    userSimList = list()
    
    for user in userList:
        if not user.getID() == targetUser.getID():
            simScore = 0
            tempMovieList = user.getWatchedMovies()
            for movie in tempMovieList:
                tempMovie = next((x for x in moviesTarget if x.getID() == movie.getID()), None)
                if not tempMovie == None:
                    simScore += 1 - (float(abs(int(tempMovie.getRating()) - int(movie.getRating())))/4) #The similarity score depends just on the difference in ratings
            simScore /= len(moviesTarget) #If both rated it the same it is 1, and 0.25 difference for every rating they are different
            userSimList.append((user.getID(), simScore))
            
    userSimList.sort(key = lambda x: x[1], reverse = True)
    if recUsers:
        return userSimList[:recommendationAmount]
    recommendedMovieList = list()
    userList.sort(key = lambda x: int(x.getID()))
    
    for tup in userSimList: #Loop over all tuples
        movies = userList[int(tup[0])-1].getWatchedMovies() #Get the movies that user watched
        notSeen = movies #Variable for all the movies that user watched that the target user hasn't seen
        for movie in moviesTarget: #Loop over all movies the target has seen
            for otherMovie in movies: #Loop over all movies the user has seen
                if movie.getID() == otherMovie.getID(): #If a movie is in both remove it
                    movies.remove(otherMovie) #Remove the movie
                    break #Once removed, break out of that loop and look for the next movie
        for potMovie in notSeen: #Loop over all potential movies
            sim = 0 #Variable for the similarity
            if int(potMovie.getRating()) >= 4: #Ignore all movies the user rated lower than a 4, considering that those might fit, but are also just bad
                for seenMovie in moviesTarget: #Compare the movie to all movies the target has seen and calculate an average similarity
                    sim += compareMoviesByUsersWatched(movieList[int(seenMovie.getID())-1], movieList[int(potMovie.getID())-1], 2) #Calculate the similarity
                sim /= len(moviesTarget) #Calculate the average similarity score
                temp = [item for item in recommendedMovieList if item[0] == potMovie.getName()] #If the movie is already in the list of recommendations
                if len(temp) == 0:
                    recommendedMovieList.append((potMovie.getName(), sim, float(movieList[int(potMovie.getID())].getRating())))
        if len(recommendedMovieList) >= int(recommendationAmount) or len(recommendedMovieList) == len(movieList): #Once enough movies are in the recommendations, stop the loop
            break
    recommendedMovieList.sort(key = lambda x: (x[1], x[2]), reverse = True) #Sort the list by similarity and average rating
    return recommendedMovieList[:recommendationAmount] #Return the asked for amount of recommendations