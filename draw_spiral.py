#!/usr/bin/python3
import turtle

def drawSpiral(turt, length, color, colorBase):
    
    # color is a 24bit value that changes each time 
    # for a colro effect
    if length == 0:
        return
    
    # add 2^10 to the old color modulo 2^24
    # the modulo 2^24 prevents the color from getting to big
    newcolor = (int(color[1:], 16) + 2**10) % (2**24)
    
    # This finds the color base integer value
    base = int(colorBase[1:], 16)

    # If the newcolor is less than base
    # add the base modulo 2^24
    if newcolor < base:
        newcolor = (newcolor + base) % (2**24)

    # here is the conversion to the hex string
    newcolor = hex(newcolor)[2:]

    # This adds the pound sign and 6 zeroes to the front
    # to make it a proper color value
    newcolor = "#"+("0"*(6-len(newcolor))) + newcolor

    turt.color(newcolor)
    turt.forward(length)
    turt.left(90)

    drawSpiral(turt, length-1, newcolor, colorBase)

def main():
    turt = turtle.Turtle()
    screen = turt.getscreen()
    turt.speed(100)
    turt.penup()
    turt.goto(-100, -100)
    turt.pendown()

    drawSpiral(turt, 200, "#000000", "#ff00ff")

    screen.exitonclick()

if __name__ == "__main__":
    main()