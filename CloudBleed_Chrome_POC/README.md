This project is in response to the silly-named, but scary CloudFront CDN issue currently unfolding. While it is very possible that your data is secure if you use a site on this list: https://github.com/pirate/sites-using-cloudflare a good chunk were verified to have had sensitive data exposed - including passwords, logins, personal information, etc.

As always when something like this comes about, change your passwords. This one is difficult because CloudFront is a massive player in this space so many, many sites were affected. Just because a site is on the list does not mean the sensitive parts of the site were, just because the sensitive parts were does not mean that *your* data was, etc. Still, this involves data that may still be cached/present, and it's worth the time to change your passwords if this affects you.

This is a good time to put in a big plug for a good password management system. Lastpass and 1password have excellent apps as do many others.

To do see what I needed to change I exported my Chrome password file, then wrote this script to dump out anything I had affected. 

To export Chrome passwords:

1. Open Chrome://flags in your Chrome.
2. Find Password Import and Export option, select Enabled from the drop-down box, and then restart the Chrome browser.
3. Now, open Chrome://settings/passwords page.
4. Click on Export button to export/backup saved passwords.' 

Steps from: www.intowindows.com/how-to-backup-saved-passwords-in-google-chrome-browser/

Requirements:

1. OSX, or Linux environments.
2. Python 2.7 or later.
3. Existing /tmp/password.csv from the above steps.
4. check.py from this project existing in /tmp/check.py

Download checker.py from here, and run it. It will download, unzip, and compare only the website name (with a little formatting) against the affected list. This password file should be *deleted* as soon as you are done (the script will not do this for you), and if in doubt - change any credentials that may have been revealed. Don't trust that the master list is valid, or that my novice attempts to deal with this didn't miss something important.
