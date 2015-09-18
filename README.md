# civAdder
Adds civilization names to leader names in brackets for civilization Battle Royal Mk. II at /r/civbattleroyal
Inspired by: https://www.reddit.com/r/civbattleroyale/comments/3lanpf/a_small_request_to_the_narrators_use_country/cv5c7if

HOW-TO USE:

Remember to have civBR_civ_leader.tsv present in the same folder.
Run from command line as:
python civ_battleroyal_leader_civ_adder.py TEXTFILE
where TEXTFILE is a plain text file with the script.

Your resulting textfile with civilizations in brackets after leadernames will be written to a file called TEXTFILE_with_civs

KNOW BUGS:
In the rare case where a sentence is builded such that two different leader names matches, no civ is return. For example:
'(...) Lincoln. I (...)'
Will be parsed as: ['Lincoln','I'], which matches Lincoln, but also 'Osei Tutu I' (because of the 'I'), Alexios I Komnenos and others, all equally well.
Thus no civ will be the 'best' civ, eventhough a human would know it should be Lincoln. I have not yet coded such a logic into my script.
