// Server To Post Price Arrays

const Express = require("express");
const BodyParser = require("body-parser");
const MongoClient = require("mongodb").MongoClient;
const ObjectId = require("mongodb").ObjectId;

const CONNECTION_URL = "mongodb+srv://zach:boom@cluster0.yd09t.mongodb.net/${dbName}?retryWrites=true&w=majority";
const DATABASE_NAME = "craigslist";


var app = Express();
app.use(BodyParser.json());
app.use(BodyParser.urlencoded({extended: true}));

var database, colleciton;

app.listen(5000, () => {
    MongoClient.connect(CONNECTION_URL, {useNewUrlParser: true }, (error, client) => {
        if (error) {
            throw error;
        }
        database = client.db(DATABASE_NAME);
        collection = database.collection("bike");
        console.log("Connected to: " + DATABASE_NAME);
    })
});

// post array of prices
app.post("/bike", (request, response) => {
    console.log("Posting", request.body);
    collection.insertOne(request.body, (error, result) => {
        if (error) {
            return response.status(500).send(error);
        }
        response.send(result.result);
    })
});

// todo app.get