
# Terminal Quest

## What has been done so far

Modifications that will be cleaned up at the end, are marked within #arf comments throughout the code.

The following files have been modified so far:

#### linux_story/story/challenges/challenge_X.py, with X=1,31, i.e. all the challenges.

AAAHRG... the story does not finish! I was taken.....! Well, that is interesting too.... 

At the beginning of each script, the instruction **\# coding: utf-8** was added in order to treat the Italian accented vovels correctly.

All the text in **story** have been translated.

The English texts have been left, commented with \#arf, in the meanwhile.

The italian objects names have been used.

This Italian version is localized for kids living in Tuscany. It will be localized appropriately, when presenting the game in other regions.


#### linux_story/load_defaults_into_filetree.py

The **containing_dir** was changed to ascii_assets/story_files/it to address the italian files.


#### linux_story/story/trees/default_trees.yaml

All the objects names have been translated.


#### linux_story/story/terminals/terminal_eleanor.py

Occurrences of "cat Eleanor" have be changed to "cat Eleonora"
otherwise Eleanor does never speak when asked!


#### linux_story/ascii_assets/story_files/it/*

The subdirectory it/ has been created in  linux_story/ascii_assets/story_files/ to host the italian versions of the ascii_assets.

Eventually, the contents have been translated in the ascii_assets calles by challenges 1-10, so far.

The newspaper (it/giornale) has been redesigned, in order to accomodate the longer name Corriere di Strada In Chianti.

In the same directory there is the transl-cp-file.sh script which was used to generate the italian files.



## What has to be done

In the following modules there are texts that have to be translated

#### step_helper_functions.py

#### Terminal.py

#### gtk3/FinishDialog.py

#### gtk3/MenuScreen.py

#### story/challenges/introduction.py

#### story/terminals/terminal_bernard.py

#### story/terminals/terminal_cd.py

#### story/terminals/terminal_eleanor.py

#### story/terminals/terminal_


