from . import State
import string
import re
from urllib.request import urlopen

class CodeBlock(State):
    def __init__(self):
        self.name = 'CodeBlock'
        super().__init__()
        self.valid_language_chars = list(string.ascii_lowercase)
        self.direct_pattern = r'^```[a-z]+\n$'

    def _is_direct(self, stack):
        tokens = stack.peek(n=3)
        opening = ''.join([t.value for t in tokens])
        return re.match(self.direct_pattern, opening)

    def _parse_direct(self, stack):
        stack.pop() # drop opening ```
        language = stack.pop().value
        # todo: a second language specific parse to break up the code into elements
        tokens = stack.seek_until(lambda tok: tok.value.startswith('```'), include_last=False)
        stack.pop() # drop closing ```
        inner = ''.join([t.value for t in tokens])
        return self.finalize(inner, language=language)

    def finalize(self, inner, language=None):
        self.buffer += f"<pre class=\"code_block\"><code class=\"{language}\">"
        self.buffer += inner
        self.buffer += '</code></pre>'
        return self.buffer

    def parse(self, stack):
        if self._is_direct(stack):
            return self._parse_direct(stack)

        #todo: support gist links
        raise Exception(
            'Code block must start with ``` and specify language ending in newline.')