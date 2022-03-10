#i2p dev practice from geti2p.net

#destination and session creation
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") #prints base32 addy

'''
base32 address is a hash which is used by other peers to discover your full Destination in the network. 
If you plan to use this destination as a permanent address in your program,
save the binary data from dest.private_key.data to a local file.
'''

#creating SAM session
session_nickname = "test-i2p" #sessions must contain unique names
session_writer = await i2plib.create_session(session_nickname, destination=dest)

#making outgoing connections
remote_host  = ""
reader, writer =  await i2plib.stream_connect(session_nickname, remote_host)
writer.write("GET / HTTP/1.0\nHost: {} \r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
  data = await reader.read(buflen)
  if len(data) > 0:
      resp += data
  else:
      break

writer.close()
print(resp.decode())

#accepting incoming connections

async def handle_client(incoming, reader, writer):
  dest, data = incoming.split(b"\n", 1)
  remote_destination = i2plib.Destination(dest.decode())
  if not data:
      data = await reader.read(BUFFER_SIZE)
  if data == b"PING":
      writer.write(b"PONG")
  write.close()
