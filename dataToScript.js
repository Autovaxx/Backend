// Sample data to send to python script
let {PythonShell} = require('python-shell')

let x = '{ "employees" : [' +
'{ "firstName":"John" , "lastName":"Doe" },' +
'{ "firstName":"Anna" , "lastName":"Smith" },' +
'{ "firstName":"Peter" , "lastName":"Jones" } ]}';

const dataToScript = () => {
    // Setting options for python shell
    let options = {
        mode: 'json',
        args: [JSON.stringify(x)]
    }

    // Executing python script 
    PythonShell.run('app.py', options, (err, results) => {

        if(err){
            console.log(err)
        }
        console.log(results)
        console.log("Python script finished")
    })
}

module.exports = {dataToScript}

