import time
from tkinter import *
import tkinter.messagebox
from nltk.sentiment.vader import SentimentIntensityAnalyzer


class TextDetector:
    def center(self, toplevel):
        """Centers the Tkinter window on the screen."""
        toplevel.update_idletasks()
        w = toplevel.winfo_screenwidth()
        h = toplevel.winfo_screenheight()
        size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
        x = int(w / 2 - size[0] / 2)
        y = int(h / 2 - size[1] / 2)
        toplevel.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

    def callback(self):
        """Callback to confirm closing the application."""
        if tkinter.messagebox.askokcancel("Quit", "Do you want to leave?"):
            self.main.destroy()

    def setResult(self, sentiment_type, res):
        """Displays the sentiment percentages."""
        if sentiment_type == "neg":
            self.negativeLabel.configure(text=f"Negative comment: {res * 100:.2f}%")
        elif sentiment_type == "neu":
            self.neutralLabel.configure(text=f"Neutral comment: {res * 100:.2f}%")
        elif sentiment_type == "pos":
            self.positiveLabel.configure(text=f"Positive comment: {res * 100:.2f}%")

    def detectText(self):
        """Detects and displays the entered text."""
        text = self.text_widget.get("1.0", END).strip()
        if not text:
            self.detectedText.configure(text="No text entered. Please type something.")
        else:
            self.detectedText.configure(text=f"Detected text:\n{text}")

    def runAnalysis(self):
        """Performs sentiment analysis on the entered text."""
        text = self.text_widget.get("1.0", END).strip()
        if not text:
            self.normalLabel.configure(text="Please type some text!")
            return

        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(text)

        if ss['compound'] >= 0.05:
            self.normalLabel.configure(text="The overall sentiment is Positive.")
        elif ss['compound'] <= -0.05:
            self.normalLabel.configure(text="The overall sentiment is Negative.")
        else:
            self.normalLabel.configure(text="The overall sentiment is Neutral.")

        for sentiment, score in sorted(ss.items()):
            self.setResult(sentiment, score)

    def addNewLine(self, event):
        """Allows adding new lines with the Enter key."""
        self.text_widget.insert(END, "\n")
        return "break"  # Prevents the default Enter key behavior

    def __init__(self):
        """Initializes the Tkinter GUI."""
        self.main = Tk()
        self.main.title("Text Detector and Sentiment Analyzer")
        self.main.geometry("600x700")
        self.main.resizable(width=False, height=False)
        self.main.protocol("WM_DELETE_WINDOW", self.callback)
        self.center(self.main)

        # Input Section
        self.label1 = Label(self.main, text="Type your text here (press Enter to add a new line):")
        self.label1.pack()

        self.text_widget = Text(self.main, height=10, width=70, wrap=WORD)
        self.text_widget.pack()
        self.text_widget.bind("<Return>", self.addNewLine)

        # Buttons for detection and analysis
        self.detect_button = Button(self.main, text="Detect Text", command=self.detectText)
        self.detect_button.pack(pady=5)

        self.analyze_button = Button(self.main, text="Analyze Sentiment", command=self.runAnalysis)
        self.analyze_button.pack(pady=5)

        # Output Section: Detected text
        self.detectedText = Label(self.main, text="", font=("Helvetica", 12), fg="blue", wraplength=500, justify=LEFT)
        self.detectedText.pack(pady=10)

        # Output Section: Sentiment analysis results
        self.result = Label(self.main, text="\nSentiment Analysis Results\n", font=("Helvetica", 15))
        self.result.pack()

        self.negativeLabel = Label(self.main, text="", fg="red", font=("Helvetica", 20))
        self.negativeLabel.pack()

        self.neutralLabel = Label(self.main, text="", font=("Helvetica", 20))
        self.neutralLabel.pack()

        self.positiveLabel = Label(self.main, text="", fg="green", font=("Helvetica", 20))
        self.positiveLabel.pack()

        self.normalLabel = Label(self.main, text="", fg="black", font=("Helvetica", 20))
        self.normalLabel.pack()


# Driver code
if __name__ == "__main__":
    my_analysis = TextDetector()
    mainloop()
