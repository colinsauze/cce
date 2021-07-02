~~~
1 + 1
~~~
{:.language-python}
Lorem ipsum
~~~
1 + 2 + 3
2 + 5
~~~
{:.language-python}
something with output
~~~
5 + 6
~~~
{: .language-python}
~~~
11
~~~
{: .output}
dolor sit amet.
~~~
import pytest_codeblocks

pytest_codeblocks.extract_from_buffer
~~~
{:.language-python}
Something that should be skipped because of the language:
~~~
foobar
~~~
{:.language-ruby}
A shell script should be exectuted:
```sh
echo abc
```
Again with an explicit skip:
<!--pytest-codeblocks:skip-->
~~~
bar
~~~
{:.language-python}

Something that contains triple fences
~~~
# ~~~
# import math~~~
~~~
{:.language-python}

Indented code blocks:
  ~~~
  1 + 1 == 2
  ~~~
{:.language-python}

"Wrong" indentation:
~~~
3 + 4 == 7
  ~~~
{:.language-python}
