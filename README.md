# PythonStaticSiteGenerator

### Description
> Simple Python 3.10 Webserver for static pages written in Markdown.

### Disclaimer
***This is not production ready software, use at your own peril.***
This project was made as an exercise/required project for the [boot.dev](https://www.boot.dev) course entitled "Build a Static Site Generator". This is not production ready/production optimized code. I do not recommend using it at all.

### Architecture

![Image of the architecture, a complete description is written below](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/UKCNg8E.png)

The flow of data through the full system is:

1. Markdown files are in the `/content` directory. A `template.html` file is in the root of the project.
2. The static site generator (the Python code in `src/`) reads the Markdown files and the template file.
3. The generator converts the Markdown files to a final HTML file for each page and writes them to the `/public` directory.
4. We start the built-in Python HTTP server for delivering the contents of the `/public` directory on `http://localhost:8888` (our local machine).
5. We open a browser and navigate to `http://localhost:8888` to view the Markdown file turned http and served to our browser

#### How the SSG will work

The vast majority of our code will reside in the `src/` directory because almost all of the work is done in steps 2 and 3 above. Here's a rough outline of what the final program will do when it runs:

**Initialization**
After starting the Python script:
1. Delete everything in the `/public` directory.
2. Copy any static assets (HTML template, images, CSS, etc.) to the `/public` directory.
3. Generate an HTML file for each Markdown file in the `/content` directory.

**Markdown to HTML Conversion**
For each file in the `/content` directory:
1. Open the file and read its contents.
2. Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
3. Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
            `Raw markdown -> TextNode -> HTMLNode`
4. Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
5. Use a recursive `to_html()` method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
6. Write the full HTML string to a file for that page in the `/public` directory.

### Project objective
The objective of this program is to put into practice *functional programing* to a certain extent.
