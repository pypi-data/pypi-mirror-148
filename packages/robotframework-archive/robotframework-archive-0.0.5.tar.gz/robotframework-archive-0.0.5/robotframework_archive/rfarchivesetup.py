import mysql.connector
import logging

def rfarchive_setup(opts):

    # connect to database
    print("INFO: Connecting to dB")
    mydb = connect_to_mysql(opts.host, opts.username, opts.password)

    # create new user
    obj = mydb.cursor()
    print("INFO: Creating superuser with local access")
    try:
        obj.execute("CREATE USER IF NOT EXISTS 'superuser'@'localhost' IDENTIFIED BY 'passw0rd';")
        obj.execute("GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'localhost' WITH GRANT OPTION;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Creating superuser with remote access")
    try:
        obj.execute("CREATE USER 'superuser'@'%' IDENTIFIED BY 'passw0rd';")
        obj.execute("GRANT ALL PRIVILEGES ON *.* TO 'superuser'@'%' WITH GRANT OPTION;")
    except Exception as e:
        print(str(e))
    
    print("INFO: Reloading grant table")
    try:
        obj.execute("FLUSH PRIVILEGES;")
    except Exception as e:
        print(str(e))
 
    print("INFO: Creating rfarchive dB")
    try:
        obj.execute("CREATE DATABASE IF NOT EXISTS rfarchive;")
    except Exception as e:
        print(str(e))

    print("INFO: Creating required tables")
    rfdb = connect_to_mysql_db(opts.host, opts.username, opts.password, "rfarchive")
    try:
        rfobj = rfdb.cursor()
        rfobj.execute("CREATE TABLE IF NOT EXISTS hsproject ( pid INT NOT NULL auto_increment primary key, name TEXT, description TEXT, created DATETIME, updated DATETIME, total INT, percentage FLOAT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS hsexecution ( eid INT NOT NULL auto_increment primary key, pid INT, description TEXT, time DATETIME, total INT, pass INT, fail INT, skip INT, etime TEXT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS hstest ( tid INT NOT NULL auto_increment primary key, eid INT, pid INT, name TEXT, status TEXT, time TEXT, error TEXT, comment TEXT, assigned TEXT, eta TEXT, review TEXT, type TEXT, tag TEXT, updated DATETIME);")
        # snow project
        rfobj.execute("CREATE TABLE IF NOT EXISTS spproject ( pid INT NOT NULL auto_increment primary key, name TEXT, description TEXT, created DATETIME, updated DATETIME, total INT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS spexecution ( eid INT NOT NULL auto_increment primary key, pid INT, description TEXT, time DATETIME);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS sptest ( tid INT NOT NULL auto_increment primary key, eid INT, pid INT, name TEXT, browser_time FLOAT, client_response_time FLOAT, response_time FLOAT, sql_count FLOAT, sql_time FLOAT);")
        # sf project 
        rfobj.execute("CREATE TABLE IF NOT EXISTS sfproject ( pid INT NOT NULL auto_increment primary key, name TEXT, description TEXT, created DATETIME, updated DATETIME, total INT);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS sfexecution ( eid INT NOT NULL auto_increment primary key, pid INT, description TEXT, time DATETIME);")
        rfobj.execute("CREATE TABLE IF NOT EXISTS sftest ( tid INT NOT NULL auto_increment primary key, eid INT, pid INT, name TEXT, ept_time FLOAT);")
    except Exception as e:
        print(str(e))

    commit_and_close_db(mydb)

def connect_to_mysql(host, user, pwd):
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd
        )
        return mydb
    except Exception as e:
        print(e)

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

def commit_and_close_db(db):
    db.commit()
    db.close()