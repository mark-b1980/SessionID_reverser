# SessionID reverser

Bruteforce tester of session IDs based in known values or yet another quick-and-dirty scriptkiddy-tool.

The script tries all potential permutations of the know values with a list of delititer characters.

The tool test also URL-, BASE64- and HEX-encoding alongside with many common hash algorythms.

**Usage**

```
m3g4h4xx0r@kali:~/session_id_reverser/$ python3 session_id_reverser.py
 (                         (   (
 )\ )                      )\ ))\ )
(()/(   (      (          (()/(()/(    (     (   )     (  (        (  (
 /(_)) ))\(  ( )\  (   (   /(_))(_))   )(   ))\ /((   ))\ )(  (   ))\ )(
(_))  /((_)\ )((_) )\  )\ |_))(_))_   (()\ /((_|_))\ /((_|()\ )\ /((_|()\
/ __|(_))((_|(_|_)((_)_(_/(_ _||   \   ((_|_)) _)((_|_))  ((_|(_|_))  ((_)
\__ \/ -_|_-<_-< / _ \ ' \)) | | |) | | '_/ -_)\ V // -_)| '_(_-< -_)| '_|
|___/\___/__/__/_\___/_||_|___||___/  |_| \___| \_/ \___||_| /__|___||_|   v.1.0
================================================================================

Enter the user ID: 1
Enter the username: admin
Enter the user email: ad@min.net 
Enter the first possible unix timestamp / seqential number: 888
Enter the last possible unix timestamp / seqential number: 999

Enter the searched SessionID to match: db54992fbd2c066d1dc31c7b325ecfc8244a3a81

Found matching session ID: sha1("admin|1|987|ad@min.net") == db54992fbd2c066d1dc31c7b325ecfc8244a3a81
```
