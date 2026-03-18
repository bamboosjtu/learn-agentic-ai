# crawl4ai 示例

这个目录包含一组实践代码和资料，用于学习如何使用 [crawl4ai](https://pypi.org/project/crawl4ai/)。它是一个现代的、AI 驱动的 Python 网页爬虫工具。

## 什么是 crawl4ai？

crawl4ai 是一个强大、灵活、智能的网页抓取库，专为大规模数据提取而设计。它支持与 LLM 集成，具备高级反爬能力，既适合简单抓取任务，也适合更复杂的网页采集场景。

## 官方资源与文档

- [官方网站](https://crawl4ai.com/)
- [GitHub 仓库](https://github.com/unclecode/crawl4ai)
- [PyPI: crawl4ai](https://pypi.org/project/crawl4ai/)
- [YouTube 教程](https://youtu.be/xo3qK6Hg9AA)

## 推荐视频

- [Crawl4AI Tutorial 1](https://www.youtube.com/watch?v=lpOb1bQO7aM)
- [Crawl4AI Tutorial 2](https://www.youtube.com/watch?v=Osl4NgAXvRk)

## 示例脚本

- [simple_crawling.py](./simple_crawling.py)：抓取单个页面并打印 Markdown 内容
- [custom_crawl_options.py](./custom_crawl_options.py)：自定义抓取选项（内容过滤、标签排除、iframe 等）
- [error_handling.py](./error_handling.py)：优雅处理抓取失败
- [deep_crawling.py](./deep_crawling.py)：使用 BFS 策略做深度抓取，并打印 URL 与深度
- [bestfirst_crawling.py](./bestfirst_crawling.py)：结合 `BestFirstCrawlingStrategy` 和 `KeywordRelevanceScorer` 的优先级抓取
- [llm_integration.py](./llm_integration.py)：LLM 驱动信息提取的模板（按需改成自己的 LLM 配置）
- [proxy_usage.py](./proxy_usage.py)：使用代理绕过部分反爬限制
- [multi_url_crawling.py](./multi_url_crawling.py)：按顺序抓取多个 URL
- [config_examples.py](./config_examples.py)：演示 `BrowserConfig`、`CrawlerRunConfig` 和 `LLMConfig`
- [deep_crawl_to_files.py](./deep_crawl_to_files.py)：深度抓取网站，并把每个 URL 的 Markdown 保存到 `data/crawlers`，同时生成一个汇总 JSON 文件

> **欢迎贡献！** 你也可以把自己的示例和经验补充进来，帮助其他人更快学会 crawl4ai。
