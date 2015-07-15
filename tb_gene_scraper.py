from lxml import html
import urllib2
import sys


if len(sys.argv) != 2:
    print "Syntax: python tb_gene_scraper.py GENE_NAME" 
    exit(1)

intro = """A tiny scraper for the tuberculist website.
If the gene has a name ending in '_promoter' it will be removed
and the 100bp BEFORE the gene will be downloaded instead.\n"""

sys.stderr.write(intro)

name = sys.argv[1]
promoter = False
if name.endswith("_promoter"):
    promoter = True
    name = name.replace("_promoter", "")


url = "http://tuberculist.epfl.ch/quicksearch.php?" \
        "gene+name=%s&submit=Search" % name
sys.stderr.write(url + "\n")

response = urllib2.urlopen(url)
tree = html.fromstring(response.read())

gene = tree.xpath("//input[@name='gene']/@value")[0]
start = tree.xpath("//input[@name='start']/@value")[0]
end = tree.xpath("//input[@name='end']/@value")[0]
direction = urllib2.quote(tree.xpath("//input[@name='direction']/@value")[0])

if promoter:
    temp = start
    start = str(int(start) - 100)
    end = temp

url = "http://tuberculist.epfl.ch/dnaseq.php?" \
        "bp=&gene=%s&start=%s&end=%s&direction=%s&submit=View" % (
                gene, start, end, direction
        )

sys.stderr.write(url + "\n")
response = urllib2.urlopen(url)
tree = html.fromstring(response.read())
sequence = ''.join(tree.xpath("//font[@color='black']/text()"))
print ">" + sys.argv[1]
print sequence

