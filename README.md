This is a minimal setup for automating RAM Concept with Python.

You define the path to your RAM Concept model (.cpt), the path to your Python script, and the location of the setup.bat. 

Then you click a button in Excel and it handles everything. It writes a temporary .cmd file, activates the correct environment using setup.bat, runs your script with the model path, and deletes the .cmd file after it’s done.

The python itself should handle whatever action you want in RAM Concept—like opening the model, exporting results, or triggering design runs. A simple logging setup is already included, and that’s where you should expand the script to match your automation needs.

The intent is to work from a single project folder called "RAM Concept Setup." All your scripts, models, and the Excel file should live in that folder. If you're using this setup for other projects, you should clone or copy the entire folder and place new scripts and models inside it.

You don’t have to manage virtual environments, and you don’t need admin access after the first setup. This is built to be repeatable, portable, and dead simple.
