const express = require('express');
const app = express();
const port = 8080;
const {spawn} = require('child_process');
const dbFunctions = require('./firestore_database')

app.use(express.json())
app.use(express.urlencoded({ extended: true })); 

app.post("/", async (req, res) => {

    console.log('Checking duplicate req: ', req.url)
    let pythonScriptData;

    const uid = req.body.UID

    const userData = await dbFunctions.getSingleDocumentData(uid)

    console.log(typeof(userData))

    // Python Input Starts here
    pythonInputData = JSON.stringify(userData)

    console.log(pythonInputData)

    const pythonSpawn= spawn('python', ['booking_script/main.py', pythonInputData])
    //const pythonSpawn= spawn('python', ['collect_user_data.py', pythonInputData])
   
    pythonSpawn.stdout.on('data', (data) => {
        console.log(`python data: ${data}`)
        
        if(data != null || data != undefined){
            pythonScriptData += data
        }
    })

    // Once the python script is finished executing, closes I/O streams. Will display error msg if there is one
    // Exit code 0 means successful run, otherwise fail.
    pythonSpawn.on('exit', (code) => {
        console.log(`EXIT CODE: ${code}`)
        
        // Manipulating the returned python data to a usable format
        pythonScriptData = pythonScriptData.split(/\r?\n/)
        pythonScriptData.splice(1, 1)
        pythonScriptData.splice(2, 1)
        pythonScriptData[0] = pythonScriptData[0].replace('undefined', "")

        console.log(pythonScriptData)
        
        const dataToAptRecord = {
            booked: true,
            vaccine: pythonScriptData[0],
            dateTime: pythonScriptData[1],
            pharmacy: pythonScriptData[2],
            pharmacy_address: pythonScriptData[3],
            pharmacy_address_pcode_city: pythonScriptData[4]
        }

        dbFunctions.updateDocumentAppointment(
            dataToAptRecord.vaccine,
            dataToAptRecord.dateTime,
            dataToAptRecord.pharmacy,
            dataToAptRecord.pharmacy_address,
            dataToAptRecord.pharmacy_address_pcode_city,
            uid
        )

        if (code > 1) {
            pythonSpawn.stderr.on('data', data => {
                console.log(`ERROR: ${data}`)
                
            })
        }
        //res.send(dataFromPython)
    } )

    

    
})

// Starting the server
app.listen(process.env.PORT || port, () => {
    console.log("Server is running");
  });
