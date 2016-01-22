

class StdoutRedirector(object):
    """
    Redirects all "print" outputs from Terminal into the Qt window
    that is given in constructor.
    """
    def __init__(self, label_obj,pyQt_app=None):
        """
        Parameters
        ----------
        label_obj : Qt-Object with config method
            Any Tkinter Object whose text can be changed over label_obj.config(text=String)
        """
        self.label_obj=label_obj
        self.pyQt_app=pyQt_app

    def write(self, out):
        """
        Method to be called by sys.stdout when text is written by print.

        Parameters
        ----------
        out : String
            Text to be printed
        """
        self.label_obj.insertPlainText(out)
        self.pyQt_app.processEvents()

    def flush(self):
        pass
