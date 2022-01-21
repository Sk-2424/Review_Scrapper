from flask import Flask, render_template, request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
# import pymongo

app = Flask(__name__)

@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')


@app.route('/scrap', methods=['GET', 'POST'])
def webscrapping():
    if(request.method == 'POST'):
        searchString =  request.form['content'].replace(" ", "")
        try:
            # myConn = pymongo.MongoClient("mongodb://localhost:27017/")
            # mydb = myConn['crawler']
            # reviews = list(mydb[searchString].find({}))
            # if len(reviews) > 0:
            #     return render_template('result.html', reviews=reviews)
            # else:
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            uData = uClient.read()
            FlipkartData = bs(uData,"html.parser")
            BigBoxes = FlipkartData.findAll("div", {"class": "_2kHMtA"})
            count_BigBoxes = len(list(BigBoxes))
            # table = mydb[searchString]
            reviews = []
            for i in range(0, 5):
                productUrl = flipkart_url + BigBoxes[i].a['href']
                uProduct = uReq(productUrl)
                uProductData = uProduct.read()
                Bs_ProductData = bs(uProductData, "html.parser")
                reviewbox = Bs_ProductData.findAll('div', {"class": "col _2wzgFH"})
                count_reviewbox = len(list(reviewbox))
                for i in range(0, count_reviewbox):
                    try:
                        comment = reviewbox[i].findAll('div', {"class": ""})[0].findAll('div', {"class": ""})[0].text
                    except:
                        comment = 'no Comment present'
                    try:
                        commenthead = reviewbox[i].p.text
                    except:
                        commenthead = 'No CommentHead present'
                    try:
                        name = reviewbox[i].findAll('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    except:
                        name = 'No name Present'
                    try:
                        rating = reviewbox[i].findAll('div', {'class': '_3LWZlK _1BLPMq'})[0].text
                    except:
                        rating = 'No rating'

                    mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commenthead,
                              "comment": comment}
                    # table.insert_one(mydict)
                    reviews.append(mydict)
            return render_template('result.html', reviews=reviews)
        except:
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)


