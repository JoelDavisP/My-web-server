import os
import socket
import time


def server_fun():
	serv_add = (host, port) = ('', 5588)
	max_clnt = 5
	serv_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serv_soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	serv_soc.bind(serv_add)
	serv_soc.listen(max_clnt)
	while True:
		clnt, add = serv_soc.accept()
		p_new = os.fork()
		if p_new == 0: 
			serv_soc.close() 
			process_req(clnt)
			clnt.close()
			os._exit(0)
		else:  
			clnt.close()

def process_req(clnt):
	req = clnt.recv(8192)
	a = req.split('\n')[0].split()[1].split('/')[1]
	out = """\
	HTTP/1.1 404 File Not Found
	"""
	strt=b'<html><body><p> Error 404 File not found</p></body></html>'
	if a.split('.')[1] == 'txt' or a.split('.')[1] == 'html':
		try:
			text_file = open(a,'rb').read()
			response = 'HTTP/1.0 200 OK\n\n' + 'Content-type: text/html\n\n' + text_file + '\n'
			clnt.sendall(response)
			clnt.close()
			time.sleep(30)
		except:
			err = ' Error 404 File not found\n\n' + 'Content-type: text/html\n\n'
			clnt.sendall(err)
			clnt.close()
			time.sleep(30)
    	if a.split('.')[1] == 'pdf':
		try:
			pdf_file = open(a,'rb').read()
			response = 'HTTP/1.0 200 OK\n\n' + 'Content-type: text/html\n\n' + pdf_file + '\n'
			clnt.sendall(response)
			clnt.close()
    			time.sleep(30)
		except:
			err = ' Error 404 File not found\n\n' + 'Content-type: text/html\n\n'
			clnt.sendall(err)
			clnt.close()
			time.sleep(30)

	if a.split('.')[1] == 'jpg' or a.split('.')[1] == 'jpeg':
		path =  os.path.abspath(a)
		size = os.path.getsize(path)
		with open(a, 'rb') as img_file:
			clnt.sendall('HTTP/1.0 200 OK\r\n' + 'Content-type: image/jpeg"\r\n' + img_file.read())
		clnt.close()
    		time.sleep(30)
			 


			#except:
			#	im_cl = clnt.makefile('wb' , 0)
			#	im_cl.write(' Error 404 File not found\n\n') 
			#	im_cl.write('Content-type: text/html\n\n')
	
if __name__ == '__main__':
    server_fun()

