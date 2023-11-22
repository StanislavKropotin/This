import scrapy


class Spider(scrapy.Spider):
    name = 'spider'
    start_urls = ['https://naked-science.ru/',
                  'https://nplus1.ru/',
                  'https://newatlas.com/']

    def parse(self, response):
        print("Парсинг прошёл успешно!\n" + response.url)
        naked_n = response.xpath("//div[@class='news-item-excerpt']/p").extract()
        n_plus = response.xpath(
            "//a[@class='n1_climb_4 transition-colors duration-75 hover:text-main inline-block mb-10 sm:mb-5 font-spectral leading-24']/div/text()").extract()
        n_atlas = response.xpath("//div[@class='PromoB-description']/text()").extract()
        n_atlas_2 = response.xpath("//div[@class='PromoC-description']/text()").extract()
        row_data = zip(naked_n)
        row_data_2 = zip(n_plus)
        row_data_3 = zip(n_atlas)
        row_data_4 = zip(n_atlas_2)

        for n in row_data:
            scraped_info = {
                'page': response.url,
                'post': n[0].replace("<p>", "").replace("</p>", "").replace(" ", "")
            }
            yield scraped_info

        for p in row_data_2:
            scraped_info_2 = {
                'page': response.url,
                'post': p[0].replace(" ", " ").replace("<div>", "").replace("</div>", "").replace("<div class=""text-main-gray"">", "")
            }
            yield scraped_info_2

        for n_a in row_data_3:
            scraped_info_3 = {
                'page': response.url,
                'post': n_a[0]
            }
            yield scraped_info_3

        for n_a_2 in row_data_4:
            scraped_info_4 = {
                'page': response.url,
                'post': n_a_2[0]
            }
            yield scraped_info_4

            NEXT_PAGE_SELECTOR = '.ui-pagination-active + a::attr(href)'
            next_page = response.xpath(NEXT_PAGE_SELECTOR).extract()
            if next_page:
                yield scrapy.Request(
                    response.urljoin(next_page),
                    callback=self.parse)

