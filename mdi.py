from wxPython.wx import *

# Subclass wxMDIParentFrame

class Parent ( wxMDIParentFrame ):

   def __init__ ( self ):
      # Call __init__ and make the window big
      wxMDIParentFrame.__init__ ( self, None, -1, "Multiple Document Interface Test", size = ( 500, 500 ) )
      # Create a menu that allows us to open new windows
      windowMenu = wxMenu()
      windowMenu.Append ( 1, 'Open New' )
      # Create a menu bar and add the menu
      menuBar = wxMenuBar()
      menuBar.Append ( windowMenu, 'Options' )
      self.SetMenuBar ( menuBar )
      # Catch a menu click
      EVT_MENU ( self, 1, self.openNew )
      self.Show ( True )

   # This method will add a window
   def openNew ( self, event ):
      # Create a child window
      child = wxMDIChildFrame ( self, -1, 'MDI Child' )
      # Give the child a panel
      child.panel = wxPanel ( child, -1 )
      child.panel.SetSize ( child.GetClientSize() )
      # Add a label
      child.label = wxStaticText ( child, -1, 'I am only a child.' )
      child.Show ( True )

application = wxPySimpleApp()
Parent()
application.MainLoop()
