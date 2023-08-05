from re import *

class Static:

    @staticmethod
    def literal(literal:str) -> str:
        """ Literal is a string that will be matched exactly.

        Args:
            literal (str): Literal string to be matched.

        Returns:
            str: Rejex string.
        """
        if not isinstance(literal, str):
            try:
                literal = str(literal)
            except Exception:
                raise ValueError(f"Literal '{literal}' must be a string or should be convertable to string.")

        to_be_escaped = "^$.|()*+?{}[]\\"
        new_literal = ""
        for i in literal:
            if i not in to_be_escaped:
                new_literal += i
            else:
                new_literal += "\\" + i

        return new_literal

    @staticmethod
    def any_char_except_newline() -> str:
        """ Any character except newline. If DOTALL flag is selected, newlines are also matched

        Returns:
            str: Rejex string.
        """
        return "."

    @staticmethod
    def any_number() -> str:
        """ Match any number character. Similar to '[0-9]'.

        Returns:
            str: Rejex string.
        """
        return "\\d"

    @staticmethod
    def any_non_number() -> str:
        """ Match any non number character. Similar to '[^0-9]'.

        Returns:
            str: Rejex string.
        """
        return "\\D"

    @staticmethod
    def any_word_character() -> str:
        """ Match any word character. Similar to '[a-zA-Z_0-9]'.

        Returns:
            str: Regex string.
        """
        return "\\w"

    @staticmethod
    def any_non_word_character() -> str:
        """ Match any non word character. Similar to '[^a-zA-Z_0-9]'.

        Returns:
            str: Regex string.
        """
        return "\\W"

    @staticmethod
    def any_whitespace_character() -> str:
        """ Match any whitespace character. Similar to '[ \\f\\n\\r\\t\\v]'.

        Returns:
            str: Regex string.
        """
        return "\\s"

    @staticmethod
    def any_non_whitespace_character() -> str:
        """ Match any non whitespace character. Similar to '[^ \\f\\n\\r\\t\\v]'.

        Returns:
            str: Regex string.
        """
        return "\\S"

    @staticmethod
    def alternative(*alts, fast=False) -> str:
        """ If a string matches any one in the alts list then it will match.

        Args:
            alts (list): The list of alt strings/chars.

        Returns:
            str: Rejex string.
        """
        alts = [*alts]
        try:
            new_alts = [i if isinstance(i, str) else str(i) for i in alts]
        except Exception:
            raise ValueError(f"All values in alts '{alts}' must be a string or should be convertable to string.")

        if fast:
            return f"({'|'.join(new_alts)})"

        if all(len(i)==1 and i != "-" for i in new_alts):
            #if all of them are single chars, use [abc] notation
            return f"[{''.join(new_alts)}]"
        elif all(bool(match(r"^\[.-.\]$", i)) for i in new_alts):
            return f"[{''.join(i[1:-1] for i in new_alts)}]"
        else:
            #if any of them are more than one char, use a|b|c notation
            return f"({'|'.join(new_alts)})"

    @staticmethod
    def except_expr(expr:str) -> str:
        """ Is a NOT operation on the expression.
        This doesn't work with "start_flag=False"

        Args:
            expr (str): The expression to be inversed

        Returns:
            str: Rejex string.
        """
        if not isinstance(expr, str):
            try:
                expr = str(expr)
            except ValueError:
                raise ValueError(f"Expression '{expr}' must be a string or should be convertable to string.")

        if expr[0] == "[" and expr[-1] == "]":
            return f"[^{expr[1:-1]}]"

        return f"[^{expr}]"

    @staticmethod
    def n_number_times(n:int, expr:str) -> str:
        """ Match 'expr' expression set exactly 'n' number of times.

        Args:
            n (int): The number of times the previous set will be matched/searched for.
            expr (str): The expression set to be matched exactly 'n' number of times.

        Returns:
            str: Rejex string.
        """
        assert isinstance(n, int), "n must be an integer."
        
        if not isinstance(expr, str):
            try:
                expr = str(expr)
            except ValueError:
                raise ValueError(f"Expression '{expr}' must be a string or should be convertable to string.")

        if len(expr) == 1:
            return f"{expr}{{{n}}}"
        return f"({expr}){{{n}}}"

    @staticmethod
    def zero_or_more(expr:str) -> str:
        """ The 'expr' to be matched zero or more times.

        Args:
            expr (str): The 'exp' to be matched zero or more times.

        Returns:
            str: Rejex string.
        """
        if not isinstance(expr, str):
            try:
                expr = str(expr)
            except ValueError:
                raise ValueError(f"Expression '{expr}' must be a string or should be convertable to string.")

        if len(expr) == 1:
            return f"{expr}*"
        return f"({expr})*"

    @staticmethod
    def one_or_more(expr:str) -> str:
        """ The 'expr' to be matched one or more times.

        Args:
            expr (str): The 'exp' to be matched one or more times.

        Returns:
            str: Rejex string.
        """
        if not isinstance(expr, str):
            try:
                expr = str(expr)
            except ValueError:
                raise ValueError(f"Expression '{expr}' must be a string or should be convertable to string.")

        if len(expr) == 1:
            return f"{expr}+"
        return f"({expr})+"

    @staticmethod
    def zero_or_one(expr:str) -> str:
        """ The 'expr' to be matched zero or one time.

        Args:
            expr (str): The 'exp' to be matched zero or one time.

        Returns:
            str: Rejex string.
        """
        if not isinstance(expr, str):
            try:
                expr = str(expr)
            except ValueError:
                raise ValueError(f"Expression '{expr}' must be a string or should be convertable to string.")

        if len(expr) == 1:
            return f"{expr}?"
        return f"({expr})?"

    @staticmethod
    def range(start:str, end:str) -> str:
        """ Match a range of characters.

        Args:
            start (str): The start of the range.
            end (str): The end of the range.

        Returns:
            str: Rejex string.
        """
        if not isinstance(start, str):
            try:
                start = str(start)
            except ValueError:
                raise ValueError(f"Start '{start}' must be a string or should be convertable to string.")

        if not isinstance(end, str):
            try:
                end = str(end)
            except ValueError:
                raise ValueError(f"End '{end}' must be a string or should be convertable to string.")

        return f"[{start}-{end}]"