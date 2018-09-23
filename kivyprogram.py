'''
Mesh test
=========

This demonstrates the use of a mesh mode to distort an image. You should see
a line of buttons across the bottom of a canvas. Pressing them displays
the mesh, a small circle of points, with different mesh.mode settings.
'''

from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class Container(GridLayout):
    pass


class MyKiviApp(App):

    def build(self):
        self.title = 'Awesome app!!!'
        return Container()

if __name__ == "__main__":
    app = MyKiviApp()
    app.run()
    