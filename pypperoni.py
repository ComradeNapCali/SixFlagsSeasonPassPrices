import argparse, sys, glob
from pypperoni.cmake import CMakeFileGenerator

PYTHON_PATH = sys.executable.replace('\\', '/').rsplit('/', 1)[0]
SITE_PKGS = PYTHON_PATH + '/Lib/site-packages/'

parser = argparse.ArgumentParser()
parser.add_argument('--nthreads', '-t', type=int, default=4,
                    help='Number of threads to use')
args = parser.parse_args()

c = CMakeFileGenerator('SixFlagsSeasonPassPrices', outputdir='build', nthreads=args.nthreads)
c.add_file('scrap.py')
c.add_file('markdown_generator.py')
c.add_file(SITE_PKGS + 'appdirs.py', name='appdirs')
c.add_tree(SITE_PKGS + 'bs4')
c.add_tree(SITE_PKGS + 'certifi')
c.add_tree(SITE_PKGS + 'chardet')
c.add_tree(SITE_PKGS + 'cssselect')
c.add_tree(SITE_PKGS + 'fake-useragent')
c.add_tree(SITE_PKGS + 'idna')
c.add_file(SITE_PKGS + 'parse.py', name='parse')
c.add_tree(SITE_PKGS + 'pyee')
c.add_tree(SITE_PKGS + 'pyppeteer')
c.add_tree(SITE_PKGS + 'pyquery')
c.add_tree(SITE_PKGS + 'requests')
c.add_file(SITE_PKGS + 'requests_html.py', name='requests_html')
c.add_tree(SITE_PKGS + 'six')
c.add_tree(SITE_PKGS + 'soupsieve')
c.add_tree(SITE_PKGS + 'tqdm')
c.add_tree(SITE_PKGS + 'urllib3')
c.add_tree(SITE_PKGS + 'w3lib')
c.add_tree(SITE_PKGS + 'websockets')
c.modules['scrap'].set_as_main()
c.run()