"""slackclipper_runner.py :: Entry point for slackclipper
"""

__author__ = "Heath Raftery <heath@empirical.ee>"

from slackclipper import *
import sys
import argparse
from urllib.parse import urlparse
# Tried the tkinter method of clipboard access, but it was rough as guts.
# No big deal to have this dependency.
from pyperclip import copy, paste


def link_validator(link):
  try:
    # Lots of ways to validate a link, but best for us is "will definitely not work"
    # so that means using the same urlparse as slackclipper, plus a sanity check to
    # rule out lots of false positives like "https://https://https://www.foo.bar" or
    # "http://www.google.com" or "ftp://warez.r.us".
    p = urlparse(link)
    return p.scheme and p.netloc and "slack" in p.netloc.lower()
  except:
    return False


# provide entry point as function, so it can be called from setuptools
def main():
  pass


parser = argparse.ArgumentParser(
  epilog="Note: this program is not endorsed or authorised in any way by Slack Technologies LLC.",
  description="""Copy the contents of a Slack thread.

Run this prgram after copying the Slack thread link to the clipboard.
The clipboard will be replaced with the contents of the thread.""")
parser.add_argument('-p', '--pipe', 
                    help="read the link from stdin and write the content to stdout, instead of using the clipboard")
parser.add_argument('-u', '--update-credentials', 
                    help="insteed of clipping a thread, just extract your credentials from Slack and store them for future use")

args = parser.parse_args()

if args.u or not are_credentials_present():
  print("Attempting to extract Slack tokens. NOTE: Slack must be closed for this to work.")
  print("You may be prompted for your login password, possibly twice. This is only used")
  print("to retrieve the Slack storage password.")
  print("")
  
  try:
    update_credentials_store()
  except Exception as e:
    print("Failed to update credentials. Details of error are below.")
    sys.exit(str(e))
    #raise e # for debugging
  else:
    print("Credentials successfully updated.")
    print("")
    if args.u:
      sys.exit(0)


try:
  link = paste()
  if not link_validator(link):
    print("Clipboard does not seem to contain a link.")
    print("Either copy a link to the clipboard and enter 'y', or enter 'n' to quit.")
    reply = str(input("Would you like to try again? (y/n): ")).lower().strip()
    if reply[0] == 'n':
      sys.exit(0)
  
  print(f"Clipping thread for link: {link}")
  content = get_thread_content(paste())
  copy(content)
  print("Done. Results are on the clipboard ready to be pasted wherever you like.")
except Exception as e:
  print("Failed. Details of error are below.")
  print(str(e))
  #raise # for debugging
