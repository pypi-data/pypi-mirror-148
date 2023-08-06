import os
import mysql.connector
import logging
from robot.api import ExecutionResult, ResultVisitor
import datetime
from datetime import timedelta

def rfhistoric_reparser(opts):

    if opts.ignoreresult == "True":
        print("Ignoring execution results...")
        return

    path = os.path.abspath(os.path.expanduser(opts.path))

    # output.xml files
    output_names = []
    # support "*.xml" of output files
    if ( opts.output == "*.xml" ):
        for item in os.listdir(path):
            if os.path.isfile(item) and item.endswith('.xml'):
                output_names.append(item)
    else:
        for curr_name in opts.output.split(","):
            curr_path = os.path.join(path, curr_name)
            output_names.append(curr_path)

    required_files = list(output_names)
    missing_files = [filename for filename in required_files if not os.path.exists(filename)]
    if missing_files:
        # We have files missing.
        exit("output.xml file is missing: {}".format(", ".join(missing_files)))

    # Read output.xml file
    result = ExecutionResult(*output_names)
    result.configure(stat_config={'suite_stat_level': 2,
                                  'tag_stat_combine': 'tagANDanother'})

    print("Capturing execution results, This may take few minutes...")

    # connect to database
    # mydb = connect_to_mysql_db(opts.host, opts.username, opts.password, opts.projectname)
    rootdb = connect_to_mysql_db(opts.host, opts.username, opts.password, 'rfarchive')

    # get latest execution id
    if opts.executionid == "latest":
        result_id = get_latest_execution_id(rootdb, opts.projectid)
    else:
        result_id = opts.executionid

    print("INFO: Updating test results")
    result.visit(TestMetrics(rootdb, result_id, opts.fullsuitename))
    print("INFO: Updating execution table")
    update_execution_table(rootdb, result_id, opts.projectid)
    print("INFO: Updating execution results")
    commit_and_close_db(rootdb)

class TestMetrics(ResultVisitor):

    def __init__(self, db, id, full_suite_name):
        self.db = db
        self.id = id
        self.full_suite_name = full_suite_name

    def visit_test(self, test):
        if self.full_suite_name == "True":
            full_suite_name = test.longname.split("." + test.name)
            name = str(full_suite_name[0]) + " - " + str(test)
        else:
            name = str(test.parent) + " - " + str(test)

        time = float("{0:.2f}".format(test.elapsedtime / float(60000)))
        error = str(test.message)
        update_test_table(self.db, self.id, str(name), str(test.status), time, error)

def get_time_in_min(time_str):
    h, m, s = time_str.split(':')
    ctime = int(h) * 3600 + int(m) * 60 + int(s)
    crtime = float("{0:.2f}".format(ctime/60))
    return crtime

def connect_to_mysql_db(host, user, pwd, db):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception as e:
        print(e)
    
def get_latest_execution_id(con, pid):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT eid FROM rfarchive.hsexecution WHERE pid=%s ORDER BY eid DESC LIMIT 1;" % (pid))
    rows = cursorObj.fetchone()
    return rows[0]

def update_execution_table(con, eid, pid):
    cursorObj = con.cursor()
    # get pass, fail, skip test cases count by eid
    cursorObj.execute("SELECT COUNT(*) FROM rfarchive.hstest WHERE eid=%s AND status='PASS';" % (eid))
    execution_rows = cursorObj.fetchone()
    tests_passed = execution_rows[0]

    cursorObj.execute("SELECT COUNT(*) FROM rfarchive.hstest WHERE eid=%s AND status='FAIL';" % (eid))
    execution_rows = cursorObj.fetchone()
    tests_failed = execution_rows[0]

    cursorObj.execute("SELECT COUNT(*) FROM rfarchive.hstest WHERE eid=%s AND status='SKIP';" % (eid))
    execution_rows = cursorObj.fetchone()
    tests_skipped = execution_rows[0]

    tests_total = tests_passed + tests_failed + tests_skipped

    sql = "UPDATE rfarchive.hsexecution SET total=%s, pass=%s, fail=%s, skip=%s WHERE eid=%s;" % (tests_total, tests_passed, tests_failed, tests_skipped, eid)
    cursorObj.execute(sql)
    con.commit()

    cursorObj.execute("SELECT eid, pass, total FROM rfarchive.hsexecution WHERE eid=%s;" % (eid))
    rows = cursorObj.fetchone()
    # update rfarchive.TB_PROJECT table
    cursorObj.execute("UPDATE rfarchive.hsproject SET updated = now(), total = %s, percentage =%s WHERE pid='%s';" % (rows[2], float("{0:.2f}".format((rows[1]/rows[2]*100))), pid))
    con.commit()
    return str(rows[0])

def update_test_table(con, eid, test, status, duration, msg):
    cursorObj = con.cursor()
    sql = """UPDATE rfarchive.hstest SET status='%s', time='%s' WHERE name="%s" AND eid=%s""" % (str(status), str(duration), str(test), eid)
    cursorObj.execute(sql)

def commit_and_close_db(db):
    db.commit()