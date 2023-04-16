# Sunday Commander
A splitview File Explorer that runs in the Terminal.

__Warning__ The screen can at sometimes flicker heavily this seems to be an issue with how i am handling the refresh with the curses lib. So if you are a person with epilepsy please be very careful in the usage of this application. on cursor movement the terminal can flicker very rapidly.

## Usage
Clone the Repository and make the file executable:

`$ git clone https://github.com/grewek/sundaycmdr.git`

`$ cd sundaycmdr`

`$ chmod +x sundaycmdr.py`
   


Then just type `./sundaycmdr` to run the Application.

Currently you can only step into the Directories in your Home Directory.
Other features besides walking the tree will come at a later point.


## Keybindings

__h__ Select the Viewport on the left of your Screen.

__j__ Moves the file cursor down in the currently selected Viewport.

__k__ Moves the file cursor up in the currently selected Viewport.

__l__ Select the Viewport on the right of your Screen.

__i__ Changes the Directory in the currently selected Viewport, if the selected item is not a Directory nothing happens.

__o__ Go out of the current Directory in the currently selected Viewport, only works if you entered a Directory in one of the Viewpanes.

