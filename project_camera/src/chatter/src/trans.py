import math
import numpy as np
def rx(a):
	return [[1,0,0],
			[0,math.cos(a),-math.sin(a)],
			[0,math.sin(a),math.cos(a)]] 
def ry(a):
	return [[math.cos(a),0,math.sin(a)],
			[0,1,0],
			[-math.sin(a),0,math.cos(a)]] 
def rz(a):
	return [[math.cos(a),-math.sin(a),0],
			[math.sin(a),math.cos(a),0],
			[0,0,1]] 
def arMarker_to_base_position(anglex,angley,anglez,pbx,pby,pbz,qabx,qaby,qabz):
	return reduce(np.dot,rx(anglex),ry(angley),rz(anglez),[[pbx],[pby],[pbz]]) + [[qabx],[qaby],[qabz]]	

def arMarker_to_base_quaternion(x1,y1,z1,w1,x2,y2,z2,w2):
	x = w1*w2 + x1*w2 + y1*z2 - z1*y2
	y = w1*y2 - x1*z2 + y1*w2 + z1*x2
	z = w1*z2 + x1*y2 - y1*x2 + z1*w2
	w = w1*w2 - x1*x2 - y1*y2 - z1*z2 
	a = [x,y,z,w]
	return a