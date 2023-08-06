# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_rtfm']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'algoliasearch>=2.6.1,<3.0.0',
 'async-timeout>=4.0.2,<5.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-rtfm',
    'version': '0.2.0',
    'description': 'A plugin for searching docs in QQ, use NoneBot and OneBot V11',
    'long_description': '<p align="center">\n  <img src="https://s2.loli.net/2022/05/01/fbZuQPidkqt6vjp.png">\n</p>\n\n<div align="center">\n\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable-next-line MD036 -->\n\n# nonebot-plugin-rtfm\n\n_✨ NoneBot2 文档搜索插件 ✨_\n<!-- prettier-ignore-end -->\n\n</div>\n\n## 🚀安装\n\n此插件需要 **Python 3.8 及以上**\n\n```bash\n# 通过 nb-cli\nnb plugin install nonebot-plugin-rtfm\n# 通过 poetry\npoetry add nonebot_plugin_rtfm\n# 通过 pip\npip install nonebot_plugin_rtfm\n```\n\n## 📝命令\n\n### /rtfm [关键词]\n\n#### 概述\n\n若提供了关键词，则根据关键词进行搜索 NoneBot2 文档，否则进入对话模式获取关键词后搜索\n\n#### 例子\n\n<details>\n<summary>图片</summary>\n\n![-ff3a75dd1b3b136.png](https://s2.loli.net/2022/04/26/jBCWS9Z6NvdTJeA.png)\n\n</details>\n\n### /obrtfm [关键词]\n\n#### 概述\n\n若提供了关键词，则根据关键词进行搜索 OneBot 适配器 文档，否则进入对话模式获取关键词后搜索\n\n#### 例子\n\n<details>\n<summary>图片</summary>\n\n![-736fa5bfcf4805f2.png](https://s2.loli.net/2022/04/26/Tsn8QrWvODygqwI.png)\n\n</details>\n\n### /插件列表\n\n#### 概述\n\n获取商店里的全部插件的简要信息，支持 `/page` 和 `戳一戳`\n\n#### 例子\n\n<details>\n<summary>图片</summary>\n\n![_J_T~YS6NJDRF61__6_8M~4.png](https://s2.loli.net/2022/04/27/lmLwqRY86yesfAM.png)\n\n</details>\n\n### /搜索插件 <关键字> [-t] [-n] [-a] [-d] [-p=[0-1]]\n\n**WIP：此功能尚未完成**\n\n#### 概述\n\n搜索插件列表的插件，支持 `/page` 和 `戳一戳`\n\n#### 参数\n\n- `-t`，`--without_tag` 查询时不使用标签查询\n- `-n`，`--without_name` 查询时不使用插件名称查询\n- `-a`，`--without_author` 查询时不使用作者名查询\n- `-d`，`--without_desc` 查询时不使用描述查询\n- `-p=[0-1]`，`--percent=[0-1]` 相似度，越接近1相似度越高\n\n### /page <页码>\n\n#### 概述\n\n查看指定页的文档，来源根据上一次的查询结果的缓存\n\n#### 例子\n\n<details>\n<summary>图片</summary>\n\n![1650986335404.png](https://s2.loli.net/2022/04/26/vrdhkiVnTs1w37K.png)\n\n</details>\n\n#### 使用戳一戳\n\n戳机器人会发送下一页文档\n\n<details>\n<summary>图片</summary>\n\n![1650986464565.png](https://s2.loli.net/2022/04/26/QWH1ul72O9MGqZm.png)\n\n</details>\n\n## 🔧配置\n\n- rtfm_page\n  - 设置一条消息的结果数（默认：5）\n- use_proxy\n  - 使用 `jsdelivr` 源获取插件信息（默认：True）\n\n## 🚧预期加入功能\n\n- [ ] Python 文档查询\n- [ ] 插件文档查询（基于 [`nonebot-plugin-help`](https://github.com/XZhouQD/nonebot-plugin-help) 的文档接入方式）\n- [ ] 图片生成（预期使用 [`nonebot-plugin-htmlrender`](https://github.com/kexue-z/nonebot-plugin-htmlrender)或 `PIL`）\n- [ ] _More..._\n\n## 🐛Bug 反馈或提交建议\n\n请通过 [Issue](https://github.com/MingxuanGame/nonebot-plugin-rtfm/issues) 向我反馈 Bug 或提交建议\n\n## 👥参与开发\n\n_待补充_\n\n## 🔒️许可\n\n本插件使用 [MIT 许可证](https://github.com/MingxuanGame/nonebot-plugin-rtfm/blob/master/LICENSE) 开源\n\n```\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS\nFOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER\nIN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN\nCONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n```\n',
    'author': 'MingxuanGame',
    'author_email': 'MingxuanGame@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MingxuanGame/nonebot-plugin-rtfm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
