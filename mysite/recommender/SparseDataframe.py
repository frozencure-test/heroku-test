from scipy import sparse
import pandas as pd
import sklearn.preprocessing as pp
import numpy as np
class SparseDataframe:

    """
    Class that handles the conversion and analysis of a data-set which contains user votes
    that are related to specific items. The data-set will be mapped as a pandas dataframe,
    which will be then converted in a sparse matrix, for more efficient memory management.
    attributes:
        dataframe: pandas dataframe from wich sparse matrix will be built.
        columns: list of the headers of the dataframe -> 1: Items, 2: Users, 3: Votes
                A row of the df contains: A vote an user casted on a item.
        uniqueUsers: list of all unique users, should be first column
        uniqueItems: list of all unique items
        itemVoteCounts: list of each item and how many votes it has
        csrMatrix: a sparse csr matrix that is built from the dataframe(check scipy.sparse)
    """
    def __init__(self, dataframe=None, greaterThan=0, csvPath=None):
        """Will create a filtered dataframe by removing low voted items"""
        if csvPath is not None:
            self.dataframe = pd.read_csv(csvPath, compression='gzip')
            self.dataframe['Votes'] = np.ones(shape=(len(self.dataframe.index)))
        if dataframe is not None:
            self.dataframe = dataframe
        self.columns = list(self.dataframe)
        counts = self.dataframe.dropna(axis=0, how='any')
        self.itemVoteCounts = counts[counts.columns[0]].value_counts()
        self.removeLowVotes(greaterThan)
        """Will populate the csr matrix and itemVoteCounts attributes"""
        self.uniqueUsers = self.__setUniqueUsers()
        self.uniqueItems = self.__setUniqueItems()
        self.csrMatrix = self.__setSparseMatrix()


    def __setUniqueUsers(self):
        un_users = self.dataframe[self.dataframe.columns[1]].unique().tolist()
        un_users.sort()
        return un_users

    def __setUniqueItems(self):
        un_items = self.dataframe[self.dataframe.columns[0]].unique().tolist()
        un_items.sort()
        return un_items

    def __getDataAsList(self):
        data = self.dataframe[self.dataframe.columns[2]].tolist()
        return data

    def __setSparseMatrix(self):
        rows = self.dataframe[self.dataframe.columns[1]].astype(pd.api.types.CategoricalDtype(categories=self.uniqueUsers)).cat.codes
        columns = self.dataframe[self.dataframe.columns[0]].astype(pd.api.types.CategoricalDtype(categories=self.uniqueItems)).cat.codes
        data = self.__getDataAsList()
        csrMatrix = sparse.csc_matrix((data, (rows, columns)), shape=(len(self.uniqueUsers), len(self.uniqueItems)))
        return csrMatrix

    def getItemVoteCount(self, itemId):
        return self.itemVoteCounts[itemId]

    def getUserIdFromIndex(self, userIndex):
        return self.uniqueUsers[userIndex]

    def getItemIdFromIndex(self, itemIndex):
        return self.uniqueItems[itemIndex]

    def getUserIndexById(self, userId):
        return self.uniqueUsers.index(userId)

    def getItemIndexById(self, itemId):
        if itemId in self.uniqueItems:
            return self.uniqueItems.index(itemId)
        else:
            return False

    def __getItemsIndexByUser(self, userId):
        userIndex = self.getUserIndexById(userId)
        return self.csrMatrix.getrow(userIndex).nonzero()[1]

    def __getUsersIndexByItem(self, itemId):
        itemIndex = self.getItemIndexById(itemId)
        return self.csrMatrix.getcol(itemIndex).nonzero()[0]

    def getItemIdsByUser(self, userId):
        itemsIndexes = self.__getItemsIndexByUser(userId)
        itemsIds = []
        for index in itemsIndexes:
            itemsIds.append(self.getItemIdFromIndex(index))
        return itemsIds

    def getUserIdsByItem(self, itemId):
        userIndexes = self.__getUsersIndexByItem(itemId)
        userIds = []
        for index in userIndexes:
            userIds.append(self.getUserIdFromIndex(index))
        return userIds

    def removeLowVotes(self, smallerThan):
        filteredCounts = self.itemVoteCounts[self.itemVoteCounts > smallerThan]
        self.dataframe = self.dataframe[self.dataframe[self.dataframe.columns[0]].isin(filteredCounts.index.tolist())]

    def cosineSimilarities(self):
        col_normed_matrix = pp.normalize(self.csrMatrix)
        return col_normed_matrix.T * col_normed_matrix

    def getTopItems(self, top, postId, voteCountsUnder=float('inf')):
        if self.getItemIndexById(postId) == False:
            return False
        similarities = self.cosineSimilarities()[self.getItemIndexById(postId),:]
        similarities = similarities.toarray()
        indexSim = None
        idSim = []
        for arr in similarities:
            ind = np.argpartition(arr, -top-20)[-top-20:]
            indexSim = [(i, arr[i]) for i in ind]
        indexSim = [value for  value in indexSim if value[0] != self.getItemIndexById(postId)]
        for elem in indexSim:
            itemId = self.getItemIdFromIndex(elem[0])
            if itemId is not None and self.getItemVoteCount(itemId) > voteCountsUnder:
                indexSim.remove(elem)
        indexSim.sort(key=lambda x: x[1], reverse=True)
        for elem in indexSim[:top]:
            singleIdSim = []
            singleIdSim.append(self.getItemIdFromIndex(elem[0]))
            singleIdSim.append(elem[1])
            print(singleIdSim)
            idSim.append(singleIdSim)
        return idSim
