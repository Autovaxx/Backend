const express = require('express');
const app = express();
const port = 8080;
const dbFunctions = require('./firestoreDatabase')
const dataToScript = require('./dataToScript')

// Need to async/await for this to work properly since it takes time to execute. 
// If you try to console log x right away it'll be blank because it exectues faster than the script 
const x = dbFunctions.returnUserData()

dataToScript.dataToScript()

// Sample root api for port 8080
app.get('/', (req, res) => {

    res.send("hello")
})

// Starting the server
app.listen(process.env.PORT || port, () => {
    console.log("Server is running");
  });