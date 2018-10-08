TCP Echo with Framing

In this lab we were to implement fileClient.py and fileServer.py to transfer files between each other and gracefully handle:

-zero length files
-user attempts to transmit a file which does not exist
-file already exists on the server
-the client or server unexpectedly disconnect

Description of my code:

The overall task is complete, the only main issue with it is the fact that I can only send .txt files because I specifically ask the server to look for those types of files when receiving. The reason why it is only text files is because when I tried to ask the server to look for other types of files, the client kept getting stuck with waiting to receive something back from the server and vice versa. For some reason when I would use "os.path.exist" only, it wouldn't work, it was only able to work when I specifically asked for a file type. I tried other methods such as assigning the payload to two different variables but it would still get stuck.

The fileClient code along with the files I was using to test are found in the Client folder under the file-transfer-lab directory. filesServer is found in the other folder called Server. I had to add the framedSocket.py code to each of the folders because it couldn't find the code when I would run. 