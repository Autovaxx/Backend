const express = require('express');
const app = express();
const port = 8080;
const dbFunctions = require('./firestoreDatabase')
const pythonDataTransfer = require('./pythonDataTransfer')
const {spawn} = require('child_process');

// Need to async/await for this to work properly since it takes time to execute. 
const x = dbFunctions.returnUserData()

// Sample root api for port 8080
app.get('/',  (req, res) => {

    const pythonOutput = spawn('python', ['app.py'])

    let dataFromPython;

    // Executes the python script and stores the data
    pythonOutput.stdout.on('data', (data) => {

        console.log("pipe data from python script")
        
        dataFromPython = data.toString()
    })
    
    // Once the python script is finished executing, closes I/O streams and sends data from script to server endpoint
    pythonOutput.on('exit', (code) => {
        console.log(`EXIT CODE: ${code}`)

        res.send(dataFromPython)
    } )
})

// Starting the server
app.listen(process.env.PORT || port, () => {
    console.log("Server is running");
  });
