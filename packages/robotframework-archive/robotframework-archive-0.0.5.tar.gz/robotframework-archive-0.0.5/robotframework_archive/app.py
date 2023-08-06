from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import config
from .args import parse_options

app = Flask (__name__,
            static_url_path='', 
            static_folder='templates',
            template_folder='templates')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/redirect')
def redirect_url():
    return render_template('redirect.html')

##### Historic Report Start ####

@app.route('/hshome', methods=['GET', 'POST'])
def historic_home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM hsproject WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('hshome.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM hsproject;")
        data = cursor.fetchall()
        return render_template('hshome.html', data=data)

@app.route('/hsnew', methods=['GET', 'POST'])
def hs_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO rfarchive.hsproject ( pid, name, description, created, updated, total, percentage) VALUES (0, '%s', '%s', NOW(), NOW(), 0, 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('historic_home'))
    else:
        return render_template('hsnew.html')

@app.route('/<db>/hsdeldbconf', methods=['GET'])
def hs_delete_db_conf(db):
    return render_template('hsdeldbconf.html', db_name = db)

@app.route('/<db>/hsdelete', methods=['GET'])
def hs_delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM rfarchive.hsproject WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('historic_home'))

@app.route('/<db>/hsdashboardAll', methods=['GET'])
def hsdashboardAll(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.hsexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.hstest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from rfarchive.hsexecution WHERE pid=%s;" % db)
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT ROUND((pass/total)*100, 2) from rfarchive.hsexecution WHERE pid=%s;" % db)
        exe_perc_data = cursor.fetchall()

        results = []
        results.append(get_count_by_perc(exe_perc_data, 100, 90))
        results.append(get_count_by_perc(exe_perc_data, 89, 80))
        results.append(get_count_by_perc(exe_perc_data, 79, 70))
        results.append(get_count_by_perc(exe_perc_data, 69, 60))
        results.append(get_count_by_perc(exe_perc_data, 59, 0))

        return render_template('hsdashboardAll.html', exe_id_avg_data=exe_id_avg_data,
         results=results, results_data=results_data, db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/hsdashboardRecent', methods=['GET'])
def hsdashboardRecent(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, 'robothis')

    cursor.execute("SELECT COUNT(eid) from rfarchive.hsexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.hstest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 2;" % db)
        exe_info = cursor.fetchall()

        if len(exe_info) == 2:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])
    
        cursor.execute("SELECT pass, fail, total, etime, skip from rfarchive.hsexecution WHERE eid=%s" % exe_info[0][0])
        last_exe_data = cursor.fetchall()

        cursor.execute("SELECT pass, fail, total, etime, skip from rfarchive.hsexecution WHERE eid=%s" % exe_info[1][0])
        prev_exe_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND status = 'FAIL' AND comment IS NULL" % exe_info[0][0])
        req_anal_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(time),2) from rfarchive.hstest WHERE eid=%s;" % exe_info[0][0])
        test_avg_dur_data = cursor.fetchall()
    
        cursor.execute("SELECT COUNT(*) From (SELECT name, eid from rfarchive.hstest WHERE status='FAIL' AND pid=%s AND eid >= %s GROUP BY name HAVING COUNT(name) = 1) AS T WHERE eid=%s" % (db, exe_info[1][0],exe_info[0][0]))
        new_failed_tests_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND pid=%s AND type LIKE '%%Application%%';" % (exe_info[0][0], db))
        app_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND pid=%s AND type LIKE '%%Automation%%';" % (exe_info[0][0], db))
        auto_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND pid=%s AND type LIKE '%%Other%%';" % (exe_info[0][0], db))
        other_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND eid='%s' AND pid=%s GROUP BY assigned;" % (exe_info[0][0], db))
        fail_counts = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND comment IS NULL AND eid='%s' AND pid=%s GROUP BY assigned;" % (exe_info[0][0], db))
        fail_counts_analy = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND type NOT LIKE '%%Automation%%' AND eid='%s' AND pid=%s GROUP BY assigned;" % (exe_info[0][0], db))
        non_app_issues_analy = cursor.fetchall()

        # required analysis percentage
        if last_exe_data[0][1] > 0 and last_exe_data[0][1] != req_anal_data[0][0]:
            req_anal_perc_data = round( ((last_exe_data[0][1] - req_anal_data[0][0]) / last_exe_data[0][1])*100  ,2)
        else:
            req_anal_perc_data = 0
        
        new_tests_count = exe_info[0][1] - exe_info[1][1]
        passed_test_dif = last_exe_data[0][0] - prev_exe_data[0][0]
        failed_test_dif = prev_exe_data[0][1] - last_exe_data[0][1]
        skipped_test_dif = prev_exe_data[0][4] - last_exe_data[0][4]

        return render_template('hsdashboardRecent.html', last_exe_data=last_exe_data, exe_info=exe_info,
        prev_exe_data=prev_exe_data, new_failed_tests_count=new_failed_tests_count,
        req_anal_data=req_anal_data, app_failure_anl_count=app_failure_anl_count,
        req_anal_perc_data=req_anal_perc_data, auto_failure_anl_count=auto_failure_anl_count,
        new_tests_count=new_tests_count,other_failure_anl_count=other_failure_anl_count,
        passed_test_dif=passed_test_dif,fail_counts=fail_counts,fail_counts_analy=fail_counts_analy,
        failed_test_dif=failed_test_dif,non_app_issues_analy=non_app_issues_analy,
        skipped_test_dif=skipped_test_dif,
        test_avg_dur_data=test_avg_dur_data,
        db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/hsdashboard/<eid>', methods=['GET'])
def hseid_dashboard(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.hsexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.hstest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from rfarchive.hsexecution WHERE pid=%s AND eid <=%s order by eid desc LIMIT 2;" % (db, eid))
        exe_info = cursor.fetchall()

        if len(exe_info) == 2:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])

        cursor.execute("SELECT pass, fail, total, etime, skip from rfarchive.hsexecution WHERE eid=%s;" % exe_info[0][0])
        last_exe_data = cursor.fetchall()

        cursor.execute("SELECT pass, fail, total, etime, skip from rfarchive.hsexecution WHERE eid=%s;" % exe_info[1][0])
        prev_exe_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND status = 'FAIL' AND comment IS NULL;" % exe_info[0][0])
        req_anal_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(time),2) from rfarchive.hstest WHERE eid=%s;" % exe_info[0][0])
        test_avg_dur_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) From (SELECT name, eid From rfarchive.hstest WHERE status='FAIL' AND pid=%s AND eid >= %s GROUP BY name HAVING COUNT(name) = 1) AS T WHERE eid=%s" % (db, exe_info[1][0],exe_info[0][0]))
        new_failed_tests_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND pid=%s AND type LIKE '%%Application%%';" % (exe_info[0][0], db))
        app_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND pid=%s AND type LIKE '%%Automation%%';" % (exe_info[0][0], db))
        auto_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) from rfarchive.hstest WHERE eid=%s AND pid=%s AND type LIKE '%%Other%%';" % (exe_info[0][0], db))
        other_failure_anl_count = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND eid='%s AND pid=%s' GROUP BY assigned;" % (exe_info[0][0], db))
        fail_counts = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND comment IS NULL AND eid='%s' AND pid=%s GROUP BY assigned;" % (exe_info[0][0], db))
        fail_counts_analy = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND type NOT LIKE '%%Automation%%' AND eid='%s' AND pid=%s GROUP BY assigned;" % (exe_info[0][0], db))
        non_app_issues_analy = cursor.fetchall()
    
        # required analysis percentage
        if last_exe_data[0][1] > 0 and last_exe_data[0][1] != req_anal_data[0][0]:
            req_anal_perc_data = round( ((last_exe_data[0][1] - req_anal_data[0][0]) / last_exe_data[0][1])*100  ,2)
        else:
            req_anal_perc_data = 0
        
        new_tests_count = exe_info[0][1] - exe_info[1][1]
        passed_test_dif = last_exe_data[0][0] - prev_exe_data[0][0]
        failed_test_dif = prev_exe_data[0][1] - last_exe_data[0][1]
        skipped_test_dif = prev_exe_data[0][4] - last_exe_data[0][4]

        return render_template('hsdashboardByEid.html', last_exe_data=last_exe_data, exe_info=exe_info,
         prev_exe_data=prev_exe_data, new_failed_tests_count=new_failed_tests_count,
         req_anal_data=req_anal_data, app_failure_anl_count=app_failure_anl_count,
         req_anal_perc_data=req_anal_perc_data, auto_failure_anl_count=auto_failure_anl_count,
         new_tests_count=new_tests_count, other_failure_anl_count=other_failure_anl_count,
         passed_test_dif=passed_test_dif,fail_counts=fail_counts,fail_counts_analy=fail_counts_analy,
         failed_test_dif=failed_test_dif,non_app_issues_analy=non_app_issues_analy,
         skipped_test_dif=skipped_test_dif,
         test_avg_dur_data=test_avg_dur_data,
         db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/hsdashboardRecentFive', methods=['GET'])
def hsdashboardRecentFive(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.hsexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.hstest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 5;" % db)
        exe_info = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from rfarchive.hsexecution WHERE eid >= %s;" % exe_info[-1][0])
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT eid, pass, fail, etime, skip from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 5;" % db)
        exe_id_filter_data = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND eid>'%s' AND pid=%s GROUP BY assigned;" % (exe_info[-1][0], db))
        fail_counts = cursor.fetchall()

        cursor.execute("SELECT assigned, COUNT(*) from rfarchive.hstest WHERE status='FAIL' AND comment IS NULL AND eid>'%s' AND pid=%s GROUP BY assigned;" % (exe_info[-1][0], db))
        fail_counts_analy = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        return render_template('hsdashboardRecentFive.html', exe_id_avg_data=exe_id_avg_data,
         exe_id_filter_data=exe_id_filter_data, results_data=results_data,fail_counts=fail_counts,fail_counts_analy=fail_counts_analy,
         new_tests=new_tests,db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/hsdashboardRecentTen', methods=['GET'])
def hsdashboardRecentTen(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.hsexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.hstest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 10;" % db)
        exe_info = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from rfarchive.hsexecution WHERE pid=%s AND eid >= %s;" % (db, exe_info[-1][0]))
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT eid, pass, fail, etime, skip from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 10;" % db)
        exe_id_filter_data = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        return render_template('hsdashboardRecentTen.html', exe_id_avg_data=exe_id_avg_data,
         exe_id_filter_data=exe_id_filter_data, results_data=results_data,
         new_tests=new_tests, db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/hsdashboardRecentThirty', methods=['GET'])
def hsdashboardRecentThirty(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.hsexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.hstest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid, total from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 30;" % db)
        exe_info = cursor.fetchall()

        cursor.execute("SELECT ROUND(AVG(pass),0), ROUND(AVG(fail),0), ROUND(AVG(etime),2), ROUND(AVG(skip),0) from rfarchive.hsexecution WHERE pid=%s AND eid >= %s;" % (db, exe_info[-1][0]))
        exe_id_avg_data = cursor.fetchall()

        cursor.execute("SELECT eid, pass, fail, etime, skip from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 30;" % db)
        exe_id_filter_data = cursor.fetchall()

        # new tests
        new_tests = exe_info[0][1] - exe_info[-1][1]

        return render_template('hsdashboardRecentThirty.html', exe_id_avg_data=exe_id_avg_data,
         exe_id_filter_data=exe_id_filter_data, results_data=results_data,
         new_tests=new_tests, db_name=db)

    else:
        return redirect(url_for('redirect_url'))

@app.route('/<db>/hsehistoric', methods=['GET'])
def hsehistoric(db):
    cursor = mysql.connection.cursor()
    # # use_db(cursor, db)
    cursor.execute("SELECT * from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 500;" % db)
    data = cursor.fetchall()
    return render_template('hsehistoric.html', data=data, db_name=db)

@app.route('/<db>/hsdeleconf/<eid>', methods=['GET'])
def hsdelete_eid_conf(db, eid):
    return render_template('hsdeleconf.html', db_name = db, eid = eid)

@app.route('/<db>/hsedelete/<eid>', methods=['GET'])
def hsdelete_eid(db, eid):
    cursor = mysql.connection.cursor()
    # # use_db(cursor, db)
    # remove execution from tables: execution, suite, test
    cursor.execute("DELETE FROM rfarchive.hsexecution WHERE eid='%s';" % eid)
    cursor.execute("DELETE FROM rfarchive.hstest WHERE eid='%s';" % eid)
    # get latest execution info
    cursor.execute("SELECT pass, total from rfarchive.hsexecution WHERE pid=%s ORDER BY eid DESC LIMIT 1;" % db)
    data = cursor.fetchall()

    try:
        if data[0][0] > 0:
            recent_pass_perf = float("{0:.2f}".format((data[0][0]/data[0][1]*100)))
        else:
            recent_pass_perf = 0
    except:
        recent_pass_perf = 0

    # update rfarchive project
    cursor.execute("UPDATE rfarchive.hsproject SET total=%s, updated=now(), percentage=%s WHERE pid='%s';" % (int(data[0][1]), recent_pass_perf, db))
    # commit changes
    mysql.connection.commit()
    return redirect(url_for('hsehistoric', db = db))

@app.route('/<db>/hstmetrics', methods=['GET', 'POST'])
def hstmetrics(db):
    cursor = mysql.connection.cursor()
    # # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update rfarchive.hstest SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT eid from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 1;" % db)
    data = cursor.fetchone()
    print(data)
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.hstest WHERE eid={eid} and pid={pid};".format(eid=data[0], pid=db))
    data = cursor.fetchall()
    return render_template('hstmetrics.html', data=data, db_name=db)

@app.route('/<db>/hstmetrics/<eid>', methods=['GET', 'POST'])
def hseid_tmetrics(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update rfarchive.hstest SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.hstest WHERE eid=%s; and pid=%s" % (eid, db))
    data = cursor.fetchall()
    return render_template('hseidtmetrics.html', data=data, db_name=db)

@app.route('/<db>/hsfailures/<eid>', methods=['GET', 'POST'])
def hseid_failures(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update rfarchive.hstest SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.hstest WHERE pid=%s and eid=%s and status='FAIL';" % (db, eid))
    data = cursor.fetchall()
    return render_template('hsfailures.html', data=data, db_name=db)

@app.route('/<db>/hsfailures', methods=['GET', 'POST'])
def hsrecent_failures(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    if request.method == "POST":
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']
        rowid = request.form['rowid']
        cursor.execute('Update rfarchive.hstest SET comment=\'%s\', assigned=\'%s\', eta=\'%s\', review=\'%s\', type=\'%s\', updated=now() WHERE tid=%s;' % (str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(rowid)))
        mysql.connection.commit()

    # Get last row execution ID
    cursor.execute("SELECT eid from rfarchive.hsexecution order by eid desc LIMIT 1;")
    data = cursor.fetchone()
    cursor.execute("SELECT * from rfarchive.hstest WHERE eid=%s and status='FAIL';" % data)
    data = cursor.fetchall()
    return render_template('hsfailures.html', data=data, db_name=db)

@app.route('/<db>/hsttags/<eid>', methods=['GET', 'POST'])
def hseid_ttags(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT eid, name, status, tag from rfarchive.hstest WHERE eid=%s and pid=%s" % (eid, db))
    data = cursor.fetchall()
    return render_template('hsttags.html', data=data, db_name=db)

@app.route('/<db>/hssearch', methods=['GET', 'POST'])
def hssearch(db):
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        try:
            if search:
                cursor.execute("SELECT * from rfarchive.hstest WHERE (pid={pid}) and (name LIKE '%{name}%' OR status LIKE '%{name}%' OR eid LIKE '%{name}%') ORDER BY eid DESC LIMIT 500;".format(name=search, pid=db))
                data = cursor.fetchall()
                return render_template('hssearch.html', data=data, db_name=db, error_message="")
            else:
                return render_template('hssearch.html', db_name=db, error_message="Search text should not be empty")
        except Exception as e:
            print(str(e))
            return render_template('hssearch.html', db_name=db, error_message="Could not perform search. Avoid single quote in search or use escaping character")
    else:
        return render_template('hssearch.html', db_name=db, error_message="")

@app.route('/<db>/hsflaky', methods=['GET'])
def hsflaky(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT eid from ( SELECT eid from rfarchive.hsexecution ORDER BY eid DESC LIMIT 5 ) as tmp ORDER BY eid ASC LIMIT 1;")
    last_five = cursor.fetchall()
    cursor.execute("SELECT eid from rfarchive.hsexecution WHERE pid=%s ORDER BY eid DESC LIMIT 5;" % db)
    last_five_ids = cursor.fetchall()
    sql_query = "SELECT name, eid, status from rfarchive.hstest WHERE pid=%s and eid >= %s ORDER BY eid DESC;" % (db, str(last_five[0][0]))
    cursor.execute(sql_query)
    data = cursor.fetchall()
    # print("==== Before Sorted Data ===")
    # print(data)
    sorted_data = sort_tests(data)
    # print("==== After Sorted Data ===")
    # print(sorted_data)
    return render_template('hsflaky.html', data=sorted_data, db_name=db, builds=last_five_ids)

@app.route('/<db>/hscompare', methods=['GET', 'POST'])
def hscompare(db):
    if request.method == "POST":
        eid_one = request.form['eid_one']
        eid_two = request.form['eid_two']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        # fetch first eid tets results
        cursor.execute("SELECT name, eid, status, time, error from rfarchive.hstest WHERE eid=%s and pid=%s;" % (eid_one, db) )
        first_data = cursor.fetchall()
        # fetch second eid test results
        cursor.execute("SELECT name, eid, status, time, error from rfarchive.hstest WHERE eid=%s and pid=%s;" % (eid_two, db) )
        second_data = cursor.fetchall()
        if first_data and second_data:
            # combine both tuples
            data = first_data + second_data
            sorted_data = sort_tests(data)
            return render_template('hscompare.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data, eid_one = eid_one, eid_two = eid_two, error_message="")
        else:
            return render_template('hscompare.html', db_name=db, error_message="EID not found, try with existing EID")    
    else:
        return render_template('hscompare.html', db_name=db, error_message="")

@app.route('/<db>/hscomment', methods=['GET', 'POST'])
def hscomment(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT eid from rfarchive.hsexecution WHERE pid=%s order by eid desc LIMIT 1;" % db)
    recent_eid = cursor.fetchone()

    if request.method == "POST":
        error = request.form['error']
        eid = request.form['eid']
        issue_type = request.form['issue']
        review_by = request.form['reviewby']
        assign_to = request.form['assignto']
        eta = request.form['eta']
        comment = request.form['comment']

        try:
            cursor.execute('Update rfarchive.hstest SET comment=\'{}\', assigned=\'{}\', eta=\'{}\', review=\'{}\', type=\'{}\', updated=now() WHERE pid={} AND eid={} AND error LIKE \'%{}%\''.format(db, str(comment), str(assign_to), str(eta), str(review_by), str(issue_type), str(eid), str(error)))
            mysql.connection.commit()
            return render_template('hscomment.html', error_message="", recent_eid=recent_eid)
        except Exception as e:
            print(str(e))
            return render_template('hscomment.html', error_message=str(e), recent_eid=recent_eid)
    
    else:
        return render_template('hscomment.html', error_message="", recent_eid=recent_eid)

##### Historic Report End ####

####  Snow Report Start ####

@app.route('/sphome', methods=['GET', 'POST'])
def sp_historic_home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM spproject WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('sphome.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM spproject;")
        data = cursor.fetchall()
        return render_template('sphome.html', data=data)

@app.route('/spnew', methods=['GET', 'POST'])
def sp_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO rfarchive.spproject ( pid, name, description, created, updated, total) VALUES (0, '%s', '%s', NOW(), NOW(), 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('sp_historic_home'))
    else:
        return render_template('spnew.html')

@app.route('/<db>/spdeldbconf', methods=['GET'])
def sp_delete_db_conf(db):
    return render_template('spdeldbconf.html', db_name = db)

@app.route('/<db>/spdelete', methods=['GET'])
def sp_delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM rfarchive.spproject WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('sp_historic_home'))

@app.route('/<db>/spsearch', methods=['GET', 'POST'])
def spsearch(db):
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        try:
            if search:
                cursor.execute("SELECT * from rfarchive.sptest WHERE (pid={pid}) and (name LIKE '%{name}%' OR eid LIKE '%{name}%') ORDER BY eid DESC LIMIT 500;".format(name=search, pid=db))
                data = cursor.fetchall()
                return render_template('spsearch.html', data=data, db_name=db, error_message="")
            else:
                return render_template('spsearch.html', db_name=db, error_message="Search text should not be empty")
        except Exception as e:
            print(str(e))
            return render_template('spsearch.html', db_name=db, error_message="Could not perform search. Avoid single quote in search or use escaping character")
    else:
        return render_template('spsearch.html', db_name=db, error_message="")

@app.route('/<db>/spehistoric', methods=['GET'])
def spehistoric(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT * from rfarchive.spexecution WHERE pid=%s order by eid desc LIMIT 500;" % (db))
    data = cursor.fetchall()
    return render_template('spehistoric.html', data=data, db_name=db)

@app.route('/<db>/spdeleconf/<eid>', methods=['GET'])
def delete_eid_conf(db, eid):
    return render_template('spdeleconf.html', db_name = db, eid = eid)

@app.route('/<db>/spedelete/<eid>', methods=['GET'])
def spdelete_eid(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    # remove execution from tables: execution, suite, test
    cursor.execute("DELETE FROM rfarchive.spexecution WHERE eid='%s' AND pid='%s';" % (eid, db))
    cursor.execute("DELETE FROM rfarchive.sptest WHERE eid='%s' AND pid='%s';" % (eid, db))
    # get no. of executions
    cursor.execute("SELECT COUNT(*) from rfarchive.spexecution WHERE pid='%s';" % (db))
    exe_data = cursor.fetchall()

    # update sphistoric project
    cursor.execute("UPDATE rfarchive.spproject SET total=%s, updated=now() WHERE pid='%s';" % (int(exe_data[0][0]), db))
    # commit changes
    mysql.connection.commit()
    return redirect(url_for('spehistoric', db = db))

@app.route('/<db>/spmetrics/<eid>', methods=['GET'])
def spmetrics(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    # Get testcase results of execution id
    cursor.execute("SELECT * from rfarchive.sptest WHERE eid=%s;" % eid)
    test_data = cursor.fetchall()
    # get suite results of execution id
    cursor.execute("SELECT * from rfarchive.spexecution WHERE eid=%s;" % eid)
    exe_data = cursor.fetchall()
    return render_template('spmetrics.html', exe_data=exe_data, test_data=test_data)

@app.route('/<db>/spcmetrics', methods=['GET'])
def spcmetrics(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    eid_one = request.args.get('eid_one')
    eid_two = request.args.get('eid_two')
    # Get testcase results of execution id
    cursor.execute("SELECT * from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_one, db))
    test_data_1 = cursor.fetchall()
    cursor.execute("SELECT * from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_two, db))
    test_data_2 = cursor.fetchall()
    # get suite results of execution id
    cursor.execute("SELECT * from rfarchive.spexecution WHERE eid=%s;" % eid_one)
    exe_data_1 = cursor.fetchall()
    cursor.execute("SELECT * from rfarchive.spexecution WHERE eid=%s;" % eid_two)
    exe_data_2 = cursor.fetchall()
    return render_template('spcmetrics.html', exe_data_1=exe_data_1, exe_data_2=exe_data_2, test_data_1=test_data_1, test_data_2=test_data_2)

@app.route('/<db>/sptmetrics', methods=['GET', 'POST'])
def sptmetrics(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    # Get last row execution ID
    cursor.execute("SELECT eid from rfarchive.spexecution WHERE pid=%s order by eid desc LIMIT 1;" % db)
    data = cursor.fetchone()
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.sptest WHERE eid=%s;" % data)
    data = cursor.fetchall()
    return render_template('sptmetrics.html', data=data, db_name=db)

@app.route('/<db>/sptmetrics/<eid>', methods=['GET', 'POST'])
def eid_tmetrics(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid, db))
    data = cursor.fetchall()
    return render_template('speidtmetrics.html', data=data, db_name=db)

@app.route('/<db>/spcompare', methods=['GET', 'POST'])
def spcompare(db):
    if request.method == "POST":
        eid_one = request.form['eid_one']
        eid_two = request.form['eid_two']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        # fetch first eid tets results
        cursor.execute("SELECT name, eid, client_response_time, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_one, db) )
        first_data = cursor.fetchall()
        # fetch second eid test results
        cursor.execute("SELECT name, eid, client_response_time, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_two, db) )
        second_data = cursor.fetchall()
        if first_data and second_data:
            # combine both tuples
            data = first_data + second_data
            sorted_data = sort_tests(data)
            return render_template('spcompare.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data,
             eid_one = eid_one, eid_two = eid_two, error_message="", show_link=1)
        else:
            return render_template('spcompare.html', db_name=db, error_message="EID not found, try with existing EID", show_link=0)    
    else:
        return render_template('spcompare.html', db_name=db, error_message="", show_link=0)

@app.route('/<db>/spdashboardRecent', methods=['GET'])
def spdashboardRecent(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.spexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.sptest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid from rfarchive.spexecution WHERE pid=%s order by eid desc LIMIT 2;" % db)
        exe_info = cursor.fetchall()

        if len(exe_info) == 1:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])
        
        cursor.execute("SELECT * from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (exe_info[0][0], db))
        last_exe_data = cursor.fetchall()

        cursor.execute("SELECT name, client_response_time from rfarchive.sptest WHERE eid=%s AND pid=%s order by client_response_time desc LIMIT 5;" % (exe_info[0][0], db))
        crt_data = cursor.fetchall()

        cursor.execute("SELECT name, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s order by sql_time desc LIMIT 5;" % (exe_info[0][0], db))
        sqlt_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(name) from rfarchive.sptest WHERE eid=%s" % exe_info[0][0])
        tables_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(SUM(client_response_time),2) from rfarchive.sptest WHERE eid=%s" % exe_info[0][0])
        scrt_data = cursor.fetchall()

        cursor.execute("SELECT ROUND(SUM(sql_time),2) from rfarchive.sptest WHERE eid=%s" % exe_info[0][0])
        ssqlt_data = cursor.fetchall()

        cursor.execute("SELECT description, time from rfarchive.spexecution WHERE eid=%s;" % exe_info[0][0])
        desc_data = cursor.fetchall()
        app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

        return render_template('spdashboardRecent.html', last_exe_data=last_exe_data, exe_info=exe_info, db_name=db,
         crt_data=crt_data, tables_data=tables_data, sqlt_data=sqlt_data, scrt_data=scrt_data, ssqlt_data=ssqlt_data, app_version_data=app_version_data)    
    else:
        return redirect(url_for('redirect_url'))


@app.route('/<db>/spdashboardRecentTwo', methods=['GET', 'POST'])
def spdashboardRecentTwo(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT COUNT(eid) from rfarchive.spexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.sptest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        if request.method == "POST":
            eid_one = request.form['eid_one']
            eid_two = request.form['eid_two']
            # fetch first eid tets results
            cursor.execute("SELECT name, eid, client_response_time, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_one, db) )
            first_data = cursor.fetchall()
            # fetch second eid test results
            cursor.execute("SELECT name, eid, client_response_time, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_two, db) )
            second_data = cursor.fetchall()

            cursor.execute("SELECT description, time from rfarchive.spexecution WHERE eid=%s;" % eid_one)
            desc_data = cursor.fetchall()
            one_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            cursor.execute("SELECT description, time from rfarchive.spexecution WHERE eid=%s AND pid=%s;" % (eid_two, db))
            desc_data = cursor.fetchall()
            two_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            if first_data and second_data:
                # combine both tuples
                data = first_data + second_data
                sorted_data = sort_tests(data)
                # print(sorted_data)
                return render_template('spdashboardRecentTwo.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data,
                 eid_one = eid_one, eid_two = eid_two, one_app_version_data=one_app_version_data,
                  two_app_version_data=two_app_version_data, error_message="", show_link=1)
            else:
                return render_template('spdashboardRecentTwo.html', db_name=db, error_message="EID not found, try with existing EID", show_link=0)    
        else:
            cursor.execute("SELECT eid from rfarchive.spexecution WHERE pid=%s order by eid desc LIMIT 2;" % (db))
            exe_info = cursor.fetchall()

            if len(exe_info) >= 2:
                exe_info = (exe_info[0][0], exe_info[1][0])
            else:
                exe_info = (exe_info[0][0], exe_info[0][0])

            eid_one = exe_info[0]
            eid_two = exe_info[1]
            # fetch first eid tets results
            cursor.execute("SELECT name, eid, client_response_time, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_one, db) )
            first_data = cursor.fetchall()
            # fetch second eid test results
            cursor.execute("SELECT name, eid, client_response_time, sql_time from rfarchive.sptest WHERE eid=%s AND pid=%s;" % (eid_two, db) )
            second_data = cursor.fetchall()

            cursor.execute("SELECT description, time from rfarchive.spexecution WHERE eid=%s;" % eid_one)
            desc_data = cursor.fetchall()
            one_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            cursor.execute("SELECT description, time from rfarchive.spexecution WHERE eid=%s AND pid=%s;" % (eid_two, db))
            desc_data = cursor.fetchall()
            two_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            if first_data and second_data:
                # combine both tuples
                data = first_data + second_data
                sorted_data = sort_tests(data)
                # print(sorted_data)
                return render_template('spdashboardRecentTwo.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data,
                 eid_one = eid_one, eid_two = eid_two, one_app_version_data=one_app_version_data,
                  two_app_version_data=two_app_version_data, error_message="", show_link=1)
            else:
                return render_template('spdashboardRecentTwo.html', db_name=db, error_message="EID not found, try with existing EID", show_link=0)

    else:
        return redirect(url_for('redirect_url'))


#### Snow Report End ####

#### SF Report Start ####

@app.route('/sfhome', methods=['GET', 'POST'])
def sf_historic_home():
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM sfproject WHERE name LIKE '%{name}%';".format(name=search))
        data = cursor.fetchall()
        return render_template('sfhome.html', data=data)
    else:
        cursor = mysql.connection.cursor()
        use_db(cursor, "rfarchive")
        cursor.execute("SELECT * FROM sfproject;")
        data = cursor.fetchall()
        return render_template('sfhome.html', data=data)

@app.route('/sfnew', methods=['GET', 'POST'])
def sf_add_new():
    if request.method == "POST":
        db_name = request.form['dbname']
        db_desc = request.form['dbdesc']
        cursor = mysql.connection.cursor()

        try:
            cursor.execute("INSERT INTO rfarchive.sfproject ( pid, name, description, created, updated, total) VALUES (0, '%s', '%s', NOW(), NOW(), 0);" % (db_name, db_desc))
            mysql.connection.commit()
        except Exception as e:
            print(str(e))

        finally:
            return redirect(url_for('sf_historic_home'))
    else:
        return render_template('sfnew.html')

@app.route('/<db>/sfdeldbconf', methods=['GET'])
def sf_delete_db_conf(db):
    return render_template('sfdeldbconf.html', db_name = db)

@app.route('/<db>/sfdelete', methods=['GET'])
def sf_delete_db(db):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM rfarchive.sfproject WHERE pid='%s';" % db)
    mysql.connection.commit()
    return redirect(url_for('sf_historic_home'))

@app.route('/<db>/sfsearch', methods=['GET', 'POST'])
def sfsearch(db):
    if request.method == "POST":
        search = request.form['search']
        cursor = mysql.connection.cursor()
        # use_db(cursor, db)
        try:
            if search:
                cursor.execute("SELECT * from rfarchive.sftest WHERE (pid={pid}) and (name LIKE '%{name}%' OR eid LIKE '%{name}%') ORDER BY eid DESC LIMIT 500;".format(name=search, pid=db))
                data = cursor.fetchall()
                return render_template('sfsearch.html', data=data, db_name=db, error_message="")
            else:
                return render_template('sfsearch.html', db_name=db, error_message="Search text should not be empty")
        except Exception as e:
            print(str(e))
            return render_template('sfsearch.html', db_name=db, error_message="Could not perform search. Avoid single quote in search or use escaping character")
    else:
        return render_template('sfsearch.html', db_name=db, error_message="")

@app.route('/<db>/sfehistoric', methods=['GET'])
def sfehistoric(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT * from rfarchive.sfexecution WHERE pid=%s order by eid desc LIMIT 500;" % (db))
    data = cursor.fetchall()
    return render_template('sfehistoric.html', data=data, db_name=db)

@app.route('/<db>/sfdeleconf/<eid>', methods=['GET'])
def sfdelete_eid_conf(db, eid):
    return render_template('sfdeleconf.html', db_name = db, eid = eid)

@app.route('/<db>/sfedelete/<eid>', methods=['GET'])
def sfdelete_eid(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    # remove execution from tables: execution, suite, test
    cursor.execute("DELETE FROM rfarchive.sfexecution WHERE eid='%s' AND pid='%s';" % (eid, db))
    cursor.execute("DELETE FROM rfarchive.sftest WHERE eid='%s' AND pid='%s';" % (eid, db))
    # get no. of executions
    cursor.execute("SELECT COUNT(*) from rfarchive.sfexecution WHERE pid='%s';" % (db))
    exe_data = cursor.fetchall()

    # update sphistoric project
    cursor.execute("UPDATE rfarchive.sfproject SET total=%s, updated=now() WHERE pid='%s';" % (int(exe_data[0][0]), db))
    # commit changes
    mysql.connection.commit()
    return redirect(url_for('sfehistoric', db = db))

@app.route('/<db>/sfmetrics/<eid>', methods=['GET'])
def sfmetrics(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    # Get testcase results of execution id
    cursor.execute("SELECT * from rfarchive.sftest WHERE eid=%s;" % eid)
    test_data = cursor.fetchall()
    # get suite results of execution id
    cursor.execute("SELECT * from rfarchive.sfexecution WHERE eid=%s;" % eid)
    exe_data = cursor.fetchall()
    return render_template('sfmetrics.html', exe_data=exe_data, test_data=test_data)

@app.route('/<db>/sfcmetrics', methods=['GET'])
def sfcmetrics(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    eid_one = request.args.get('eid_one')
    eid_two = request.args.get('eid_two')
    # Get testcase results of execution id
    cursor.execute("SELECT * from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid_one, db))
    test_data_1 = cursor.fetchall()
    cursor.execute("SELECT * from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid_two, db))
    test_data_2 = cursor.fetchall()
    # get suite results of execution id
    cursor.execute("SELECT * from rfarchive.sfexecution WHERE eid=%s;" % eid_one)
    exe_data_1 = cursor.fetchall()
    cursor.execute("SELECT * from rfarchive.sfexecution WHERE eid=%s;" % eid_two)
    exe_data_2 = cursor.fetchall()
    return render_template('sfcmetrics.html', exe_data_1=exe_data_1, exe_data_2=exe_data_2, test_data_1=test_data_1, test_data_2=test_data_2)

@app.route('/<db>/sftmetrics', methods=['GET', 'POST'])
def sftmetrics(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    # Get last row execution ID
    cursor.execute("SELECT eid from rfarchive.sfexecution WHERE pid=%s order by eid desc LIMIT 1;" % db)
    data = cursor.fetchone()
    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.sftest WHERE eid=%s;" % data)
    data = cursor.fetchall()
    return render_template('sftmetrics.html', data=data, db_name=db)

@app.route('/<db>/sftmetrics/<eid>', methods=['GET', 'POST'])
def sfeid_tmetrics(db, eid):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    # Get testcase results of execution id (typically last executed)
    cursor.execute("SELECT * from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid, db))
    data = cursor.fetchall()
    return render_template('sfeidtmetrics.html', data=data, db_name=db)

@app.route('/<db>/sfdashboardRecent', methods=['GET'])
def sfdashboardRecent(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)

    cursor.execute("SELECT COUNT(eid) from rfarchive.sfexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.sftest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        cursor.execute("SELECT eid from rfarchive.sfexecution WHERE pid=%s order by eid desc LIMIT 2;" % db)
        exe_info = cursor.fetchall()

        if len(exe_info) == 1:
            pass
        else:
            exe_info = (exe_info[0], exe_info[0])
        
        cursor.execute("SELECT * from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (exe_info[0][0], db))
        last_exe_data = cursor.fetchall()

        cursor.execute("SELECT name, ept_time from rfarchive.sftest WHERE eid=%s AND pid=%s order by ept_time desc LIMIT 5;" % (exe_info[0][0], db))
        crt_data = cursor.fetchall()

        cursor.execute("SELECT COUNT(name) from rfarchive.sftest WHERE eid=%s" % exe_info[0][0])
        tables_data = cursor.fetchall()

        return render_template('sfdashboardRecent.html', last_exe_data=last_exe_data, exe_info=exe_info, db_name=db,
         crt_data=crt_data, tables_data=tables_data)    
    else:
        return redirect(url_for('redirect_url'))


@app.route('/<db>/sfdashboardRecentTwo', methods=['GET', 'POST'])
def sfdashboardRecentTwo(db):
    cursor = mysql.connection.cursor()
    # use_db(cursor, db)
    cursor.execute("SELECT COUNT(eid) from rfarchive.sfexecution WHERE pid=%s;" % db)
    results_data = cursor.fetchall()
    cursor.execute("SELECT COUNT(tid) from rfarchive.sftest WHERE pid=%s;" % db)
    test_results_data = cursor.fetchall()

    if results_data[0][0] > 0 and test_results_data[0][0] > 0:

        if request.method == "POST":
            eid_one = request.form['eid_one']
            eid_two = request.form['eid_two']
            # fetch first eid tets results
            cursor.execute("SELECT name, eid, ept_time from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid_one, db) )
            first_data = cursor.fetchall()
            # fetch second eid test results
            cursor.execute("SELECT name, eid, ept_time from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid_two, db) )
            second_data = cursor.fetchall()

            cursor.execute("SELECT description, time from rfarchive.sfexecution WHERE eid=%s;" % eid_one)
            desc_data = cursor.fetchall()
            one_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            cursor.execute("SELECT description, time from rfarchive.sfexecution WHERE eid=%s AND pid=%s;" % (eid_two, db))
            desc_data = cursor.fetchall()
            two_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            if first_data and second_data:
                # combine both tuples
                data = first_data + second_data
                sorted_data = sort_tests(data)
                # print(sorted_data)
                return render_template('sfdashboardRecentTwo.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data,
                 eid_one = eid_one, eid_two = eid_two, one_app_version_data=one_app_version_data,
                  two_app_version_data=two_app_version_data, error_message="", show_link=1)
            else:
                return render_template('sfdashboardRecentTwo.html', db_name=db, error_message="EID not found, try with existing EID", show_link=0)    
        else:
            cursor.execute("SELECT eid from rfarchive.sfexecution WHERE pid=%s order by eid desc LIMIT 2;" % (db))
            exe_info = cursor.fetchall()

            if len(exe_info) >= 2:
                exe_info = (exe_info[0][0], exe_info[1][0])
            else:
                exe_info = (exe_info[0][0], exe_info[0][0])

            eid_one = exe_info[0]
            eid_two = exe_info[1]
            # fetch first eid tets results
            cursor.execute("SELECT name, eid, ept_time from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid_one, db) )
            first_data = cursor.fetchall()
            # fetch second eid test results
            cursor.execute("SELECT name, eid, ept_time from rfarchive.sftest WHERE eid=%s AND pid=%s;" % (eid_two, db) )
            second_data = cursor.fetchall()

            cursor.execute("SELECT description, time from rfarchive.sfexecution WHERE eid=%s;" % eid_one)
            desc_data = cursor.fetchall()
            one_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            cursor.execute("SELECT description, time from rfarchive.sfexecution WHERE eid=%s AND pid=%s;" % (eid_two, db))
            desc_data = cursor.fetchall()
            two_app_version_data=str(desc_data[0][0]) + "__" + str(desc_data[0][1])

            if first_data and second_data:
                # combine both tuples
                data = first_data + second_data
                sorted_data = sort_tests(data)
                # print(sorted_data)
                return render_template('sfdashboardRecentTwo.html', data=sorted_data, db_name=db, fb = first_data, sb = second_data,
                 eid_one = eid_one, eid_two = eid_two, one_app_version_data=one_app_version_data,
                  two_app_version_data=two_app_version_data, error_message="", show_link=1)
            else:
                return render_template('sfdashboardRecentTwo.html', db_name=db, error_message="EID not found, try with existing EID", show_link=0)

    else:
        return redirect(url_for('redirect_url'))


#### SF Report End ####
def use_db(cursor, db_name):
    cursor.execute("USE %s;" % db_name)

def sort_tests(data_list):
    out = {}
    for elem in data_list:
        try:
            out[elem[0]].extend(elem[1:])
        except KeyError:
            out[elem[0]] = list(elem)
    return [tuple(values) for values in out.values()]

def get_count_by_perc(data_list, max, min):
    count = 0
    for item in data_list:
        if item[0] <= max and item[0] >= min:
            count += 1
    return count

def main():
    args = parse_options()
    app.config['MYSQL_HOST'] = args.sqlhost
    app.config['MYSQL_USER'] = args.username
    app.config['MYSQL_PASSWORD'] = args.password
    app.config['auth_plugin'] = 'mysql_native_password'
    app.run(host=args.apphost)