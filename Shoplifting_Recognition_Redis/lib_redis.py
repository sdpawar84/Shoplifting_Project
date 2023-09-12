import redis
import linecache
import pickle
import linecache
import sys
########### Exception handling #############

def PrintException():
	exc_type, exc_obj, tb = sys.exc_info()
	f = tb.tb_frame
	lineno = tb.tb_lineno
	filename = f.f_code.co_filename
	linecache.checkcache(filename)
	line = linecache.getline(filename, lineno, f.f_globals)
	print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


########################################

########### Redis Handling #############
def redis_write(path,data,session):
	val=pickle.dumps(data, protocol=pickle.DEFAULT_PROTOCOL)
	try:
		session.set(path,val)
		return True
	except:
		return False

def redis_read(path,session,delete=False):
	val=session.get(path)
	if delete:
		session.delete(path)
	if val:
		return pickle.loads(val)
	else:
		return False


def redis_push(path,data,session):
	val=pickle.dumps(data, protocol=pickle.DEFAULT_PROTOCOL)
	try:
		session.rpush(path,val)
	except:
		return False

def redis_pop(path,session):
	val=session.lpop(path)
	if val:
		return pickle.loads(val)
	else:
		return False


def writeq(nodeid,queue,camid,data,session,size=5):
	try:
		q_l=session.llen(nodeid+"/"+queue+"/"+camid)
		if q_l > size:
			return False
		redis_push(nodeid+"/"+queue+"/"+camid,data,session)
	except:
		print("Redis Error")
		PrintException()
		return False

def readq(nodeid,queue,camid,session):
	try:
		return redis_pop(nodeid+"/"+queue+"/"+camid,session)
	except:
		print("Redis Error")
		return False


def list_keys(pattern,session):
	try:
		val=session.keys(pattern=pattern)
	except:
		print("List_keyerror")
		return False
	return val

def calculate_ql(pattern,session):
	final_ql=0
	try:
		keys=list_keys(pattern,session)
	except:
		return False

	for k in keys:
		try:
			q_l=session.llen(k)
			final_ql=final_ql+q_l
		except:
			pass
	if len(keys)==0:
		ratio=0
	else:
		ratio=final_ql/len(keys)
	return ratio


########################################




