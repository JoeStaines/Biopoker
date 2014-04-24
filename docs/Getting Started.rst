Getting Started
===============

Biopoker has both a client and server side applications that need to be run separately. The server side handles all
of the poker logic and sends it's internal state of the game to the clients.

To run the game, change directory to the Biopoker root and then:

To run the server side::

    python TableMain.py (no. of players that will be in the game)
	
This can take a few seconds for the Table object to initialise (up to 5 seconds), so wait until the console
responds and answer the prompts
	
To run the client::

    python UI.py
	
The UI is just a 'dumb terminal' effectively and relies on the state data from the server side, 
so the server has to be run still, even if not over a network.

This will not run it with biodata enabled though. To do that, vicarious needs to be run before anything. 
Change directory to::

    (Biopoker root)\lib\vicarious\Vicarious\Vicarious\GUI
	
Then run::

    python ProcessStarter.py (path of config file)
	
The config files used for Biopoker are located in::

    (Biopoker root)\config-files
	 
Use 'config-fakes-only-2' if you want to use fake data from the fake vilistus, or qsensor-config if you want 
to use real data if you have a qsensor. For the qsensor config file, the COM port will need to be changed manually 
in the xml that corresponds to the COM port of the qsensor.

When running the TableMain command, you'll be prompted to choose if you want to use the same biodata port. If you 
say yes to this, then all of the players will use port 50008 for threshold values. It will be the same for each player 
but that is why it's used for testing. If you want to pick no, then you have to change the xml of the config files so 
that there are enough copies of all the processors that match the number of people playing. When choosing ports for 
all the new processors, they can be anything as long as they match up in terms of inPort/outport EXCEPT the threshold 
processor. For every new threshold processor, it must be 1 above the last starting from 50050. So for example, if you 
have 3 players in the game, you'll eventually have 3 threshold processors in the xml that outport on ports 50050, 50051 
and 50052 respectively.

To get any data through, you'll need to set the baseline values through the GUI. The baseline gui has a bug where 
it doesn't seem to show properly unless you resize it, so if it comes up as a gray square, then just resize the window 
and the gui should show properly

Using the batch files
---------------------

Alternatively, if running windows then you can use the supplied batch files. The same order still applies: 
vicarious -> table -> ui. The source code of the vicarious bat file will need to be changed if you want to use a 
different config file. You will also still need to edit the xml files if required as started above.