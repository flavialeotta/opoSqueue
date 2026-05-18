# OpoSqueue v0.1.0

Package asyncio:

1. Synchronous functions
If you define a function using def async function(), the function becomes a 'coroutine', which means it is allowed to pause and wait for things. It will need 'await' which is like a pause button. 

Once this function is defined, you need asyncio.run() to run it: this type of function starts the event loop, puts the function inside it and ,manages all pauses and starts of it until you close the program.

In my main application there are two loops:
1. UI: waits for the user to click buttons. Controlled by QEventLoop(app)
2. Async: needs to check if SSH data has arrived. Controlled by asyncio.set_event_loop(loop)


Components of opoSqueue:
1. main.py
- function async main():
    a. creates the application using app = Qapplication(sys.argv);
    b. puts the app into a loop using loop = Qeventloop(app);
    c. starts a window calling TitleScreen();
    d. loops the app forever with loop.run_forever().

2. ui/window/titlescreen.py
- class TitleScreen():
