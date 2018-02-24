from rq import Queue
from worker import conn
from test_server import testFunc



q = Queue(connection=conn)
result = q.enqueue(testFunc, 3, 5)

print(result)