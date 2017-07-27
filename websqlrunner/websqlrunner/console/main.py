import sys

from core.sqlRunner import *
from core.SqlRunnerThread import *


def main(conn_strings, sql_query, run_in_parallel=False):
    if not conn_strings:
        raise ValueError()
    if not isinstance(conn_strings, list):
        raise TypeError()
    if not len(conn_strings):
        raise ValueError()
    if not isinstance(run_in_parallel, bool):
        raise TypeError()
    if not sql_query:
        raise ValueError()
    if not isinstance(sql_query, str):
        raise TypeError()

    thread_count = 1
    threads = []
    for conn_string in conn_strings:
        sql_runner = SqlRunner.from_sql_server_connection_string(conn_string)
        if not run_in_parallel:
            sql_runner.run(sql_query)
        else:
            #spin a new thread
            runner_thread = SqlRunnerThread.from_sqlrunner(sql_runner, sql_query,
                                                           "thread-%d" % thread_count,
                                                           "thread-%d" % thread_count,
                                                           thread_count)
            threads.append(runner_thread)
            runner_thread.start()

    #wait for all the threads to complete
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 3:
        print("Not enough arguments")
    else:
        sql = args[0]
        run_in_parallel = args[1]
        conn_strings = args[2:]
        main(conn_strings, sql, run_in_parallel)
