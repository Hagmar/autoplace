# autoplace
Automate your beautiful (?) Place creations!

# What is this?
Have you struggled coordinating with other redditors to draw your masterpiece(s) on Reddit's [Place](
https://www.reddit.com/place/)? This is a way to automatically coordinate everyone to work together on a project!

Project owners can simply draw an image using the Place colors, specify the coordinate at which they want it, and start an autoplace server.
Clients can then connect to servers and will automatically be given instructions for which pixels to paint and which color to paint it.


# Requirements
* Python 3.5 or higher
* [Requests](https://pypi.python.org/pypi/requests)
* [NumPy](https://pypi.python.org/pypi/numpy) (If running a server)
* [Websockets](https://pypi.python.org/pypi/numpy)
* A Reddit account (If running a client)

These can be installed manually or by running `pip3 install -r requirements.txt`

# How to use
1. Make sure you fulfill the requirements above
## Server
2. Create an image using the the colors available in Place ([See below](#colors))
    * If you use any other colors than the Place palette, they will be ignored. This way you can draw pictures which are not rectangular as well.
3. Start the server with `python3 place_server.py <project name> <image> <x> <y>`
    * Project name is the name that you give to clients so they can join the project
    * Image is the picture you made in step 2
    * x and y are the coordinates at which to draw the image
    * The server accepts optional arguments for the hosts to allow and the port to listen on
    * Run `python3 place_server.py -h` for help
4. Watch the magic happen!

## Client
2. Obtain a host, port and project from Reddit, a friend, your grandma or the local fire department.
3. Start the client with `python3 place_client.py <host> <port> --proj <project name>`
4. The script will prompt you for your Reddit credentials
    * You can also use `--user <username>` and/or `--pass <password>` to provide credentials directly
5. Watch the magic happen!

# Colors
These are the valid colors in the Place palette:
* ![#ffffff](https://placehold.it/15/ffffff/000000?text=+) `#ffffff`
* ![#e4e4e4](https://placehold.it/15/e4e4e4/000000?text=+) `#e4e4e4`
* ![#888888](https://placehold.it/15/888888/000000?text=+) `#888888`
* ![#222222](https://placehold.it/15/222222/000000?text=+) `#222222`
* ![#ffa7d1](https://placehold.it/15/ffa7d1/000000?text=+) `#ffa7d1`
* ![#e50000](https://placehold.it/15/e50000/000000?text=+) `#e50000`
* ![#e59500](https://placehold.it/15/e59500/000000?text=+) `#e59500`
* ![#a06a42](https://placehold.it/15/a06a42/000000?text=+) `#a06a42`
* ![#e5d900](https://placehold.it/15/e5d900/000000?text=+) `#e5d900`
* ![#94e044](https://placehold.it/15/94e044/000000?text=+) `#94e044`
* ![#02be01](https://placehold.it/15/02be01/000000?text=+) `#02be01`
* ![#00d3dd](https://placehold.it/15/00d3dd/000000?text=+) `#00d3dd`
* ![#0083c7](https://placehold.it/15/0083c7/000000?text=+) `#0083c7`
* ![#0000ea](https://placehold.it/15/0000ea/000000?text=+) `#0000ea`
* ![#cf6ee4](https://placehold.it/15/cf6ee4/000000?text=+) `#cf6ee4`
* ![#820080](https://placehold.it/15/820080/000000?text=+) `#820080`
