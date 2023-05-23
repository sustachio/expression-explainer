"""
from PIL import Image, ImageDraw, ImageFont

BLACK = (0, 0, 0)

BACKGROUND_COLOR = (200,200,200)
FONT = ImageFont.truetype("/usr/share/fonts/truetype/lato/Lato-Black.ttf", 28, encoding="unic")

image = Image.new(mode="RGB", size=(200, 200))
image.paste(BACKGROUND_COLOR, (0, 0, image.size[0], image.size[1]))

draw = ImageDraw.Draw(image)

def write_text(text):
    draw.text(
            xy=(10, 10),
            text=text,
            font=FONT,
            fill=BLACK
            )

write_text("4+3+1(4*3)")



#draw.rectangle(xy = (50, 50, 150, 150),
#               fill = (0, 127, 0),
#               outline = (255, 255, 255),
#               width = 5)

image.show()
"""

"""
1. While there are still tokens to be read in,
   1.1 Get the next token.
   1.2 If the token is:
       1.2.1 A number: push it onto the value stack.
       1.2.2 A variable: get its value, and push onto the value stack.
       1.2.3 A left parenthesis: push it onto the operator stack.
       1.2.4 A right parenthesis:
         1.2.4.1 While the thing on top of the operator stack is not a 
           left parenthesis,
             1.2.4.1.1 Pop the operator from the operator stack.
             1.2.4.1.2 Pop the value stack twice, getting two operands.
             1.2.4.1.3 Apply the operator to the operands, in the correct order.
             1.2.4.1.4 Push the result onto the value stack.
         1.2.4.2 Pop the left parenthesis from the operator stack, and discard it.
       1.2.5 An operator (call it thisOp):
         1.2.5.1 While the operator stack is not empty, and the top thing on the
           operator stack has the same or greater precedence as thisOp,
           1.2.5.1.1 Pop the operator from the operator stack.
           1.2.5.1.2 Pop the value stack twice, getting two operands.
           1.2.5.1.3 Apply the operator to the operands, in the correct order.
           1.2.5.1.4 Push the result onto the value stack.
         1.2.5.2 Push thisOp onto the operator stack.
2. While the operator stack is not empty,
    2.1 Pop the operator from the operator stack.
    2.2 Pop the value stack twice, getting two operands.
    2.3 Apply the operator to the operands, in the correct order.
    2.4 Push the result onto the value stack.
3. At this point the operator stack should be empty, and the value
   stack should have only one value in it, which is the final result.
"""

# single expression
def calculate(operator, left, right):
    match operator:
        case "+":
            return left + right

        case "-":
            return left - right

        case "*":
            return left * right

        case "/":
            return left / right

        case _:
            raise SyntaxError(f"Unkown operator '{operator}' apllied on '{left}' and '{right}'")

def get_predecence(operator: str) -> int:
    match operator:
        case "+" | "-":
            return 1

        case "*" | "/":
            return 2

        case _:
            return 0

# evaluate an expression
def algorithm(expression: str) -> int | float:
    value_stack: list[int | float] = []
    operator_stack: list[str] = []

    index = 0


    # 1. While there are still tokens to be read in,
    while index < len(expression):
        # 1.1 Get the next token.
        token = expression[index]

        # 1.2 If the token is:

        # 1.2.1 A number: push it onto the value stack.
        if token.isdigit():
            number = ""

            while token.isdigit() and index < len(expression):
                number += token

                index += 1
                token = expression[index]

            value_stack.append(int(number))

            continue


        # 1.2.2 A variable: get its value, and push onto the value stack.
        # TODO: implement variables


        # 1.2.3 A left parenthesis: push it onto the operator stack.
        elif token == "(":
            operator_stack.append(token)


        # 1.2.4 A right parenthesis:
        elif token == ")":

            # 1.2.4.1 While the thing on top of the operator stack is not a left parenthesis,
            while operator_stack[-1] != "(":

                # 1.2.4.1.1 Pop the operator from the operator stack.
                operator = operator_stack.pop()
                # 1.2.4.1.2 Pop the value stack twice, getting two operands.
                right, left = value_stack.pop(), value_stack.pop()

                # 1.2.4.1.3 Apply the operator to the operands, in the correct order.
                result = calculate(operator, left, right)

                # 1.2.4.1.4 Push the result onto the value stack.
                value_stack.append(result)

            # 1.2.4.2 Pop the left parenthesis from the operator stack, and discard it.
            operator_stack.pop()


        # 1.2.5 An operator:
        elif token in "+-*/":

            # 1.2.5.1 While the operator stack is not empty, and the top thing on the operator stack has the same or greater precedence as this operator,
            while len(operator_stack) and get_predecence(operator_stack[-1]) >= get_predecence(token):
                # 1.2.5.1.1 Pop the operator from the operator stack.
                operator = operator_stack.pop()
                # 1.2.5.1.2 Pop the value stack twice, getting two operands.
                right, left = value_stack.pop(), value_stack.pop()

                # 1.2.5.1.3 Apply the operator to the operands, in the correct order.
                result = calculate(operator, left, right)

                # 1.2.5.1.4 Push the result onto the value stack.
                value_stack.append(result)

            # 1.2.5.2 Push thisOp onto the operator stack.
            operator_stack.append(token)

        index += 1



    # 2. While the operator stack is not empty,
    while len(operator_stack):
        # 2.1 Pop the operator from the operator stack.
        operator = operator_stack.pop()
        # 2.2 Pop the value stack twice, getting two operands.
        right, left = value_stack.pop(), value_stack.pop()

        # 2.3 Apply the operator to the operands, in the correct order.
        result = calculate(operator, left, right)

        # 2.4 Push the result onto the value stack.
        value_stack.append(result)


    # 3. At this point the operator stack should be empty, and the value stack should have only one value in it, which is the final result.
    return value_stack[0]



print(algorithm("4*2+(3-6)"))
print(4 * 2 + (3-6))
