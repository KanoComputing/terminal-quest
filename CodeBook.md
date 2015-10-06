# Terminal Quest

At the beginning of each script, the instruction **\# coding: utf-8** was added in order to treat the Italian accented vovels correctly. All the text printed in the story frame (at the left) and the error messages in the terminal (at the right) have been translated. The italian objects names have been used. This Italian version is localized for kids living in Tuscany. It will be localized appropriately, when presenting the game in other regions. 

These changes have been applied to the following files

- linux_story/titles.py
- linux_story/Terminal.py
- linux_story/step_helper_functions.py
- linux_story/load_defaults_into_filetree.py 
  - The **containing_dir** was changed to ascii_assets/story_files/it to address the italian files.

- linux_story/gtk3/FinishDialog.py
- linux_story/gtk3/MenuScreen.py

- linux_story/story/challenges/introduction.py
- linux_story/story/challenges/challenge_*.py

- linux_story/story/terminals/terminal_bernard.py
- linux_story/story/terminals/terminal_cd.py
- linux_story/story/terminals/terminal_eleanor.py
- linux_story/story/terminals/terminal_nano.py


- linux_story/story/trees/default_trees.yaml
  - All the objects names have been translated.

- linux_story/ascii_assets/story_files/it/*
  - The subdirectory it/ has been created in  linux_story/ascii_assets/story_files/ to host the italian versions of the ascii_assets.
  - Eventually, the contents have been translated in the ascii_assets.
  - The newspaper (it/giornale) has been redesigned, in order to accomodate the longer name Corriere di Strada In Chianti.
  - In the same directory there is the transl-cp-file.sh script which was used to generate the italian files.


