import turtle
import tkinter
import xml

class GoToCommand:
    def __init__(self, x, y, width = 1, color = "black"):
        self.x = x
        self.y = y
        self.color = color
        self.width = width 

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)

class CircleCommand:
    def __init__(self, radius, width = 1, color = "black"):
        self.radius = radius
        self.width = width
        self.color = color

    def draw(self, turtle):
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.circle(self.radius)

class BeginFillCommand:
    def __init__(self, color):
        self.color = color

    def draw(self, turtle):
        turtle.fillcolor(self.color)
        turtle.begin_fill()

class EndFillCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.end_fill()

class PenUpCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.penup()

class PenDownCommand:
    def __init__(self):
        pass

    def draw(self, turtle):
        turtle.pendown()

class PyList:
    def __init__(self):
        self.items = []

    def append(self, item):
        self.items = self.items + [item]

    def __iter__(self):
        for c_item in self.items:
            yield c_item


# This clas defines the drawin application. The following line says that 
# the drawing application class inherits fromt he Frame class. This means
# that a DrawingApplication is liek a Frame object except for the code
# written here which redefines/extends the behavior of Frame
class DrawingApplication(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.buildWindow()
        self.graphicsCommands = PyList()

    # This method is called to create all the widgets, place them in the GUI,
        # and define the event handle for the application
    def buildWindow(self):

        # The master is the root window. The title is set below
        self.master.title("Draw")

        # Here is how to create a menu bar. the tearoff = 0 means that menus
        # can't be separated from the window which is a feature of tkinter
        bar = tkinter.Menu(self.master)
        fileMenu = tkinter.Menu(bar, tearoff=0)

        # This code is called by the New menu item below when it is selected.
        # The same aplies for the loadFile, addtofile, and savefile below. 
        # The exit menu item below callsquit on the master or root window
        def newWindow():
            # This sets theturtle to be ready for a new picture. It also
            # sets the sequence back to empty. It is necessary for the 
            # graphicsCommands sequence to be in the object. Because
            # otherwise the statemntÑ graphicsCommands = PyList()
            # would make this variable a local one in the newWindow method.
            # If it were local, it would not be set anymore once the newwindow method returned

            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto(0,0)
            theTurtle.pendown()
            screen.update()
            screen.listen()
            self.graphicsCommands = PyList()
        
        fileMenu.add_command(label="New", command=newWindow)

        # The parse function adds the contents of an XMl file to the sequence
        def parse(filename):
            xmldoc = xml.dom.minidom.parse(filename)

            graphicsCommandsElement = xmldoc.getElementsByTagName("GraphicsCommands")[0]

            graphicsCommands = graphicsCommandsElement.getElementsByTagName("Command")

            for commandElement in graphicsCommands:
                print(type(commandElement))
                command = commandElement.firstChild.data.strip()
                attr = commandElement.attribute
                if command == "GoTo":
                    x = float(attr["x"].value)
                    y = float(attr["y"].value)
                    width = float(attr["width"].value)
                    color = attr["color"].value.strip()
                    cmd = GoToCommand(x, y, width, color)

                elif command == "Circle":
                    radius = float(attr["radius"].value)
                    width = float(attr["width"].value)
                    color = attr["color"].value.strip()
                    cmd = CircleCommand(radius, width, color)

                elif command == "BeginFill":
                    color = attr["color"].value.strip()
                    cmd = BeginFillCommand(color)

                elif command == "EndFill":
                    cmd = EndFillCommand()

                elif command == "PenUp":
                    cmd = PenUpCommand()

                elif command == "PenDown":
                    cmd = PenDownCommand()

                else: 
                    raise RuntimeError("Unknown Command: " +  command)

            def loadFile():
                filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")

                newWindow()

                # This re initializes the sequence for the new picture
                self.graphicsCommands = PyList()

                # calling parse will read the rgaphics commans from the file
                parse(filename)

                for cmd in self.graphicsCommands:
                    cmd.draw(theTurtle)

                # This line is necessary to update the window after the picture
                # is drawn
                screen.update()

            fileMenu.add_command(label="Load...", command=loadFile)

            def addToFile():
                filename = tkinter.filedialog.askopenfilename(title="Select a Graphics File")

                theTurtle.penup()
                theTurtle.goto(0, 0)
                theTurtle.pendown()
                theTurtle.pencolor("#000000")
                theTurtle.fillcolor("#000000")
                cmd = PenUpCommand()
                self.graphicsCommands.append(cmd)
                cmd = GoToCommand(0, 0, 1, "#000000")
                self.graphicsCommands.append(cmd)
                cmd = PenDownCommand()
                self.graphicsCommands.append(cmd)
                screen.update()
                parse(filename)

                for cmd in self.graphicsCommands:
                    cmd.draw(theTurtle)
                    screen.update()

            fileMenu.add_command(label="Load into...", command=addToFile)

            # The write functon write an XML file to the givenfilename
            def write(filename):
                file = open(filename, "w")
                file.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n')
                file.write('<GraphicsCommands>\n')
                for cmd in self.graphicsCommands:
                    file.write('    ' + str(cmd) + "\n")

                file.write('</GraphicsCommands>\n')

                file.close()
            
            def saveFile():
                filename = tkinter.filedialog.asksaveasfilename(title="Save Pciture As...")
                write(filename)

            fileMenu.add_command(label="Save As...", command=saveFile)

            fileMenu.add_command(label="Exit", command=self.master.quit)

            bar.add_cascade(label="File", menu=fileMenu)

            # This helps show the newly created menu bar into the root window
            self.master.config(menu=bar)

            # Adding here some widgets like the drawing panel
            canvas = tkinter.Canvas(self, width=600, height=600)
            canvas.pack()

            # We create rawturtle to allow it to draw on screen, we instance the turtle in the canvas
            theTurtle = turtle.RawTurtle(canvas)

            # We make the shape of the turtle a circle
            theTurtle.shape("circle")
            screen = theTurtle.getscreen()

            # The next line helps not update the screen unless screen.update is called
            # this prevent the program from crashing when using the draghandler
            screen.tracer()

            # Here we are creating the right side of the window for the buttons, labels and boxes. 
            # This makes the fram fill the right side completely where it is available.
            sideBar = tkinter.Frame(self, padx=5, pady=5)
            sideBar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

            # This label widget, when using pack, it gets placed at the top of the sidebar
            pointLabel = tkinter.Label(sideBar, text="Width")
            pointLabel.pack()

            # This netry allows user to pick width for the lines. This variable widthSize 
            # can be used to get and set the value od the drawing line
            widthSize = tkinter.StringVar()
            widthEntry = tkinter.Entry(sideBar, textvariable=widthSize)

            widthEntry.pack()
            widthSize.set(str(1))

            radiusLabel = tkinter.Label(sideBar, text="Radius")
            radiusLabel.pack()
            radiusSize = tkinter.StringVar()
            radiusEntry = tkinter.Entry(sideBar, textvariable=radiusSize)
            radiusSize.set(str(10))
            radiusEntry.pack()

            # A button widget calls an event handler when pressed. The circleHandler function below
            # is the event handler when the Draw Circle button is pressed
            def circleHandler():

                # When drawing a command is creted and then the command is drawn by calling the draw
                # method. Adding the commadn to the graphics commasn sequence means the application will remember
                cmd = CircleCommand(float(radiusSize.get()), float(widthSize.get()), penColor.get())
                cmd.draw(theTurtle)
                self.graphicsCommands.append(cmd)

                # This lines update the screen and puts focus back on the canvas. This is necessary
                # because pressing "u" to undo the screen must have focus to receive the keypress
                screen.update()
                screen.listen()


def main():
    filename = input("Please enter drawing filename: ")
    t = turtle.Turtle()
    screen = t.getscreen()
    file = open(filename, "r")

    graphicsCommands = PyList()

    command = file.readline().strip()

    while command != "":
        if command == "goto":
            x = float(file.readline())
            y = float(file.readline())
            width = float(file.readline())
            color = file.readline().strip()
            cmd = GoToCommand(x, y, width, color)

        elif command == "circle":
            radius = float(file.readline())
            width = float(file.readline())
            color = file.readline().strip()
            cmd = CircleCommand(radius, width, color)

        elif command == "beginfill":
            color = file.readline().strip()
            cmd = BeginFillCommand(color)

        elif command == "endfill":
            cmd = EndFillCommand()

        elif command == "penup":
            cmd = PenUpCommand()

        elif command == "pendown":
            cmd = PenDownCommand()
        
        else:
            raise RuntimeError("Unknown Command: " + command)

        graphicsCommands.append(cmd)

        command = file.readline().strip()

    for cmd in graphicsCommands:
        cmd.draw(t)

    file.close()
    t.ht()
    screen.exitonclick()
    print("Program Execution Completed")

if __name__ == "__main__":
    main()
