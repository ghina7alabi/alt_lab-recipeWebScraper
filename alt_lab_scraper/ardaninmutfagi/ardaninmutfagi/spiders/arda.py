# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from ..items import *

class ArdaSpider(scrapy.Spider):
    name = 'arda'
    allowed_domains = ['ardaninmutfagi.com']
    start_urls = ['http://ardaninmutfagi.com/']

    def start_requests(self):
        start_url = 'https://www.ardaninmutfagi.com/category/yemek-tarifleri/page/'
        max_pages = 2

        for page in range(max_pages):
            yield scrapy.Request(url=start_url + str(page+1), callback=self.parse)


    def parse(self, response):
        raw = response.body
        soup = BeautifulSoup(raw, 'html.parser')

        items = soup.select('.icerik-card-box')

        for item in items:
            item = item.select_one('a')

            print('------------------------------')
            print(item['href'])
            new_url = item['href']
            yield scrapy.Request(url=new_url, callback=self.recipe_parse)

    def recipe_parse(self, response):

        recipe_item = RecipeItem()

        raw = response.body
        soup = BeautifulSoup(raw, 'html.parser')

        url = response.url

        title = soup.select_one('.entry-title').text

        ingredients = soup.select_one('.mlz').text.strip()
        ingredients = ingredients.split('\n')

        recipe = []
        content = soup.select('.entry-content p')

        for items in content:
            items = items.text.strip().split('\n')
            recipe.append(items)

        recipe_item['title'] = title
        recipe_item['url'] = url
        recipe_item['ingredients'] = ingredients
        recipe_item['recipe'] = recipe

        yield recipe_item
