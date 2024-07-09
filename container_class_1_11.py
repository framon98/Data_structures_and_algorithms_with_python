import turtle
import tkinter
import tkinter.filedialog
import tkinter.colorchooser
import xml.dom.minidom

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

    def __str__(self):
        return '<Command x="' + str(self.x) + '" y="' + str(self.y) + '" width="' + \
                str(self.width) + '" color="' + self.color + '">GoTo</Command>'

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
                attr = commandElement.attributes
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
                
                self.append(cmd)

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
            filename = tkinter.filedialog.asksaveasfilename(title="Save Picture As...")
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
        screen.tracer(0)

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

        # The button is created and made to fill the sidebar for easy use
        circleButton = tkinter.Button(sideBar, text="Draw Circle", command=circleHandler)
        circleButton.pack(fill=tkinter.BOTH)

        # Color Mode 255 allows the use of RGB code when selectin the pen color. This allows
        # each value to be a number in the range 00-FF for each value. Theselector returns a string
        # with the selected color and a slice is taken to get the #RRGGBB hexadecimal string
        screen.colormode(255)
        penLabel = tkinter.Label(sideBar, text="Pen Color")
        penLabel.pack()
        penColor = tkinter.StringVar()
        penEntry = tkinter.Entry(sideBar, textvariable=penColor)
        penEntry.pack()

        # This is color black
        penColor.set("#000000")

        def getPenColor():
            color = tkinter.colorchooser.askcolor()
            if color != None:
                penColor.set(str(color)[-9:-2])

        penColorButton = tkinter.Button(sideBar, text="Pick Pen Color", command=getPenColor)
        penColorButton.pack(fill=tkinter.BOTH)

        fillLabel = tkinter.Label(sideBar, text="Fill Color")
        fillLabel.pack()
        fillColor = tkinter.StringVar()
        fillEntry = tkinter.Entry(sideBar, textvariable=fillColor)
        fillColor.set("#000000")

        def getFillColor():
            color = tkinter.colorchooser.askcolor()
            if color != None:
                fillColor.set(str(color)[-9:-2])
        
        fillColorButton = tkinter.Button(sideBar, text="Pick Fill Color", command=getFillColor)
        fillColorButton.pack(fill=tkinter.BOTH)
        

        def beginFillHandler():
            cmd = BeginFillCommand(fillColor.get())

        beginFillButton = tkinter.Button(sideBar, text="Begin Fill", command=beginFillHandler)
        beginFillButton.pack(fill=tkinter.BOTH)

        def endFillHandler():
            cmd = EndFillCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

        endFillButton = tkinter.Button(sideBar, text="End Fill", command=endFillHandler)
        endFillButton.pack(fill=tkinter.BOTH)

        penLabel = tkinter.Label(sideBar, text="Pen is Down")
        penLabel.pack()

        def penUpHandler():
            cmd = PenUpCommand()
            cmd.draw(theTurtle)

            penLabel.configure(text="Pen is Up")
            self.graphicsCommands.append(cmd)

        penUpButton = tkinter.Button(sideBar, text="Pen Up", command=penUpHandler)
        penUpButton.pack(fill=tkinter.BOTH)

        def penDownHandler():
            cmd = penDownHandler()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen is Down")
            self.graphicsCommands.append(cmd)

        penDownButton = tkinter.Button(sideBar, text="Pen Down", command=penDownHandler)
        penDownButton.pack(fill=tkinter.BOTH)

        # This is a handler for a click event, meaning this tell the program what to do if a mouse clicks
        def clickHandler(x, y):
            # When a mouse clicks, get the widthzie entry and set the width of the pen to that.
            # The float method is needed due to the entry being a string
            cmd = GoToCommand(x, y, float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()

        # This method ties the click hanlder to the mouse click
        screen.onclick(clickHandler)

        # This methos handler the dragging of the pen across the screen
        def dragHandler(x, y):
            cmd = GoToCommand(x, y,float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)
            screen.update()
            screen.listen()

        theTurtle.ondrag(dragHandler)

        #This removes the last command from the list and redraws the image
        def undoHandler():
            if len(self.graphicsCommands) > 0:
                self.graphicsCommands.removeLast()
                theTurtle.clear()
                theTurtle.penup()
                theTurtle.goto(0, 0)
                theTurtle.pendown()
                for cmd in self.grapchisCommands:
                    cmd.draw(theTurtle)
                screen.update()
                screen.listen()

        screen.onkeypress(undoHandler, "u")
        screen.listen()


def main():

    root = tkinter.Tk()
    drawingApp = DrawingApplication(root)

    drawingApp.mainloop()

    print("Program Execution Completed")

if __name__ == "__main__":
    main()
