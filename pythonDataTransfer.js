

const getPythonData = () => {
    const pythonOutput = spawn('python', ['app.py'])

    console.log(pythonOutput.toString())
}


// const getPythonData = async () => {
    
//     let myjson = ""

//     // pythonProcess.stdout.on('data',  (data) => {
//     //     mystr = data.toString()
        
//     //     myjson = JSON.parse(mystr)
    
//     //     console.log(`JSON IS: ${myjson}`)
        
        
//     // })
//     return myjson
// }

module.exports = {getPythonData}
