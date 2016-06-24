from prompt_toolkit.completion import Completer, Completion
import shlex
import re


class OptLiveCompleter(Completer):

    def __init__(self, opts_dict, dynamic):
        """
        @params opts_dict: should be something like
        ```
        {"ls": {"args": ["tags"], # positional options
                "opts": ["--help", "-h", ....]} # options
         ...
        }
        ```

        @params dynamic: a linked object to some dynamic values like
        ```
        {"tags": ["value1" ...]}
        ```

        when a command is issued, it will try to locate all the completion
        possiblities. For positional option, we build it from dynamic value so
        what is set in "args" can be read from param dynamic. Completion values
        then become the combination of `opts` and dynamic `args`
        """

        self.opts_dict = opts_dict
        self.dynamic = dynamic

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # when started with just spaces, do nothing
        if re.match(r"^\s+$", text):
            pass
        else:
            opts = shlex.split(text)
            # opts[0] is cmd
            dy = self.dynamic

            if len(opts) == 1:
                for i in self.opts_dict:
                    if i.startswith(opts[0]) and i != opts[0]:
                        # yield commands
                        yield Completion(i, -len(opts[0]))
                    # when command input is done and followed by spaces
                    elif i == opts[0] and len(text) > len(opts[0]):
                        comb = []
                        _opts = self.opts_dict[opts[0]]["opts"]
                        args = self.opts_dict[opts[0]]["args"]
                        for i in args:
                            if i in dy:
                                comb.extend(dy[i])
                        comb.extend(_opts)
                        for i in comb:
                            yield Completion(i)

            else:
                if opts[0] in self.opts_dict:
                    comb = []
                    _opts = self.opts_dict[opts[0]]["opts"]
                    args = self.opts_dict[opts[0]]["args"]
                    for i in args:
                        if i in dy:
                            comb.extend(dy[i])
                    comb.extend(_opts)
                    for i in comb:
                        if i.startswith(opts[-1]):
                            pos = 0 if text.endswith(" ") else -len(opts[-1])
                            yield Completion(i, pos)
