#!/usr/bin/env python
import binascii
import struct
import time
import util
import sys

def createcoinbasetx(data,address,msg):
	nTime = data['curtime']
	extranonce_type = '>Q'
	extranonce_placeholder = struct.pack(extranonce_type, int('f000000ff111111f', 16))
	extranonce_size = struct.calcsize(extranonce_type)

	height = data['height']
	flags = data['coinbaseaux']['flags']
	extradata = 'NeuralMiner'
	_time = nTime

	#in
	scriptSig_template = (util.ser_number(height) + binascii.unhexlify(flags) + util.ser_number(int(_time)) + chr(extranonce_size), util.ser_string('' + extradata))
	scriptSig = scriptSig_template[0] + extranonce_placeholder + scriptSig_template[1]

	prevout_hash = 0L
	prevout_n = 2 ** 32 - 1
	nSequence = 0

	txIn = ""
	txIn += "".zfill(64).decode('hex')
	txIn += struct.pack("<I", prevout_n)
	txIn += util.ser_string(scriptSig)
	txIn += struct.pack("<I", nSequence)

	#out
	scriptPubKey = util.script_to_address(address)

	nVersion = 1
	nLockTime = 0
	nValue = data['coinbasevalue']

	txOut = ""
	txOut += struct.pack("<q", nValue)
	txOut += util.ser_string(scriptPubKey)

	coinbasetx = ""
	coinbasetx += struct.pack("<i", nVersion)
	coinbasetx += chr(01)
	coinbasetx += txIn
	coinbasetx += chr(01)
	coinbasetx += txOut
	coinbasetx += struct.pack("<I", nLockTime)

	coinbase = binascii.hexlify(coinbasetx)

	return coinbase
