#! /usr/bin/python3

# ----------------------------------------------------------------------------------------------- #
# CSC346 Clouding Computing - Project 8
# Author: Glen Chin
# Title: database_adapter.py
# Description: Database Adapter for all related database operations to support api/servers
# ----------------------------------------------------------------------------------------------- #

import MySQLdb
import dbinfo

# Creates the connection to the RDS database
# Uses login information stored in dbinfo
def create_conn():
    conn = MySQLdb.connect(host = dbinfo.host,
                            user = dbinfo.user,
                            passwd = dbinfo.password,
                            db = "csc346_servers")
    return conn

# ----------------------------------------------------------------------------------------------- #
# GETTER METHODS -------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Get all rows from servers table
# Returns rows in servers
def get_servers(conn):
    cursor = conn.cursor()   
    cursor.execute('SELECT * FROM servers')
    data = cursor.fetchall()
    cursor.close()
    return data

# Get a server row by id and owner
# Returns one row in server associated with id and owner
def get_server_by_id(conn, id, owner):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM servers WHERE id=%s AND owner=%s', (id,owner))
    data = cursor.fetchall()
    cursor.close()
    return data

# Get all servers owned by owner
# Returns rows in server associated with owner
def get_servers_by_owner(conn, owner):
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM servers WHERE owner=%s', (owner,))
    data = cursor.fetchall()
    cursor.close()
    return data

# Get a server id by instanceID
# Returns id of server associated with instanceID
def get_server_by_instanceID(conn, instance_id):
    cursor = conn.cursor() 
    cursor.execute('SELECT id FROM servers WHERE instanceID=%s', (instance_id,))
    data = cursor.fetchall()
    cursor.close()
    return data[0][0]

# ----------------------------------------------------------------------------------------------- #
# SETTER METHODS -------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------- #

# Insert a new server into servers table
def insert_server(conn, owner, description, instance_id):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ' +
                    'servers(owner, description, instanceID) ' +
                    'VALUES(%s, %s, %s)',
                    (owner, description, instance_id))
    cursor.close()
    conn.commit()


# Update server state by server id
def update_server_state_ready(conn, instance_id):
    cursor = conn.cursor()
    cursor.execute('UPDATE servers ' +
                    'SET ready=1 ' +
                    'WHERE instanceID=%s',
                    (instance_id,))
    cursor.close()
    conn.commit()

# Delete a server by instance id
def delete_server(conn, instanceID):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM servers ' +
                    'WHERE instanceID=%s',
                    (instanceID,))
    cursor.close()
    conn.commit()

# Check if any rows returned from servers table by server id
# Returns True when server with given server id exist, False otherwise
def is_exist_server(conn, id):
    cursor = conn.cursor() 
    cursor.execute('SELECT * FROM servers WHERE id=%s', (id,))
    count = cursor.rowcount
    cursor.close()
    return (count > 0)

# Check if any rows returned from sessions table by owner
# Returns True when server with given owner exist, False otherwise
def checkCookieExist(conn, owner):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ' +
                    'WHERE owner=%s',
                    (owner,))
    count = cursor.rowcount
    if count == 1:
        return True
    return False

# Check if any rows returned from sessions table by owner and has not expired
# Returns True when server with given owner exist and has not expired, False otherwise
def checkCookieValidity(conn, owner):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sessions ' +
                    'WHERE owner=%s and expiration > NOW()',
                    (owner,))
    count = cursor.rowcount
    if count == 1:
        return True
    return False

# Insert a new session into sessions table
def insert_session(conn, owner):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO ' +
                    'sessions(owner, expiration) ' +
                    'VALUES(%s, ADDTIME(NOW(), "00:10:00")) ',
                    (owner,))
    cursor.close()
    conn.commit()

# Update session expiry by another 10 minutes
def update_session(conn, owner):
    cursor = conn.cursor()
    cursor.execute('UPDATE sessions ' +
                'SET expiration=ADDTIME(NOW(), "00:10:00") ' +
                'WHERE owner=%s',
                (owner,))
    cursor.close()
    conn.commit()