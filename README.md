# static-purity
Static website generator based on Python 3

This file constitutes the program static-purity.
I built the software for my own learning and use. I hope you find it useful. The idea for this project and a significant portion of the code comes from the excellent [Rippledoc](http://www.unexpected-vortices.com/sw/rippledoc/index.html) program [Gitlab Source](https://gitlab.com/uvtc/rippledoc)

There should be a copy of the GNU General Public License stored in any repository hosting this software. If you have not received one, please see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)

# Usage

COMMAND
    static-purity.py
 
DESCRIPTION
    static-purity scans a directory for markdown files that are new 
    or have been modified since the last time the program ran. It 
    then generates html files from those markdown files and creates 
    or modifies a directory structure to host a small blog.   

    Available options:

    --build       Build entire site.  All files and 
                  link structure are regenerated

    --update      Update only files that have been 
                  added modified since last program run
                  (This option not available currently)

    -h, --help    View this page and exit
    
# Rationale

static-purity was developed for a constrained environment.  I wanted to dynamically create and host a website on a [Raspberry Pi](https://www.raspberrypi.org).  Goals are:

* fast page generation times
* minimal use of third-party libraries
* anyone should be able to create a decent looking site with zero experience
* experienced developers should be able to tweak easily
* it should "just work"

# How-To

1. Save static-purity.py to the folder that will host the website
2. From a terminal `cd /website directory/`
3. Run `python static-purity.py --build`
4. That's it!

static purity will create the following folders:

* `/css`
* `/drafts`
* `/html`
* `/img`
* `/md`

It will also create a template `./index.html` file and the initial `./archive` file.  You can create your own first post in the `./md/` directory.  Delete the template post and rebuild the site.  

You are now up and running.  Currently you must create your own `./about.html` file.  Each time your add a new post to your `./md` directory rebuild the site and all links will be regenerated.

*Note: filenames for all posts must be of the form `YYYMMDD-filename.md`*
