// Server For Craigslist Prices

const Express = require("express");
const BodyParser = require("body-parser");
const MongoClient = require("mongodb").MongoClient;
const ObjectId = require("mongodb").ObjectId;
const { request } = require("express");

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
    });
});

// post array of prices
app.post("/bike", (request, response) => {
    console.log("post body:", request.body);
    collection.insertOne(request.body, (error, result) => {
        if (error) {
            return response.status(500).send(error);
        }
        response.send(result.result);
    });
});

// get an entry by id
app.get("/bike/:id", (request, response) => {
    console.log("findOne id:", request.params);

    collection.findOne({ "_id": new ObjectId(request.params.id) }, (error, result) => {
        if (error) return response.status(500).send(error);
        response.send(result);
    });
});

/* wip, will need to convert collection name to data or something not specific like bike
// http://127.0.0.1:5000/data?category=bicycles&area=orangecounty&analytics=["mean", "median", "mode"]
app.get("/data*", async (request, response) => {
    console.log("data query before", request.query);
    var analytics = request.query.analytics;
    delete request.query.analytics;
    console.log("data query after", request.query, {analytics});
    const prices = await collection.find(request.query);
    console.log(prices);

    //if( request.query.analytics ) {

    //}
});
*/

// get an entry by query
app.get("/bike*", (request, response) => {
    console.log("find query:", request.query, request.body);
    collection.find(request.query).toArray((error, result) => {
        if (error) {
            return response.status(500).send(error);
        }
        response.send(result);
    });
});

// delete by query, if {removeEmpty : true}, remove all values without category
app.delete("/bike*", async (request, response) => {
    console.log("delete query:", request.query);
    var res;
    if(request.query.removeEmpty) {
        res = await collection.deleteMany({category : null});
    } else {
        res = await collection.deleteMany(request.query);
    }
    response.send("Deleted:" + res.deletedCount);
});
