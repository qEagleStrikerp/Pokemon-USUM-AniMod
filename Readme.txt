@Pokemon Ultra Sun and Ultra Moon Animation Modifier
@Version 0.2
@Copyright qEagleStrikerp, 05.11.2019
@Tutorial for Windows. Other OSes seem not to work at the time, for certain programs are not available on those platforms

--- Version changes ---
-> Now Amie animations can be used
-> Also, you can copy animations to different locations than only the idle (important for mons like Salamence: In order to get it to the ground, you have to replace all animations)
-> Since this is now possible, it is advisable to redo all of Gen 1 to see if there are Amie animations fitting to replace the idle. At the moment, this is not done yet.

1. Info
This mod currently replaces animations for any Pokemon and form of the 1st Generation. I may do the other Gens as well if the demand is high enough.
Btw: I am no expert at programming. If you look through my python file and think "What terrible programming", then I am sorry XD.

2. Dump your game and extract the data
Follow this guide to dump your game as a decrypted CIA file: https://3ds.hacks.guide/godmode9-usage.html
Download Python 3 from: https://www.python.org/downloads/
Create a new folder (I'll refer to this as "game folder" from now on) and place the CIA in it. Rename it to "game.cia" for easier handling.
Download the CTRtool from: https://github.com/jakcron/Project_CTR/releases
Take the right ctrtool.exe appropriate for your system and place it in your game folder.
Also, download 3dstool from: https://github.com/dnasdw/3dstool/releases
Place "3dstool.exe" in your game folder as well.
Now open up CMD as administrator and navigate to your game folder, copy the following lines of code in and press enter after each one:
ctrtool --contents=contents game.cia
ctrtool --exheader=exheader.bin --exefs=exefs.bin --romfsdir=romfs --logo=logo.bcma.lz --plainrgn=plain.bin contents.0000.00000000
3dstool -xvtf cxi contents.0000.00000000 --header ncchheader.bin
It should take some time to finish.

3. Edit the games files
Download and start pk3DS (https://projectpokemon.org/home/forums/topic/34377-pk3ds-3ds-rom-editor-randomizer/)
Go to Tools -> Misc. Tools -> (un)pack + BCLIM
Now in your game folder, go to romfs/a/0/9/. Inside, there should be files from 0 to 9, without any extension. The file "4" should have about 1,3Gb and this is the file we are searching for. Drag the window next to the pk3DS window we have opened before. Now drag the file "4" into the empty box at the top. This will take some time. Afterwards, a folder named "4_g" should be created.

4. Editing the files
This is where the files included in this ZIP will come into action. Drag "AnimationModifier.py" and "data.json" into the folder that was just created. Then right-click on AnimationModifier.py and select "Edit with IDLE" (Warning: If you have Python 2 installed alongside Python 3, due to Python 2 and Python 3 behaving differently, you will probably have two options for Editing with IDLE; one with a submenu and one without. In this case, select the one with submenu and then select "Edit with IDLE 3.7"). Once IDLE has opened the file, hit F5 once to start the process. It should finish pretty quickly. If no error gets thrown, everything worked just fine! Afterwards, delete "AnimationModifier.py" and "data.json" from the folder. This is very important!

4.5 (For Advanced users who want to edit animations on their own)
If you want to edit animations on your own, you will need to download Notepad++ (https://notepad-plus-plus.org/) and Ohana3DS (https://github.com/gdkchan/Ohana3DS-Rebirth). Now load up any Pokemon data you want (file 1 is always the model, file 2 the textures, file 3 the shiny textures, file 5 the battle animations and file 6 the Amie animations) in Ohana. Look through the animations and once you have found the one you want to use instead of the idle animation, note the position of the animation. Now open up data.json with Notepad++. Navigate to the name of the animation file you are currently looking up. Every file is associated with three numbers. The first number is position of the normal animation from file 5, the second number the position of the amie animation from file 6, and the third number say to which position in file 5 the animation gets copied. For example "3, 0, 1" means that the first animation in file 5 will be replaced by the third animation in file 5. "0, 5, 2" means that the second animation in file 5 will be replaced by the fifth Amie animation from file 6. If there's a number for both a normal and a Amie animation, the program will always take the Amie animation. If the third number is 0, nothing will happen. Note though that the position of the animations differ greatly from file to file. If you want to use the fifth animation, you sometimes have to choose a number like "12" instead. So try around and increase the numbers by one until the right animation is chosen. If you want to see how it works, look up Salamence in the data.json (04748.bin).
With that knowledge, you can replace any animation of any Pokemon by changing the values associated with its file in the data.json.
If you decide to do more than just a few Pokemon, consider committing the updated data.json to the GitHub of this project!

5. Repacking the animation files
Open up pk3DS once again. and select the same tool as before. Now drag the "4_g" folder into the empty box IN THE MIDDLE, not the upper one. Select "Yes". This process while a long, long time to finish (Warning: The process is only finished once the "4_g" folder has been deleted by the program). A file named "4_g.garc" will be created. Delete the old "4" file and rename the new "4_g.garc" to just "4".

6A. Repacking the Rom itself as a CIA
[coming soon]

6B. Repacking the Rom itself as a 3DS
If you want your rom as 3DS file (e.g. for playing on Citra):
Now download HackingTool9DS from: https://github.com/Asia81/HackingToolkit9DS-Deprecated-/releases
Navigate into ExtraTools and open "3DSBuilderMod.exe".
Click "Open RomFS" and select the "romfs" folder in your game folder.
Check the option "Use an ExeFS binary".
Click "Open ExeFS" and select the "exefs.bin" folder in your game folder.
Click "Open ExHeader" and select the "exheader.bin" in your game folder.
Click "Save Location" and select your game folder; name the game however you want, e.g. "moonMod.3ds". It has to have a .3ds ending though.
Hit "Go" and wait until everything is finished. Now you should have a fully working .3ds file!

7. Last notes
I haven't been able to test every single step. If something doesn't work, please contact me (preferably at qEagleStrikerp@web.de). Same goes for game crashes and bugs, should some of them occur. And if an animation that is replaced by the mod seems weird, please tell me the name of the Pokémon. You can also contribute! If you want the mod to expand faster than I will make it expand to the other generations myself, or if you want to find some animations for Pokemon that currently still have a lame idle animation, you can help out by doing step 4.5 of this guide. When you're done, just commit the changes on GitHub.