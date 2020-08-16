import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = ["http://books.toscrape.com/"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):


        with open("books3.csv","a") as file:
            #file.write("image_url,book_title,product_price\n")
            books=response.css("article.product_pod")
            for book in books:
                title='"'+book.css("h3 a").attrib["title"]+'"'
                #title='"'+book.css("h3 a::text").get()+'"'
                prices=book.css("div.product_price p.price_color::text").get()
                image_url=book.css("a img").attrib["src"]

                file.write(image_url+","+title+",Â"+prices+"\n")
            next_page = response.css('li.next a::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
