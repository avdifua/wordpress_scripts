# wordpress_scripts

Here I will be collecting my own scripts for WordPress.
These scripts help me to handle the most common problems with sites which working on Linux.

My first script suspicious_code_in_wordpress.py

This is a simple script for finding text in files.
But I called this script 'suspicious code in wordpress' because wrote for finding code like this 'eval(base64_decode(' in .html and .php files.
Sometimes I found in my Wordpress sites with old theme or plugins this suspicious code, actually, this is kind of redirect virus. And usually, this virus hit a lot of files. On one site may be more than 10 or 20 infected files. 
And if you do not have backup =) it would be tiring work for you, to find and delete this code. 
This scrip does this boring work for you! 
For default this script find this code 'eval(base64_decode('.
But you can change it in value - ''pattern_suspicious_code' .
Script work in Linux and Windows.

P.S. 
This script is not perfect. I just started learning to program =)