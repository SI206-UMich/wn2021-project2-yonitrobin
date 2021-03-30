from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    #open 
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filename), 'r') as f:
        url = f.read()

    #soup objects
    soup = BeautifulSoup(url, 'html.parser')
    book_titles = soup.find_all('a', class_ = 'bookTitle')
    authors = soup.find_all('div', class_ = 'authorName__container')
   
    #list of authors
    author_names = []
    for author in authors:
        author_names.append(author.text.split("'")[0])

    #list of books
    books = []
    for book in book_titles:
        books.append(book.text.strip())
        
    #make list of tuples by looping thru length
    results = [(books[i], author_names[i]) for i in range(len(books))]
    return results
    
    
def get_search_links():
    
    #create bs object
    url = 'https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = soup.find_all('a', class_ = 'bookTitle', itemprop = 'url')
    
    #list of urls
    links = []

    #parse through the object
    for tag in tags:
        t = tag['href']
        if t.startswith('/book/show/'):
            sites = 'https://www.goodreads.com' + str(t)
            links.append(sites)
    return links[:10]

    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

def get_book_summary(book_url):
    #create bs object
    resp = requests.get(book_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
   
    #book title
    title = soup.find('h1', class_ = 'gr-h1--serif')
    title_text = title.text.strip()

    #num pages
    pages = soup.find('span', itemprop = 'numberOfPages')
    pages_text = pages.text.split()
    pages_num = int(pages_text[0])

    #author
    author = soup.find('span', itemprop = 'name')
    author_text = author.text.strip()
    bookInfo = (title_text, author_text, pages_num)
    
    return bookInfo

    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    #open
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), filepath), 'r') as f:
        url = f.read()
    
    #bs objects
    soup = BeautifulSoup(url, 'html.parser')
    categories = soup.find_all('h4', class_ = 'category__copy')
    titles = soup.find_all('div', class_ = 'category__winnerImageContainer')
    urls = soup.find_all('div', class_ = 'category clearFix')

    category_lst = []
    for cat in categories:
        category_lst.append(cat.text.strip())
    
    titles_lst = []
    for title in titles:
        name = title.find('img')['alt']
        titles_lst.append(name)
    
    url_lst = []
    for url in urls:
        link = url.find('a')['href']
        url_lst.append(link)
    
    

    best_books = [(category_lst[i], titles_lst[i], url_lst[i]) for i in range(len(titles_lst))]
    return best_books



def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """

    with open(filename, 'w') as f:
        write = csv.writer(f)
        write.writerow(('Book Title', 'Author Name'))
        write.writerows(data)
    


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    '''def test_get_titles_from_search_results(self):

        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results_var = get_titles_from_search_results('search_results.htm')
        
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual((len(results_var)), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual((type(results_var)), list)

        # check that each item in the list is a tuple
        for item in results_var:
            self.assertEqual(type(item), tuple)
        
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(results_var[0],('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling') )
        
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(results_var[-1],('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling') )

        
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls), list)

        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls), 10)


        # check that each URL in the TestCases.search_urls is a string
        for i in TestCases.search_urls:
            self.assertEqual(type(i), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        # for each URL in TestCases.search_urls (should be a list of tuples)
        for i in TestCases.search_urls:
            summaries.append(get_book_summary(i))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)

        for i in summaries:     
            # check that each item in the list is a tuple
            self.assertEqual(type(i), tuple)

            # check that each tuple has 3 elements
            self.assertEqual(len(i), 3)

            # check that the first two elements in the tuple are string
            self.assertEqual(type(i[0]), str)
            self.assertEqual(type(i[1]), str)

            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(i[2]), int)

            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)
        

   def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books('best_books_2020.htm')

        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)
            # assert each item in the list of best books is a tuple
        for i in best_books:
            self.assertEqual(type(i), tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(i), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))
    '''
    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        writer_var = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(writer_var, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r', newline = '') as f:
            read_csv = csv.reader(f)
            csv_lines = []
            for i in read_csv:
                csv_lines.append(i)


        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)

        # check that the header row is correct
        self.assertEqual(csv_lines[0], ['Book Title', 'Author Name']

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1],('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(csv_lines[-1],('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)



