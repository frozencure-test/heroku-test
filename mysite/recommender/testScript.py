from mysite.recommender.SparseDataframe import SparseDataframe
from mysite.recommender.preprocessor import decompress
import numpy as np
import time


start1 = time.time()
path = decompress()
sparseDf = SparseDataframe(greaterThan=10, csvPath=path)
end1= time.time()
print(end1-start1)

start = time.time()
top = 10
postId = 4105331
print(sparseDf.getTopItemsCosineSim(postId, top))
# similaritiesContainer = sparseDf.getTopSingleItems(postId)
# similarities = similaritiesContainer[0]
# ind = np.argpartition(similarities, -top-1)[-top-1:]
# indexSim = [(i, similarities[i]) for i in ind]
# indexSim = [value for  value in indexSim if value[0] != sparseDf.getItemIndexById(postId)]
# indexSim.sort(key=lambda x: x[1], reverse=True)
# idSim = []
# for elem in indexSim:
#     singleIdSim = []
#     singleIdSim.append(sparseDf.getItemIdFromIndex(elem[0]))
#     singleIdSim.append(elem[1])
#     #print(singleIdSim)
#     idSim.append(singleIdSim)
# print(idSim)


# print(similarities)
# topTen = topTenContainer[0]
# topTen = topTen[-10:]
# for (i, index) in enumerate(topTen):
#       print('%s ' % (sparseDf.getItemIdFromIndex(index)))
# # print(len(topTenContainer.T[0]))
# # print(len(sparseDf.uniqueItems))
# end = time.time()
# print(end-start)
