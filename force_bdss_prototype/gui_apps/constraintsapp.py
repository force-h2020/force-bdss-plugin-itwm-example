from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup

from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty
from .kivy_library import MinMaxSlider, EditableLabel, KeyboardListener


#window
class ConstraintsApp(App):
    def build(self):
        root = BoxLayout(orientation = 'vertical')
        root.add_widget(ConstraintsTopRow(size_hint_y = 0.25))
        self.constraintWrapper = ConstraintWrapper(self.input,  size_hint_y=4, do_scroll_x=False)
        root.add_widget(self.constraintWrapper)
        root.add_widget(ConstraintsBottomRow(size_hint_y = 0.2))
        self.keyboardListener = KeyboardListener()
        return root

    def runWithOutput(self, editorInput, defaultOutput):
        self.input = editorInput
        self.output = defaultOutput
        self.run()
        return self.output

    def stopWithOutput(self):
        self.output = self.export()
        self.stop()
    
    def addConstraint(self):
        self.constraintWrapper.addEditableConstraint('New Constraint','?',0,1)

    def export(self):
        return self.constraintWrapper.export()

    def getIndex(self, name):
        return self.constraintWrapper.getIndex(name)
    
    def getWidgetIndex(self, widget):
        return self.constraintWrapper.getWidgetIndex(widget)
        
    def getShiftPressed(self):
        shift = (303, 'rshift')
        rshift = (304, 'shift')
        return shift in self.keyboardListener.pressedKeys or rshift in self.keyboardListener.pressedKeys
    

#Widgets
class ConstraintWrapper(ScrollView):
    constrainWidgets = []

    def __init__(self, constraints, **kwargs):
        super().__init__(**kwargs)
        self.view = GridLayout(cols=1, size_hint=(1, None))
        self.view.bind(minimum_height=self.view.setter('height'))
        for c in constraints:
            self.addStaticConstraint(c.get('name'),c.get('unit'),c.get('min'),c.get('max'))
        self.add_widget(self.view)
    
    def addStaticConstraint(self, name, unit, min, max):
        self.constrainWidgets.append(StaticConstraintWidget(name, unit, min, max, size_hint=(1,None), size = (50,135)))
        self.view.add_widget(self.constrainWidgets[len(self.constrainWidgets)-1])
    
    def addEditableConstraint(self, name, unit, min, max):
        if(self.getIndex(name) == -1):
            self.constrainWidgets.append(EditableConstraintWidget(name, unit, min, max, size_hint=(1,None), size = (50,135)))
            self.view.add_widget(self.constrainWidgets[len(self.constrainWidgets)-1])
        else:
            i = 2
            while (self.getIndex(name + str(i)) != -1):
                i += 1
            return self.addEditableConstraint(name+str(i), unit, min, max)

    def getIndex(self, name):
        for i in range(0, len(self.constrainWidgets)):
            if self.constrainWidgets[i].name == name:
                return i
        return -1

    def getWidgetIndex(self, constraintWidget):
        for i in range(0, len(self.constrainWidgets)):
            if self.constrainWidgets[i] == constraintWidget:
                return i
        return -1
    
    def export(self):
        output = []
        for constraint in self.constrainWidgets:
            output.append(constraint.export())
        return output

class ConstraintWidgetBase(RelativeLayout):
    _name = StringProperty()
    _unit = StringProperty()
    _value0 = NumericProperty()
    _value1 = NumericProperty()
    _min = NumericProperty()
    _max = NumericProperty()

    def __init__(self, name, unit, min, max, **kwargs):
        super().__init__(**kwargs)
        self._name = name
        self._unit = unit
        self._min = min
        self._value0 = min
        self._value1 = max
        self._max = max

    def setValue(self, newValue, index):
        if(index):
            self._value1 = newValue
        else:
            self._value0 = newValue
    
    def updateValueLabel(self, value, index):
        if(index):
            self.ids['maxLabel'].text = self.valueString(value)
        else:
            self.ids['minLabel'].text = self.valueString(value)

    def valueString(self, value):
        range = min(abs(self._max-self._min),abs(value))
        i = 0 
        rangeCheck = 0.1
        while(range < rangeCheck):
            rangeCheck *= 0.1
            i+=1
        if(i==0):
            return str(round(value, 2)) 
        return str(round(value, i+3))

    def resetValueLabel(self, index):
        if(index):
            self.updateValueLabel(self.ids['slider'].value1,1)
        else:
            self.updateValueLabel(self.ids['slider'].value0,0)

    def checkInBounds(self, value):
        if(value >= self._min and value <= self._max):
            return
        raise IndexError('value out of bounds')

    def checkValue(self, value, index):
        if(index): #max
            if(value >= self.ids['slider'].value0):
                return 
        else: #min
            if(value <= self.ids['slider'].value1):
                return 
        raise ValueError('Max < Min')

    def updateValue(self, stringValue, index):
        try:
            newValue = float(stringValue)
            self.checkValue(newValue,index)
            self.checkInBounds(newValue)
        except ValueError:
            content = 'Min-values must be smaller than Max-values!'
            popup = Popup(title='Warning',
            content=Label(text=content, text_size= (350, None)),
            size_hint=(None, None), size=(400, 300))
            popup.open()
            return self.resetValueLabel(index)
        except IndexError:
            if(self.shiftPressed()):
                return self.updateBounds(newValue,index)
            else:
                content = 'Value out of Bounds, please stay in bounds or redefine the bounds by pressing \'shift\' while updating a min/max value.'
                popup = Popup(title='Warning',
                content=Label(text=content, text_size= (350, None)),
                size_hint=(None, None), size=(400, 300))
                popup.open()
                return self.resetValueLabel(index)
        #value is ok
        if(self.shiftPressed()):
            self.updateBounds(newValue,index)
        else:
            self.setValue(newValue, index)
    
    def updateBounds(self, value, index):
        if(index): #max
            self._max = value
        else: #min
            self._min = value
        self.setValue(value, index)

    def shiftPressed(self):
        return App.get_running_app().getShiftPressed()>0
    
    def isEditable(self):
        pass

    def export(self):
        return {'name': self._name, 'unit': self._unit,'min': self.ids['slider'].value0, 'max': self.ids['slider'].value1}

class StaticConstraintWidget(ConstraintWidgetBase):
    def isEditable(self):
        return False

class EditableConstraintWidget(ConstraintWidgetBase):
    def updateName(self, newName):
        if App.get_running_app().getWidgetIndex(self) == App.get_running_app().getIndex(newName) or App.get_running_app().getIndex(newName) == -1:
            self.name = newName
        else:
            content = 'Can not change name, because of name duplication: '+str(newName)
            popup = Popup(title='Warning',
            content=Label(text=content, text_size= (350, None)),
            size_hint=(None, None), size=(400, 300))
            popup.open()
            self.name = self.ids['nameLabel'].textCache
            self.ids['nameLabel'].text = self.ids['nameLabel'].textCache

    def updateUnit(self, newUnit):
        self.unit = newUnit


    def isEditable(self):
        return True

class ConstraintsTopRow(RelativeLayout):
    pass

class ConstraintsBottomRow(BoxLayout):
    pass

######### Main  #########
if __name__ == '__main__':
    constraints = [{'name': 'Volume A','unit': 'm³', 'min': -5.0, 'max': 5.0},
                   {'name': 'Concentration e','unit': 'ppm', 'min': 0.01, 'max': 3.0},
                   {'name': 'Temperature', 'unit': 'K', 'min': -10.0, 'max': -5.0},
                   {'name': 'Reaction time', 'unit': 's', 'min': 0.01, 'max': 0.09}]
    print(ConstraintsApp().runWithOutput(constraints,constraints))

