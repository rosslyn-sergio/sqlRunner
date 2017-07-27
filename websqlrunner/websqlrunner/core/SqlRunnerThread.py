
import threading


class SqlRunnerThread(threading.Thread):
    def __init__(self, thread_id, name, counter, sqlrunner, sql):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter
        self.sqlRunner = sqlrunner
        self.sql = sql
        self.context = None
        self.success_function = None

    @classmethod
    def from_sqlrunner(cls, sqlrunner, sql, thread_id, name, counter):
        return SqlRunnerThread(thread_id, name, counter, sqlrunner, sql)

    def run(self):
        print("Starting " + str(self))
        code,error = self.sqlRunner.run(self.sql)
        if not code:
            if self.success_function:
                self.success_function(self.context)
            print("Finished " + str(self))
        else:
            #an error occurred
            if self.failed_function:
                self.failed_function(self.context)
            print("Failed " + str(self) + " with error " + str(error))

    def __str__(self):
        return "thread id: {}, name: {}, counter: {}".format(self.thread_id,
        self.name, self.counter)
