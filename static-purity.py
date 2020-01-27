#!/usr/bin/env python3

######################################################################
# Copyright 2020 James Evans <jwhevans@hotmail.com>
#
# This file constitutes the program static-purity and is the static
# website generator for mnml.blog
#
# This file is free software and may be modified and/or redistribuited 
# under the terms of the GNU General Public License by the Free 
# Software Foundation.
#
# I built the software for my own learning and use. I hope you find it 
# useful. This software comes with NO WARRANTY; without even an 
# implied warranty of merchantability or fitness for a particular 
# purpose. See the GNU General Public License for more details.
#
# There should be a copy of the GNU General Public License stored in 
# any repository hosting this software. If you have not received one, 
# please see <http:www.gnu.org/licenses/>
######################################################################

import os, sys, markdown as md, time
from datetime import date

VERSION = "2020-01-26"
PROJECT_NAME = "static-purity"
AUTHOR = "James Evans"
COPYRIGHT = ""

TODAY = date.today().strftime('%Y-%m-%d')

all_md_sorted_rev = []
default_dirs = ['css', 'drafts', 'html', 'img', 'md']

help_msg = """
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
"""

available_options = ["-h", "--help", "--build", "--update"]

######################################################################
def main():
    t0 = time.time()
    print(f"Running {PROJECT_NAME} - v{VERSION}...")

    if len(sys.argv) > 1 and sys.argv[1] == '--build':
        # TODO: rebuild the site
        print(f" Rebuilding {PROJECT_NAME}")
    elif len(sys.argv) > 1 and sys.argv[1] == '--update':
        # TODO: update the site
        print(f" Updating {PROJECT_NAME}")
        sys.exit(0)
    else:
        print(help_msg)
        sys.exit(0)

    # Verifying directory structure and setting up if needed
    print(" Verifying directory structure...")
    for dir in default_dirs:
        if not os.path.exists(dir):
            print(f"""  Directory {dir} is missing.  Creating...""")
            os.makedirs(dir)

    # Check if at least one markdown file and ./css/styles.css exist
    # If not give the user an option to insert a template
    # or to exit and create their own before running again
    if not any(fnm.endswith('.md') for fnm in os.listdir('./md/')):
        file_is_missing("Markdown")
    
    if not os.path.exists('./css/styles.css'):
        file_is_missing("CSS")

    print(" Sanitizing file names...")
    sanitize_filenames('./md/')

    print(" Sorting md files...")
    global all_md_sorted_rev
    all_md_sorted_rev = sorted(os.listdir('./md/'), reverse=True)

    print(" Converting markdown to html...")
    md_to_html('./md/')

    print(" Creating archive...")
    create_archive()

    t1 = time.time()
    print(f"Execution complete. Time: {t1-t0:.4f} s")

######################################################################
def file_is_missing(fnm):
    res = input(f"""
WARNING:
    {fnm} files were not found.  These files are necessary for {PROJECT_NAME}
    to build your site. You may continue and a template file will be
    created or you may quit and create {fnm} files first. 
    Continue? y/n: """)
    if res == 'y' or res == 'Y':
        print(f"Creating template {fnm}...")
        create_missing_file(fnm)
        pass
    elif res == 'n' or res == 'N':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Improper input. Exiting...")
        sys.exit(0)


def sanitize_filenames(path):
    fnms = os.listdir(path)
    for fnm in fnms:
        os.rename(os.path.join(path, fnm), 
        os.path.join(path, fnm.replace(' ', '-')))


def create_missing_file(fnm):
    if fnm == "Markdown":
        f = open('./md/' + TODAY + '-Template.md', 'w')
        f.write(default_index_md)
        f.close()
    elif fnm == "CSS":
        f = open('./css/styles.css', 'w')
        f.write(default_styles_css)
        f.close()
    else:
        print(f"WARNING: Could not create necessary file")
        

def md_to_html(path):
    for md_file in all_md_sorted_rev:
        if md_file[-2:] == 'md':
            f = open(path + md_file, 'r')
            html = md.markdown(f.read())
            f.close()
            title = str(md_file[9:-3]).title().replace('-', ' ')
            create_html(html, md_file, title)


def create_html(content, name, title):
    dir_depth = 1 # deepest directory level - all execept index

    idx = all_md_sorted_rev.index(name)
    if idx == 0: 
        # first record - this is the index
        dir_depth = 0
        html_bef = html_before.replace('{{PREV_LINK}}', '←prev')
        html_aft = html_after.replace('{{PREV_LINK}}', '←prev')

        if len(all_md_sorted_rev) > 1:
            next_fnm = './html/' + all_md_sorted_rev[idx + 1][:-2] + 'html'
            next_link = f"""<a href="{next_fnm}">next→</a>"""
            html_bef = html_bef.replace('{{NEXT_LINK}}', next_link)
            html_aft = html_aft.replace('{{NEXT_LINK}}', next_link)
        else:
            next_fnm = '../archive.html'
            next_link = f"""<a href="{next_fnm}">next→</a>"""
            html_bef = html_bef.replace('{{NEXT_LINK}}', next_link)
            html_aft = html_aft.replace('{{NEXT_LINK}}', next_link)
    if idx == 1: 
        # second record - prev must point to index
        prev_fnm = '../index.html'
        prev_link = f"""<a href="{prev_fnm}">←prev</a>"""
        html_bef = html_before.replace('{{PREV_LINK}}', prev_link)
        html_aft = html_after.replace('{{PREV_LINK}}', prev_link)

        next_fnm = all_md_sorted_rev[idx + 1][:-2] + 'html'
        next_link = f"""<a href="{next_fnm}">next→</a>"""
        html_bef = html_bef.replace('{{NEXT_LINK}}', next_link)
        html_aft = html_aft.replace('{{NEXT_LINK}}', next_link)
    if idx >  1 and idx < len(all_md_sorted_rev) - 2: 
        # middle records - process normally
        prev_fnm = all_md_sorted_rev[idx - 1][:-2] + 'html'
        prev_link = f"""<a href="{prev_fnm}">←prev</a>"""
        html_bef = html_before.replace('{{PREV_LINK}}', prev_link)
        html_aft = html_after.replace('{{PREV_LINK}}', prev_link)
        
        next_fnm = all_md_sorted_rev[idx + 1][:-2] + 'html'
        next_link = f"""<a href="{next_fnm}">next→</a>"""
        html_bef = html_bef.replace('{{NEXT_LINK}}', next_link)
        html_aft = html_aft.replace('{{NEXT_LINK}}', next_link)
    if idx == len(all_md_sorted_rev) - 2:
        # last record - next must point to archive
        prev_fnm = all_md_sorted_rev[idx - 1][:-2] + 'html'
        prev_link = f"""<a href="{prev_fnm}">←prev</a>"""
        html_bef = html_before.replace('{{PREV_LINK}}', prev_link)
        html_aft = html_after.replace('{{PREV_LINK}}', prev_link)

        next_fnm = '../archive.html'
        next_link = f"""<a href="{next_fnm}">next→</a>"""
        html_bef = html_bef.replace('{{NEXT_LINK}}', next_link)
        html_aft = html_aft.replace('{{NEXT_LINK}}', next_link)

    html_bef = html_bef.replace('{{PATH_TO_CSS}}', '../' * dir_depth + 'css/styles.css')
    html_bef = html_bef.replace('{{PATH_TO_INDEX}}', '../'  * dir_depth + 'index.html')
    html_bef = html_bef.replace('{{PATH_TO_ARCHIVE}}', '../' * dir_depth + 'archive.html')
    html_bef = html_bef.replace('{{PATH_TO_ABOUT}}', '../' * dir_depth + 'about.html')
    html_bef = html_bef.replace('{{PROJECT_NAME}}', PROJECT_NAME)
    html_bef = html_bef.replace('{{TITLE}}', title)
    html_bef = html_bef.replace('{{AUTHOR}}', AUTHOR)
    html_aft = html_aft.replace('{{COPYRIGHT}}', COPYRIGHT)
    html_aft = html_aft.replace('{{MD_SOURCE}}', '../'  * dir_depth + 'md/' + all_md_sorted_rev[idx])

    if idx == 0:
        f = open('./index.html', 'w')
    else:
        f = open('./html/' + name[:-2] + 'html', 'w')
    
    f.write(html_bef)
    f.write(content)
    f.write(html_aft)
    f.close()
    

def create_archive():
    group = all_md_sorted_rev[0][:4]
    with open('./archive.md', 'w') as f:
        f.write('  * ' + group + '\n')
        for md_file in all_md_sorted_rev:
            if not str(md_file).startswith('.'):
                if group == md_file[:4]:
                    f.write('    * [' + md_file[9:-3].title().replace('-',' ')\
                        + '](../html/' + md_file[0:-2] + 'html)\n')
                else:
                    idx = all_md_sorted_rev.index(md_file)
                    group = all_md_sorted_rev[idx][:4]
                    f.write('  * ' + group + '\n')
                    f.write('    * [' + md_file[9:-3].title().replace('-',' ')\
                        + '](../html/' + md_file[0:-2] + 'html)\n')
    
    with open('./archive.md', 'r') as f:
        content = md.markdown(f.read())
        f.close()

    prev_fnm = './html/' + all_md_sorted_rev[len(all_md_sorted_rev) - 2][:-2] + 'html'
    prev_link = f"""<a href="{prev_fnm}">←prev</a>"""
    html_bef = html_before.replace('{{PREV_LINK}}', prev_link)
    html_aft = html_after.replace('{{PREV_LINK}}', prev_link)
    html_bef = html_bef.replace('{{NEXT_LINK}}', 'next→')
    html_aft = html_aft.replace('{{NEXT_LINK}}', 'next→')
    html_bef = html_bef.replace('{{PATH_TO_CSS}}', './css/styles.css')
    html_bef = html_bef.replace('{{PATH_TO_INDEX}}', './index.html')
    html_bef = html_bef.replace('{{PATH_TO_ARCHIVE}}', './archive.html')
    html_bef = html_bef.replace('{{PATH_TO_ABOUT}}', './about.html')
    html_bef = html_bef.replace('{{PROJECT_NAME}}', PROJECT_NAME)
    html_bef = html_bef.replace('{{TITLE}}', 'Archive')
    html_bef = html_bef.replace('{{AUTHOR}}', AUTHOR)
    html_aft = html_aft.replace('{{COPYRIGHT}}', COPYRIGHT)
    html_aft = html_aft.replace('{{MD_SOURCE}}', './archive.md')

    with open('./archive.html', 'w') as f:
        f.write(html_bef)
        f.write(content)
        f.write(html_aft)  
        f.close()
    
######################################################################    
default_index_md = f"""<p class = "dateline">{TODAY}</p>

#{PROJECT_NAME}

This is a template file generated by {PROJECT_NAME}[1]

  * add your own markdown files to the `./md/` directory of your site
    to begin creating your blog.
    this file will be overwritten automatically as you add your own posts
  * an archive file will be generated each time you build the site
  * an about page is not generated automatically in this release.

[1]: https://github.com/jwhevans/static-purity
"""
######################################################################
default_styles_css = """
* {
    box-sizing: border-box;
}

html {
	font-family: "Helvetica", "Arial", sans-serif;
}

body {
    color: #222;
    line-height: 1.25;
    background-color: #fff;
}

#content {
    max-width: 600px;
    margin: auto;
}

#header {
    font-weight: bold;
    font-size: x-large;
    text-align: center;
    padding: 5px 10px 5px 10px;
}

#header a {
    text-decoration: none;
}

#top-nav, #bottom-nav {
    font-size: small;
    display: flex;
    padding: 5px 10px 5px 10px;
    border-bottom: 1px solid #ddd;
}

.nav-right {
    margin-left: auto;
}

.nav-middle {
	margin-left: auto;
	text-align: center;
}

.dateline {
	font-size: small;
	line-height: 0.25em;
}

#article-content {
    padding: 5px 10px 5px 10px;
}

#footer {
    padding: 10px;
    font-size: small;
}

caption {
    font-style: italic;
    font-size: small;
    color: #555;
}

a:link {
    color: #3A4089;
}

table {
    background-color: #eee;
    padding-left: 2px;
    border: 1px solid #d4d4d4;
    border-collapse: collapse;
}

th {
    background-color: #d4d4d4;
    padding-right: 4px;
}

tr, td, th {
    border: 2px solid #d4d4d4;
    padding-left: 4px;
    padding-right: 4px;
}

dt {
    font-weight: bold;
}

code {
    background-color: #eee;
}

pre {
    background-color: #eee;
    border: 1px solid #ddd;
    padding-left: 6px;
    padding-right: 2px;
    padding-bottom: 5px;
    padding-top: 5px;
}

blockquote {
    padding-top: 2px;
    padding-bottom: 2px;
    padding-left: 16px;
    padding-right: 16px;
}

blockquote code, blockquote pre {
    background-color: #cad2e4;
    border-style: none;
}

h1 {
	font-size: x-large;
	font-style: bold;
}

h2 {
	font-size: large;
	font-style: bold;
}

h1, h2, h3, h4, h5, h6 {
    color: #3A4089;
}

h3, h4, h5, h6 {
    font-style: italic;
} 
"""
# end of defadefault_styles_css
######################################################################
html_before = """\
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" lang="" xml:lang="">
<head>
  <meta charset="utf-8" />
  <meta name="generator" content="{{PROJECT_NAME}}" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
  <meta name="author" content="{{AUTHOR}}" />
  <title>{{PROJECT_NAME}} - {{TITLE}}</title>
  <link rel="stylesheet" href="{{PATH_TO_CSS}}" />
</head>
<body>

<div id="content">

<div id="header"><a href="{{PATH_TO_INDEX}}">mnml.blog</a></div>

<div id="article-box">


<div id="top-nav">
  <div>{{PREV_LINK}}</div>
    <div class="nav-middle">
      <a href="{{PATH_TO_ABOUT}}">about</a> | <a href="{{PATH_TO_ARCHIVE}}">archive</a>
    </div> <!-- nav-middle -->
  <div class="nav-right">{{NEXT_LINK}}</div>
</div> <!-- top-nav -->

<div id=article-content">
""" 
# end of html_before
######################################################################
html_after = """
</div> <!-- article-content -->

<div id="bottom-nav">
  <div>{{PREV_LINK}}</div>
  <div class="nav-right">{{NEXT_LINK}}</a></div>
</div> <!-- bottom-nav -->

</div> <!-- article-box -->

<div id="footer">
{{COPYRIGHT}}
<a href="{{MD_SOURCE}}">Markdown source for this page</a><br/>
(Site generated by 
<a href="https://github.com/jwhevans/static-purity">Static-Purity</a>)
</div> <!-- footer -->

</div> <!-- content -->

</body>
</html>
""" 
# end of html_after
######################################################################
main()