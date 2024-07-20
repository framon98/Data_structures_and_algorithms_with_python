#!/usr/bin/python3
import turtle

def drawSpiral(turt, length, color, colorBase):




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