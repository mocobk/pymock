# py-mock
![](https://shields.mitmproxy.org/pypi/v/py-mock.svg)
![](https://shields.mitmproxy.org/pypi/pyversions/py-mock.svg)

```shell
pip install py-mock
```
## py-mock 介绍

`py-mock` 移植了 [Mock.js](https://github.com/nuysoft/Mock
)、[better-mock](https://github.com/lavyun/better-mock)的功能到 Python，如果你熟悉 Mock
.js 的[模板语法](http://mockjs.com/examples.html)， 那么在 Python 中也能轻而易举地 Mock
 出你想要的数据，`py-mock` `100%` 兼容 Mock.js。

## 一些说明
实际上 `py-mock` 是借助了 `py_mini_racer` 来运行 Mock.js 中的 mock 函数，且仅移植了 Mock.mock
 方法，如果有问题可以在 github 上给我提 issue。

## 使用示例

```python
from pprint import pprint

from pymock import Mock

Mock = Mock()

pprint(Mock.mock('@csentence 变量示例'))
```
```
'何思许型面率儿相算加阶角难角看有资。 变量示例'
```

```python
pprint(Mock.mock({
    'list|1-10': [{
        'id|+1': 1,
        'email': '@EMAIL'
    }]
}))
```
```
{'list': [{'email': 'n.metv@mddwjpjxo.cf', 'id': 1},
          {'email': 'e.vseuqc@viiuxwde.biz', 'id': 2},
          {'email': 'v.eoje@mklgh.ba', 'id': 3},
          {'email': 'm.xobzjwhegf@hsclkd.uk', 'id': 4}]}
```

```python
pprint(Mock.mock(Mock.mock({
    'number1|1-100.1-10': 1,
    'number2|123.1-10': 1,
    'number3|123.3': 1,
    'number4|123.10': 1.123
})))
```
```
{'number1': 56.5787,
 'number2': 123.14013355,
 'number3': 123.695,
 'number4': 123.1236478526}
```

```python
pprint(Mock.mock({
    'regexp1': r'/[a-z][A-Z][0-9]/',
    'regexp2': r'/\w\W\s\S\d\D/',
    'regexp3': r'/\d{5,10}/',
    'regexp4': r'\/\d{5,10}\/'  # output raw regexp with escape slash
}))
```
```
{'regexp1': 'xP9',
 'regexp2': 'B \xa0V7O',
 'regexp3': '98356203',
 'regexp4': '/\\d{5,10}/'}
```

```python
pprint(Mock.mock({
        'name': {
            'first': '@first',
            'middle': '@first',
            'last': '@last',
            'email': 'example\\@gmail.com',
            'full': '@first @middle @last'
        }
    }
))
```
```
{'name': {'email': 'example@gmail.com',
          'first': 'Nancy',
          'full': 'Nancy Nancy Lee',
          'last': 'Lee',
          'middle': 'Nancy'}}
```

```python
pprint(Mock.mock({
    'random': {
        'name': [
            '@name',
            '@cname'
        ],
        'image': [
            # @image( size, background, foreground, format, text )
            "@image",
            "@image('300x400')",
            "@image('300x400', '占位图文字')",
            "@image('300x400', '#234567', '#FFFFFF', 'png', 'HelloWorld')"
        ],
        'emoji': [
            # emoji( pool, min, max )
            "@emoji",
            "@emoji('😀😁😂😃😄')",
            "@emoji(3, 6)",
            "@emoji('123🌘😷🙊★♠♫', 3, 6)"
        ]
    }
}
))
```
```
{'random': {'emoji': ['🌛', '😀', '👲🌐👧🍢🌂🐁', '♫1★🙊'],
            'image': ['https://iph.href.lu/400x300?bg=&fg=&text=',
                      'https://iph.href.lu/300x400?bg=&fg=&text=',
                      'https://iph.href.lu/300x400?bg=&fg=&text=占位图文字',
                      'https://dummyimage.com/300x400/234567/FFFFFF.png?text=HelloWorld'],
            'name': ['Mary Thompson', '高刚']}}
```

You can also Mock form JSON string or JavaScript Object like-string
```python
pprint(Mock.mock_js("""
{
    name: {
        first: "@cfirst", 
        last: "@clast",
        name: "@first@last",
    }
}
"""))
```

```
{'name': {'first': '卢', 'last': '强', 'name': '卢强'}}
```

[更多示例](http://mockjs.com/examples.html)
