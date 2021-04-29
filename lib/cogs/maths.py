import discord, math, re, cmath, aiofiles, os
from enum import Enum
from dataclasses import dataclass
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pylatexenc.latex2text import LatexNodes2Text
from pylatexenc.latexwalker import LatexWalkerError
from discord.ext import commands
from discord import Embed
WHITESPACE = [' ', '\n' '\t']
DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def findnumbers(numbers):
    if ',' in numbers:
        split = numbers.split(",")
        numbers = []
        for number in split:
            try:
                numbers.append(float(number))
            except ValueError:
                pass
    else:
        split = numbers.split(" ")
        numbers = []
        for number in split:
            try:
                numbers.append(float(number))
            except ValueError:
                pass
    return numbers

def getSize(txt, font):
    Img = Image.new('RGB', (1, 1))
    drawn = ImageDraw.Draw(Img)
    return drawn.textsize(txt, font)

class TokenType(Enum):
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    LPAREN = 5
    RPAREN = 6

@dataclass
class Token:
    type: TokenType
    value: any = None

    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else "")

@dataclass
class Token:
    type: TokenType
    value: any = None

class Lexer:
    def __init__(self, query):
        self.query = iter(query)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.query)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == '.' or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == "+":
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == "-":
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == "*":
                self.advance()
                yield Token(TokenType.MULTIPLY)
            elif self.current_char == "/":
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char == "(":
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ")":
                self.advance()
                yield Token(TokenType.RPAREN)
            else:
                raise Exception(f"Illegal character '{self.current_char}'")

    def generate_number(self):
        decimal_count = 0
        number_str = self.current_char
        self.advance()
        while self.current_char != None and self.current_char =='.' or self.current_char in DIGITS:
            if self.current_char == '.':
                decimal_count += 1
                if decimal_count > 1:
                    break
            number_str += self.current_char
            self.advance()
        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str = '0' + number_str
        return Token(TokenType.NUMBER, float(number_str))

@dataclass
class NumberNode:
    value: float
    def __repr__(self):
        return f"{self.value}"
@dataclass
class AddNode:
    node_a: any
    node_b: any
    def __repr__(self):
        return f"({self.node_a}+{self.node_b})"
@dataclass
class SubtractNode:
    node_a: any
    node_b: any
    def __repr__(self):
        return f"({self.node_a}-{self.node_b})"
@dataclass
class DivideNode:
    node_a: any
    node_b: any
    def __repr__(self):
        return f"({self.node_a}/{self.node_b})"
@dataclass
class MultiplyNode:
    node_a: any
    node_b: any
    def __repr__(self):
        return f"({self.node_a}*{self.node_b})"

@dataclass
class PlusNode:
    node: any
    def __repr__(self):
        return f"(+{self.node}"

@dataclass
class MinusNode:
    node: any
    def __repr__(self):
        return f"(-{self.node}"

@dataclass
class Number:
    value: any
    def __repr__(self):
        return f"{self.value}"

class Parser_:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.advance()

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token == None:
            return None

        result = self.expr()
        return result

        if self.current_token != None:
            raise Exception("Invalid syntax!")

    def expr(self):
        result = self.term()
        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())
        return result

    def term(self):
        result = self.factor()
        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.factor())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.factor())
        return result

    def factor(self):
        token = self.current_token
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type != TokenType.RPAREN:
                raise "Invalid syntax"
            self.advance()
            return result
        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())
        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())
        raise("Invalid syntax")


class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def visit_NumberNode(self, node):
        return Number(node.value)

    def visit_PlusNode(self, node):
        return self.visit(node.node)

    def visit_MinusNode(self, node):
        return Number(-self.visit(node.node).value)

    def visit_AddNode(self, node):
        return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)

    def visit_SubtractNode(self, node):
        return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

    def visit_MultiplyNode(self, node):
        return Number(self.visit(node.node_a).value * self.visit(node.node_b).value)

    def visit_DivideNode(self, node):
        try:
            return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)
        except:
            raise Exception("Runtime math error")

class maths(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="calculator", description="A simple python calculator", aliases=["calc", "calculate"])
    async def calculator(self, ctx, *, query=None):
        if query is None:
            text = """
Usage: ./calc [calculation]

Supported operations:
    [+] Addition
    [-] Subtraction
    [/] Division
    [*] Multiplication
    [()] Parenthasis
    [-(int)] Negative numbers
    [+(int)] Positive numbers
            """
            await ctx.send(f"```{text}```")
        else:
            try:
                lexer = Lexer(query)
                tokens = lexer.generate_tokens()
                parser = Parser_(tokens)
                tree = parser.parse()
                interpreter = Interpreter()
                value = interpreter.visit(tree)
                print(value)
                await ctx.send(f"```{value}```")
            except Exception as e:
                print(e)
                await ctx.send(f"```There was an error while performing your calculation: {e}\n{text}```")

    @commands.command(name="StandardDeviation", description="Standard deviation of values", aliases=["std"])
    async def std(self, ctx, *, numbers):
        numbers = re.findall('[0-9]+', numbers)
        for i in range(0, len(numbers)):
            numbers[i] = int(numbers[i])
        std = np.std(numbers)
        await ctx.send(f"The standard deviation is: {round(std, 3)}")

    @std.error
    async def std_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            text = """
Usage: ./std [List of numbers]
            """
            await ctx.send(f"```{text}```")

    @commands.command(name="round", description="Round a value/list of values", aliases=["rnd"])
    async def round_(self, ctx, decimalplaces=None, *, numbers=None):
        text = """
        Usage: ./rnd [Decimal places] [numbers]

        Use 0 decimal places for the nearest whole number

                    """
        if decimalplaces is None:
            await ctx.send(f"```{text}```")
        else:
            try:
                decimalplaces = int(decimalplaces)
                check = True
            except ValueError:
                check = False
                await ctx.send(f"```Decimal places must be an integer\n{text}```")
                raise
            if check is not False:
                numbers = findnumbers(numbers)
                rounded = []
                if decimalplaces == 0:
                    for x in numbers:
                        rounded.append(round(x))
                else:
                    for x in numbers:
                        rounded.append(round(x, decimalplaces))
                strtosend = ""

                for x in rounded:
                    if len(rounded) == 1:
                        strtosend = f"{x}"
                    else:
                        strtosend += f"{x}, "
                await ctx.send(f"```{strtosend}```")

    @commands.command(name="ceil", description="ceil a value/list of values", aliases=["roundup", "rndup"])
    async def ceil_(self, ctx, *, numbers=None):
        if numbers is None:
            text = """
Usage: ./ceil [list of values]
            """
            await ctx.send(f"```{text}```")
        else:
            numbers = findnumbers(numbers)
            ceiled = []
            for number in numbers:
                ceiled.append(math.ceil(number))
            strtosend = ""
            for x in ceiled:
                if len(ceiled) == 1:
                    strtosend = f"{x}"
                else:
                    strtosend += f"{x}, "
            if len(ceiled) != 1:
                strtosend = strtosend[0:len(strtosend) - 2]
            await ctx.send(f"```{strtosend}```")

    @commands.command(name="floor", description="floor a value/list of values", aliases=["rounddown", "rnddown"])
    async def floor_(self, ctx, *, numbers=None):
        if numbers is None:
            text = "Usage: ./floor [list of values]"
            await ctx.send(f"```{text}```")
        else:
            numbers = findnumbers(numbers)
            floored = []
            for number in numbers:
                floored.append(math.floor(number))
            strtosend = ""
            for x in floored:
                if len(floored) == 1:
                    strtosend = f"{x}"
                else:
                    strtosend += f"{x}, "
            if len(floored) != 1:
                strtosend = strtosend[0:len(strtosend) - 2]
            await ctx.send(f"```{strtosend}```")

    @commands.command(name="greatestcommondivisor", description="Finds the greatest common divisor of a set of values", aliases=["gcd"])
    async def gcd_(self, ctx, *, numbers=None):
        text = """
        Usage: ./gcd [num1] [num2]
                    """
        if numbers is None:
            await ctx.send(f"```{text}```")
        else:
            numbers = findnumbers(numbers)
            if len(numbers) == 2:
                try:
                    numbers = list(map(int, numbers))
                    check = True
                except ValueError:
                    await ctx.send(f"```Numbers must be whole numbers\n{text}```")
                    check = False
                if check is True:
                    divisor = math.gcd(numbers[0], numbers[1])
                    text = f"Numbers: {numbers[0]}, {numbers[1]}\nDivisor: {divisor}"
                    await ctx.send(f"```{text}```")
            else:
                await ctx.send(f"```Please enter two numbers\n{text}```")

    @commands.command(name="quadratic", description="Solves quadratic equation", aliases=["solvequadratic"])
    async def quadratic(self, ctx, a=None, b=None, c=None):
        text = "Usage: ./quadratic [a] [b] [c]"
        if a is None or b is None or c is None:
            await ctx.send(f"```{text}```")
        else:
            try:
                a = int(a)
                b = int(b)
                c = int(c)
                check = True
            except ValueError:
                await ctx.send(f"```One or more values were not integers\n{text}```")
                check = False
            if a == 0:
                await ctx.send(f"```Invalid quadratic, 'a' cannot be 0\n{text}```")
                check = False
            if check is True:
                d = (b ** 2) - (4*a*c)
                s1 = (-b-cmath.sqrt(d))/(2*a)
                s2 = (-b+cmath.sqrt(d))/(2*a)
                await ctx.send(f"```The two solutions are: {s1} and {s2}```")


def setup(client):
    client.add_cog(maths(client))
