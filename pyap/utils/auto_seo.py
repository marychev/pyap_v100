class AutoSeo(object):
    """Автоматическое заполнение сео полей"""
    def __init__(self, page, title):
        self.title = title
        self.page = page

    def default(self):
        if not self.page.seo_title:
            self.page.seo_title = self.title
        if not self.page.seo_description:
            self.page.seo_description = self.title
        if not self.page.seo_keywords:
            self.page.seo_keywords = self.title

