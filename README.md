# Project Description
Automatic clan war stats extraction and clan member donation (and some more info as well) extraction. A very much work-in-progress.

# Requirement
1. At least one "Key" required by Clash Royale API is already created (see "Getting Started" for detailed instructions)
2. Python 3
(3. bash, optional)

# Getting Started
0. clone the repo into your local repository, say $SRC
1. Register an account (if not already exist) at Clash Royale API (https://developer.clashroyale.com/)
2. Log in to Clash Royale API
3. (The following reference to the UI is as off July 8th, 2019. The website UI might change with time.)
At the top right corner, there is your name in a box as a dropdown menu. Click on it, and you will see "My Account" and "Log Out". Click on "My Account".
4. Click "Create New Key" or click in an existing key created before.
5. A "Token" is generated for every key created. Copy and paste the Token string into a file, with any file name of your preference in any directory.
Suggestion: put the token file in $SRC
6. Edit $SRC/get_playerstats.sh and $SRC/get_warstats.sh by filling the TOKEN and CLANTAG variable values and save the changes.
7. Open a terminal,
cd $SRC
bash get_playerstats.sh
bash get_warstats.sh
