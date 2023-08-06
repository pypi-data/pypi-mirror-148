# xpe

*Finally, a commandline xpath tool that is easy to use.*

***What is this?***

xpe is a commandline xpath parser. Pipe in some textual data, supply it with an xpath expression, and it will dump the result to stdout. Perfect for shellscripting. For example:
    
    curl -sL github.com | xpe "//meta[@name='twitter:title']"

    GitHub: Where the world builds software
    
Alternatively, xpe can query a file for xpath expressions like so:

    xpe '//a/@href' somefile.htm

The order doesn't matter, so the following is also valid:

    xpe somefile.htm '//a/@href'
