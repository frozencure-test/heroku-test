from rq import Queue
from worker import conn
from test_server import testFunc



q = Queue(connection=conn)
job = q.enqueue(testFunc, 'hello world')

print(job.result)