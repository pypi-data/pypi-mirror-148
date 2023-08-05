from .rejex_static import Static

class Rejex:
    def __init__(self, start_flag:bool=True, end_flag:bool=False) -> None:
        """ Initialize Rejex object.

        Args:
            start_flag (bool, optional): Matches expression only at the start. Defaults to True.
            end_flag (bool, optional): Matches expression only at the end(Doesn't work as intended). Defaults to False.
        """
        self.string:str = ""

        self._start_flag:bool = start_flag
        self._end_flag:bool = end_flag

        if not start_flag:
            self.string += ".*"

    @property
    def get_start_flag(self) -> bool:
        return self._start_flag

    @property
    def get_end_flag(self) -> bool:
        return self._end_flag

    def compile(self) -> str:
        if self._end_flag:
            self.string += "$"

        return self.string

    def literal(self, literal:str) -> 'Rejex':
        """ Literal is a string that will be matched exactly.

        Args:
            literal (str): Literal string to be matched.

        Returns:
            Rejex: Rejex object.
        """

        self.string += Static.literal(literal)

        return self

    def any_char_except_newline(self) -> 'Rejex':
        """ Any character except newline.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_char_except_newline()

        return self

    def any_number(self) -> 'Rejex':
        """ Match any number character. Similar to '[0-9]'.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_number()

        return self

    def any_non_number(self) -> 'Rejex':
        """ Match any non number character. Similar to '[0-9]'.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_non_number()

        return self

    def any_word_character(self) -> 'Rejex':
        """ Match any word character. Similar to '[a-zA-Z_0-9]'.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_word_character()

        return self

    def any_non_word_character(self) -> 'Rejex':
        """ Match any non word character. Similar to '[^a-zA-Z_0-9]'.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_non_word_character()

        return self

    def any_whitespace_character(self) -> 'Rejex':
        """ Match any whitespace character. Similar to '[ \\f\\n\\r\\t\\v]'.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_whitespace_character()

        return self

    def any_non_whitespace_character(self) -> 'Rejex':
        """ Match any non whitespace character. Similar to '[^ \\f\\n\\r\\t\\v]'.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.any_non_whitespace_character()

        return self

    def alternative(self, *alts, fast=False) -> 'Rejex':
        """ If a string matches any one in the alts list then it will match.

        Args:
            alts (list): The list of alt strings/chars.
            fast (bool): Doesn't check alts and compiles to string using the fastest universal method(Might become unreadable). Defaults to False

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.alternative(*alts, fast=fast)

        return self

    def except_expr(self, expr:str) -> 'Rejex':
        """ Is a NOT operation on the expression.
        This doesn't work with "start_flag=False"

        Args:
            expr (str): The expression to be inversed

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.except_expr(expr)

        return self

    def n_number_times(self, n:int, expr:str) -> 'Rejex':
        """ Match 'expr' expression set exactly 'n' number of times.

        Args:
            n (int): The number of times the previous set will be matched/searched for.
            expr (str): The expression set to be matched exactly 'n' number of times.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.n_number_times(n, expr)

        return self

    def zero_or_more(self, expr:str) -> 'Rejex':
        """ The 'expr' to be matched zero or more times.

        Args:
            expr (str): The 'exp' to be matched zero or more times.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.zero_or_more(expr)

        return self

    def one_or_more(self, expr:str) -> 'Rejex':
        """ The 'expr' to be matched one or more times.

        Args:
            expr (str): The 'exp' to be matched one or more times.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.one_or_more(expr)

        return self

    def zero_or_one(self, expr:str) -> 'Rejex':
        """ The 'expr' to be matched zero or one time.

        Args:
            expr (str): The 'exp' to be matched zero or one time.

        Returns:
            Rejex: Rejex object.
        """
        self.string += Static.zero_or_one(expr)

        return self

    def range(self, start:str, end:str) -> 'Rejex':
        """ Match a range of characters.

        Args:
            start (str): The start of the range.
            end (str): The end of the range.

        Returns:
            str: Rejex string.
        """
        self.string += Static.range(start, end)

        return self