#!/usr/bin/env python3.8

import os,sys
import datetime as dt
from datetime import datetime,date,time,timedelta

import argparse

import mysql.connector
from mysql.connector import errorcode

#
# MyMySql : A module for dumb MySql stuff
#

# Purpose: A compact and simple interface to mysql.connector
# Primarily, this is to create an API similar to my other module,
# mysqlite3. With the API's being similar enough that they can be
# encapsulated together into a class heirarchy.
# While I know modules exist to do this very same thing, I do this
# here mostly to eliminate some outside dependancies

VERSION = (0,0,1)

__version__ = ".".join([str(x) for x in VERSION])

# MySQL Class Wrapper
class MySQLWrapper():
	"""MySQL Baking Datastore"""

	# Server
	Server = None
	# User
	User = None
	# Password
	Password = None
	# Database
	Database= None
	# Active Database
	Connection = None
	# Active Cursor
	Cursor = None

	# Initialize Instance
	def __init__(self,server,user,password,database=None):
		"""Initialize Instance"""

		self.Server = server
		self.User = user
		self.Password = password
		self.Database = database
		self.Connection = None
		self.Cursor = None

	# Use Database
	def Use(self,database=None):
		"""Set Database To Use"""

		if database == None:
			database = self.Database

		self.Execute(f"USE {database}")

		self.Database = database

	# Create Database
	def CreateDatabase(self,**kwargs):
		"""Create Database"""

		dbname = kwargs.get("name",None)

		if dbname: self.Database = dbname

		if self.Database and self.IsOpen():
			self.Execute(f"CREATE DATABASE '{self.Database}'")

			self.Use()
		else:
			raise  IOError("Database is not open")

	# Create A Table
	def CreateTable(self,table_spec):
		"""Create Table"""

		if self.IsOpen():
			self.Execute(table_spec)
		else:
			raise IOError("Database is not open")

	# Open Backing Store
	def Open(self,**kwargs):
		"""Open MySQL Database"""

		if self.Database:
			self.Connection = mysql.connector.connect(host=self.Server,user=self.User,password=self.Password,database=self.Database)
		else:
			self.Connection = mysql.connector.connect(host=self.Server,user=self.User,password=self.Password)

		self.Cursor = self.Connection.cursor()

		return self.Cursor

	# Check if Database is Open
	def IsOpen(self):
		"""Check if Backing Store is Open"""

		return self.Connection != None

	# Check if Database is Closed
	def IsClosed(self):
		"""Inverted IsOpen"""

		return not self.IsOpen()

	# Close Backing Store
	def Close(self):
		"""Close MySQL Database"""

		if self.Cursor != None:
			self.Cursor.close()
			self.Cursor = None

		if self.Connection != None:
			self.Connection.close()
			self.Connection = None

	# Get Cursor
	def GetCursor(self,new_cursor=False):
		"""Get current (or new) Cursor"""

		if not self.IsOpen():
			raise IOError("Database is not open")

		if new_cursor:
			cursor = self.Connection.cursor()

			if self.Cursor == None:
				self.Cursor = cursor

			return cursor

		return self.Cursor

	# Basic Execution Atom
	def Execute(self,cmd,parameters=None,cursor=None):
		"""Basic Execution Atom"""

		if not self.IsOpen():
			raise IOError("Database is not open")

		if cursor == None:
			cursor = self.GetCursor()

		if parameters:
			cursor.execute(cmd,parameters)
		else:
			cursor.execute(cmd)

	# Execution with result set
	def Resultset(self,cmd,parameters=None,cursor=None):
		"""Execution with result set"""

		if not self.IsOpen():
			raise IOError("Database is not open")

		if cursor == None:
			cursor = self.GetCursor()

		if parameters:
			cursor.execute(cmd,parameters)
		else:
			cursor.execute(cmd)

		results = cursor.fetchall()

		return results

	# Basic Insert
	def Insert(self,cmd,parameters=None,cursor=None):
		"""Basic/Compact Insert"""

		try:
			self.Execute(cmd,parameters,cursor)

			self.Connection.commit()
		except Exception as err:
			raise err

	# Run A Basic Select
	def Select(self,cmd,parameters=None,cursor=None):
		"""Compact Select Statement"""

		return self.Resultset(cmd,parameters,cursor)

	# Update A Record(s)
	def Update(self,cmd,parameters=None,cursor=None):
		"""Update Some/A Record(s)"""

		try:
			self.Execute(cmd,parameters,cursor)

			self.Connection.commit()
		except Exception as err:
			raise err

	# Delete A Record(s)
	def Delete(self,cmd,parameters=None,cursor=None):
		"""Delete A record"""

		try:
			self.Execute(cmd,parameters,cursor)

			self.Connection.commit()
		except Exception as err:
			raise err


# Test Stub
def test(args,unknowns,**kwargs):
	"""Test Stub"""

	import py_helper as ph
	from py_helper import DebugMode,CmdLineMode,Msg,DbgMsg,ErrMsg

	CmdLineMode(True)
	DebugMode(args.debug)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Mymysql test stub parser")

	parser.add_argument("-d","--debug",action="store_true",help="Enter debug mode")
	parser.add_argument("-t","--test",action="store_true",help="Enter test mode")

	args,unknowns = parser.parse_known_args()

	if args.test:
		test(args,unknowns)
	else:
		print("This module is not intended for stand alone execution")
