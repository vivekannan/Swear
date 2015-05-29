# Swear
Swear uses OpenSubtitles XMLRPC API to search for movies based on the given name and then downloads a subtitle for the selected title and counts the occurence of the most commonly used swear words.

# Usage

    ./swear.py [Movie name]

# Example

    ./swear.py 'Reservoir Dogs'
    
    Found the following partial matches
    [1] Reservoir Dogs (1992)
    [2] Reservoir Dogs (2004) (TV Episode) -
    [3] 'Reservoir Dogs' Revisited (2005) (TV Special)
    [4] Reservoir Guide Dogs (1995) (Short)
    [5] Reservoir Dugs (2013) (Video)
    [6] Dogs Reservoir (2013) (TV Episode) -
    [7] Reservoir Dolls (2015) (TV Episode) -
    [8] Reservoir Drunks (2008) (Video)
    [9] Reservoir Dawgs (2014) (TV Episode) -
    [10] Reservoir Birds (1997) (TV Episode) -
    [11] Reservoir Dogs - "Why Am I Mr. Pink?" (2013) (TV Episode) -
    [12] Fathom Screening: Reservoir Dogs (2012) (TV Episode) -
    [13] Cesar Millan: People Training for Dogs (2005)
    Select a title: 1
    Selected "Reservoir Dogs (1992)", downloading subtitle...
    Boat-Load of shit, fuck, fuckin.
    Load of ass, goddamn, dick, bitch, hell.
    Dash of prick, fucking, pussy, damn, butt.
    Hint of bastard, balls, bloody, nigger, piss.
    

