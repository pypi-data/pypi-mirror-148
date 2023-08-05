from urllib.parse import quote, unquote

url = 'http://github.com/Krtura/swift'

print(quote(url, safe=''))
print(unquote('http%3A%2F%2Fgithub.com%2FKrtura%2Fswift'))

from html import escape, unescape

# print(escape('<script>alert("abc")</script>')) # correct

# print(unescape('&lt;script&gt;alert(&quot;abc&quot;)&lt;/script&gt;')) # correct