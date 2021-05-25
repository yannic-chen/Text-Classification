# Text-Classification

The Text-Classification Project is a collection of softwares to handle obtainig training data to train neural networks in text classification. Here I specifically focus on news articles mentioning "Gold" in the context of Gold Price changes and predictions. This can however be changed depending on persons needs or interest.

## Extractor.py

The Extractor.py is a program that searches news articles on google and saves the relevant articles in a summary format. Multiple criteria are used to filter out irrelevant news articles.

1. The software extracts all news article it could find from google that are listed under "Gold" or "XAU" (ticker name for gold).
2. The URL of the articles are checked with URLs in the "url_done.txt" file to filter out news articles that have previously been extracted.
3. The software then checks the date of the news article (if available). If the publishing date is either "today" or "yesterday", it considers the news as "new".
4. The article then goes through a natural language processing function to create a summary and identify keywords.
5. Those keywords are then compared to a list of existing "relevant" keywords (Initially there is no a list of keywords. It needs to build up over time as more news articles has been processed). If X number of keywords match the top Y "relevant" keywords, the article is kept. Currently X = 3 and Y = 50. *Keywords can also be removed (e.g. "Standard" as in "Gold Standard"). This list of keywords is saved in a "keywords.npy"*.
6. The summary of the articles are saved in the folder "to_classify". The original full text is saved in the same folder with the prefix "full". The articles are numbered numerically. **The article with the largest number (name) should always be left inside the folder, so the software knows at which number to start numbering the articles**
7. Finally, "keywords.npy" is updated using the keywords from the accepted articles. The URL of where the news article is saved is included in the "url_done.txt" file. A log is created with the date, articles checked and added.

The articles in the "to_classify" folder are now ready to be classified.

*due to the nature of some news websites, they only update date and URL, with only small changes, thus these news articles do aggregate and create a bias of the keywords (which for now isnt a problem). Also, the url_done.txt is periodically trimmed from the top, as those URLs are likely never encountered again, to speed up the performance.*

## Categorizer.py

The Categorizer.py is a GUI software, made with Tkinter, that makes the manual classification of the "Gold" news inside the "to_classify" folder easier and faster. Given the soure folder in the text file (i.e. "to_classify"), it pickes the first articles and displays the text. After reading through the article summary text, the user decides to categorize them as **positive**, **negative** or nothing (**delete**). For the setup here, the articles will be moved to the respective folder. "pos" for positive articles and "neg" for negative articles. The Delete button removes the article.

*The output location of the positive and negative articles can be changed manually inside the code.*

## Others

* The "reference_text" folder is used to dump all the original "full" articles after the article summary has been classified into either positive or negative
* the "gold_news" folder and its .zip data are a subset of articles (237 articles) seperated into a train and validation set for training neural networks.
* The "Initiator for API.py" and "test.ipynb" are reference and testing files, and serve no other purpose. (can be deleted)
