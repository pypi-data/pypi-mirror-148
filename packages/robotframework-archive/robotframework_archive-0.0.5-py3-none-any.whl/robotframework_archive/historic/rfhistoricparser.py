import os
import mysql.connector
import logging
from robot.api import ExecutionResult, ResultVisitor
import datetime
from datetime import timedelta

def rfhistoric_parser(opts):

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
    rootdb = connect_to_mysql_db(opts.host, opts.username, opts.password, 'rfarchive')

    stats = result.statistics
    try:
        stats_obj = stats.total.all
    except:
        stats_obj = stats.total
    total = stats_obj.total
    passed = stats_obj.passed
    failed = stats_obj.failed
    try:
        skipped = stats_obj.skipped
    except:
        skipped = 0

    elapsedtime = datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=result.suite.elapsedtime)
    elapsedtime = get_time_in_min(elapsedtime.strftime("%X"))
    elapsedtime = float("{0:.2f}".format(elapsedtime))

    # insert test results info into db
    result_id = insert_into_execution_table(rootdb, opts.projectid, opts.executionname, total, passed, failed, skipped, elapsedtime)
    print("INFO: Capturing test results")
    result.visit(TestMetrics(rootdb, result_id, opts.projectid, opts.fullsuitename))

    print("INFO: Writing execution results")
    commit_and_close_db(rootdb)

# other useful methods
class TestMetrics(ResultVisitor):

    def __init__(self, db, id, pid, full_suite_name):
        self.db = db
        self.id = id
        self.pid = pid
        self.full_suite_name = full_suite_name

    def visit_test(self, test):
        if self.full_suite_name == "True":
            full_suite_name = test.longname.split("." + test.name)
            name = str(full_suite_name[0]) + " - " + str(test)
        else:
            name = str(test.parent) + " - " + str(test)

        time = float("{0:.2f}".format(test.elapsedtime / float(60000)))
        error = str(test.message)
        insert_into_test_table(self.db, self.id, self.pid, str(name), str(test.status), time, error, str(test.tags))

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

def insert_into_execution_table(ocon, pid, description, total, passed, failed, skipped, etime):
    rootCursorObj = ocon.cursor()
    sql = "INSERT INTO rfarchive.hsexecution (eid, pid, description, time, total, pass, fail, skip, etime) VALUES (%s, %s, %s, now(), %s, %s, %s, %s, %s);"
    val = (0, pid, description, total, passed, failed, skipped, etime)
    rootCursorObj.execute(sql, val)
    ocon.commit()

    rootCursorObj.execute("SELECT eid, pass, total FROM rfarchive.hsexecution ORDER BY eid DESC LIMIT 1;")
    rows = rootCursorObj.fetchone()

    # update rfarchive.TB_PROJECT table
    rootCursorObj.execute("UPDATE rfarchive.hsproject SET updated = now(), total = %s, percentage =%s WHERE pid='%s';" % (rows[2], float("{0:.2f}".format((rows[1]/rows[2]*100))), pid))
    ocon.commit()
    return str(rows[0])

def insert_into_test_table(con, eid, pid, test, status, duration, msg, tags):
    cursorObj = con.cursor()
    sql = "INSERT INTO rfarchive.hstest (tid, eid, pid, name, status, time, error, tag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (0, eid, pid, test, status, duration, msg, tags)
    cursorObj.execute(sql, val)

def commit_and_close_db(db):
    db.commit()