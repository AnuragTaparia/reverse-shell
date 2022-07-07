## Multi Client

- In this multiple server-client connection can be made
- You can run server.py on your machine or on server/remote machine and client.py on target machines
- If you are running server.py on your local system than make sure that target machines and your system are in the same network
- The other thing you can do is host the server.py on a server, So that you don't have to worry about being in the same network as your target systems
- There is a intercative system(_I have named it moon_) where you can check for the available clients/target and select any one of them
  - **list** command will show you the lost of available clients
  ```
  moon> list
  ```
  - **select** command will select the target ID which you wanna control
  ```
  moon> select 0
  ```
- While you are controling the client's shell, if you wanna go back to _moon_, type the **moon** command
