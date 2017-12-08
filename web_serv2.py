# 'This is a minimal web server project in python that receives request from client(s) (here browser) and send the requested resources back.'

#' Usage: Run the code in python 2 editor and in browser run "http://localhost:5889/filename"'


import os
import socket
import time
def server_fun():
	serv_add = (host, port) = ('', 5889)
	max_clnt = 10
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
		except:
			err = ' Error 404 File not found\n\n' + 'Content-type: text/html\n\n'
			clnt.sendall(err)
		clnt.close()
		time.sleep(30)

	if a.split('.')[1] == 'jpg' or a.split('.')[1] == 'jpeg':
		try:
			size = os.path.getsize(path)
			path =  os.path.abspath(a)
			img_file = open(a, 'rb')
			clnt.sendall('HTTP/1.1 200 OK\r\n' + 'Accept-Ranges: bytes\r\n' + 'Content-type: image/jpeg\r\n' + 'Content-Length: ' +str(size) +'\r\n\r\n')
			clnt.sendall(img_file.read())
		except:
			err = ' Error 404 File not found\n\n' + 'Content-type: text/html\n\n'
			clnt.sendall(err)
		clnt.close()
		time.sleep(30)
	
if __name__ == '__main__':
    server_fun()
