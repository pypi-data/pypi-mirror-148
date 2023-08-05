import asyncio
from requests_html import HTMLSession, AsyncHTMLSession
from functools import partial
from .page_iterators import *
from .zhihu_types import *
from .extractors import extract_data, extract_user, extract_question_data
from ..utils import get_useragent, get_headers, get_proxy
import itertools
from loguru import logger
import json
import time


class ZhiHuScraper:
    """
    知乎采集
    """
    default_headers = {
        # 'connection': 'close',
        "user-agent": get_useragent()
    }

    def __init__(self, session=None, async_session=None, requests_kwargs=None):
        if session is None:
            session = HTMLSession()
            session.headers.update(self.default_headers)
        if requests_kwargs is None:
            requests_kwargs = {}
        if async_session is None:
            async_session = AsyncHTMLSession(workers=ASYNC_COUNT)
            async_session.headers.update(self.default_headers)
        self.async_session = async_session
        self.session = session
        self.requests_kwargs = requests_kwargs

    def set_proxy(self, proxy: Optional[Dict[str, str]] = None):
        """
        设置代理
        :param proxy: proxy = {'http': 'http://ip:port', 'https': 'http://ip:port'}
        :return:
        """
        proxies = {
            'proxies': proxy
        }
        self.requests_kwargs.update(proxies)

    def set_timeout(self, timeout: int):
        """
        设置请求超时 单位秒
        """
        self.requests_kwargs['timeout'] = timeout

    def search_crawler(self, key_word: Union[str], **kwargs) -> Union[Iterator[ArticleType],
                                                                      Iterator[AnswerType],
                                                                      Iterator[VideoType]]:
        """
        通过关键词对检索结果进行采集
        :param key_word: 需要采集的关键词
        :return:
        """
        kwargs['scraper'] = self
        iter_search_pages_fn = partial(iter_search_pages, key_word=key_word, request_fn=self.send, **kwargs)
        return self._generic_crawler(extract_data, iter_search_pages_fn, **kwargs)

    def top_search_crawler(self, top_search_url, **kwargs) -> Keyword:
        response = self.send(top_search_url)
        data = json.loads(response.text)
        keywords = []
        for info in data.get('top_search', {}).get('words', []):
            keywords.append(info.get('query', ''))
        del response, data
        return {
            'keywords': keywords
        }

    def question_crawler(self, question_id: Union[str], **kwargs) -> Iterator[QuestionType]:
        """
        通过问题id采集
        """
        kwargs['scraper'] = self
        iter_question_pages_fn = partial(iter_question_pages, question_id=question_id, request_fn=self.send, **kwargs)
        kwargs['total_count'] = kwargs.get('drill_down_count', 0)
        return self._generic_crawler(extract_data, iter_question_pages_fn, **kwargs)

    def article_crawler(self, article_id: Union[str], **kwargs) -> Iterator[ArticleType]:
        """
        通过文章id采集文章页数据
        """
        kwargs['scraper'] = self
        iter_article_pages_fn = partial(iter_article_pages, article_id=article_id, request_fn=self.send, **kwargs)
        return self._generic_crawler(extract_data, iter_article_pages_fn, **kwargs)

    def video_crawler(self, video_id: Union[str], **kwargs) -> Iterator[VideoType]:
        """
        通过视频id采集视频页数据
        """
        kwargs['scraper'] = self
        iter_video_pages_fn = partial(iter_video_pages, video_id=video_id, request_fn=self.send, **kwargs)
        return self._generic_crawler(extract_data, iter_video_pages_fn, **kwargs)

    def user_crawler(self, user_id: Union[str], **kwargs) -> Iterator[UserType]:
        """
        通过账号id采集个人主页数据
        """
        kwargs['scraper'] = self
        iter_user_page_fn = partial(iter_user_pages, user_id=user_id, request_fn=self.send, **kwargs)
        return self._generic_crawler(extract_user, iter_user_page_fn, **kwargs)

    def hot_list_crawler(self, **kwargs) -> Iterator[QuestionType]:
        """
        首页热榜采集
        """
        kwargs['scraper'] = self
        iter_hot_page_fn = partial(iter_hot_list_pages, request_fn=self.send, **kwargs)
        return self._generic_crawler(extract_question_data, iter_hot_page_fn, **kwargs)

    def hot_question_crawler(self, domains, **kwargs) -> Iterator[QuestionType]:
        """
        热点问题采集
        """
        kwargs['scraper'] = self
        kwargs['total_count'] = kwargs.pop('question_count', 0)
        for domain in domains:
            iter_hot_question_page_fn = partial(iter_hot_question_pages, domain=domain, request_fn=self.send, **kwargs)
            for result in self._generic_crawler(extract_question_data, iter_hot_question_page_fn, **kwargs):
                yield result

    def send(self, url, **kwargs):
        if not url:
            logger.error('url is null')
        method = kwargs.get('method', 'GET')
        return self.post(url, **kwargs) if method == 'POST' else self.get(url, **kwargs)

    def get(self, url, **kwargs):
        """
        请求方法，在该方法中进行x_zse_96参数加密
        @ x_zse_96: 是否需要x_zse_96参数加密
        """
        assert url is not None, 'url is null'
        x_zse_96 = kwargs.get('x_zse_96', False)
        d_c0 = re.sub('d_c0=|;.*', '', self.default_headers.get('cookie', '')) or ''
        kwargs['d_c0'] = d_c0
        if isinstance(url, str):
            if x_zse_96:
                self.default_headers.update(get_headers(url, d_c0) or {})
            self.session.headers.update(self.default_headers)
            retry_limit = 6
            response = None
            for retry in range(1, retry_limit + 1):
                try:
                    response = self.session.get(url, **self.requests_kwargs)
                    response.raise_for_status()
                    return response
                except Exception as e:
                    if retry < retry_limit:
                        sleep_time = retry * 2
                        logger.debug(f'重连第{retry}次，休眠{sleep_time}秒, 异常：{e}')
                        time.sleep(sleep_time)
                        # 重新获取代理
                        # proxies = {'http': get_proxy(), 'https': get_proxy()}
            assert response is not None, f'重新请求{retry_limit}次， response为空'
        if isinstance(url, list):  # 使用协程请求
            return self.generic_response(url, **kwargs)

    def generic_response(self, urls, **kwargs):
        urls = [urls[i: i + ASYNC_COUNT] for i in range(0, len(urls), ASYNC_COUNT)]
        for sub_urls in urls:
            tasks = [lambda url=url: self.async_get(url, **kwargs) for url in sub_urls]
            results = self.async_session.run(*tasks)
            yield results

    async def async_get(self, url, **kwargs):
        if kwargs.get('x_zse_96', False):
            self.default_headers.update(get_headers(url, kwargs.get('d_c0')) or {})
        self.async_session.headers.update(self.default_headers)
        response = await self.async_session.get(url, **self.requests_kwargs)
        if response and response.status_code != 200:
            logger.error(f'request url: {url}, response code: {response.status_code}')
        await asyncio.sleep(2)
        return response

    def post(self, url, **kwargs):
        pass

    def _generic_crawler(self,
                         extract_fn,
                         iter_pages_fn,
                         options=None,
                         **kwargs):
        """
        中转函数
        @extract_fn 数据清洗方法
        @iter_pages_fn 页面处理方法
        @options 参数
        """
        page_limit = kwargs.get('page_limit') if kwargs.get('page_limit', 0) else DEFAULT_PAGE_LIMIT
        counter = itertools.count(0) if page_limit is None else range(page_limit)
        if options is None:
            options = {}
        elif isinstance(options, set):
            options = {k: True for k in options}
        total_count = kwargs.get('total_count', 0)
        count = 0
        for i, page in zip(counter, iter_pages_fn()):
            for element in page:
                if 0 < total_count <= count:
                    return None
                count += 1
                info = extract_fn(element, options=options, request_fn=self.send)
                yield info