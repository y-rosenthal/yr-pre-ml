# Further reading

This book teaches the parts of NumPy and pandas that you need before machine learning. These free resources go
further. None of them is needed for this book; use them when you want another explanation, more examples, or the
next step.

## NumPy (chapters 3 to 6)

- **"NumPy: the absolute basics for beginners"**, in the NumPy documentation:
  <https://numpy.org/doc/stable/user/absolute_beginners.html>. A short tour of arrays: creating them, indexing,
  arithmetic and summaries along an axis. Good for a second explanation of what the chapters on arrays teach.

## pandas (chapters 7 to 13)

- **The pandas "Getting started" tutorials**:
  <https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html>. Ten short lessons, each about one
  question ("How do I select a subset of a `DataFrame`?", "How to calculate summary statistics"), with pictures of
  the tables. Good for reviewing one topic at a time; they are written for the current version of pandas.

## Books

- **Allen Downey, *Elements of Data Science***: <https://allendowney.github.io/ElementsOfDataScience/>. A free
  book for beginners, by the author of *Think Python*, in the same style. Its chapter 3, "Lists and Arrays", and
  its chapter 7, "DataFrames and Series", cover NumPy and pandas with other examples. Its later chapters continue
  with data analysis and regression.
- **Wes McKinney, *Python for Data Analysis*, 3rd edition**: <https://wesmckinney.com/book/>. A detailed
  reference on pandas, by the person who created it, free to read online. Use it to look up a topic in depth.
  Note that some of its pandas code is older than pandas 3, so a few outputs and examples differ with the newest
  pandas (for example, text columns have the dtype `object` there, and `str` in pandas 3).
- **Jake VanderPlas, *Python Data Science Handbook***: <https://jakevdp.github.io/PythonDataScienceHandbook/>.
  Free online, with chapters on NumPy, pandas, matplotlib and machine learning with scikit-learn. Good for more
  depth on each package, and as a bridge to machine learning. It too was written for older versions of pandas.

## Machine learning

- **scikit-learn "Getting Started"**: <https://scikit-learn.org/stable/getting_started.html>. A short tour of the
  pattern that this book uses (create a model, `fit` it, `predict`), and of the next tools: pipelines, model
  evaluation and parameter searches. A good first step after this book.
