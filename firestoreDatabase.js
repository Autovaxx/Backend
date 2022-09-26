const admin = require('firebase-admin')
const serviceAccount = require('./serviceAccountKeys.json');
const { QuerySnapshot } = require('@google-cloud/firestore');

// Connecting to Firestore DB
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// Storing collection to variable
let sampleData = db.collection('users')


// Fetching entire user collection from DB
const returnUserData = async () => { 
    
    const userData = []
    // Logging data to console and storing it in an array
    await sampleData.get().then((querySnapshot) =>[
        querySnapshot.forEach(document => {
            userData.push(document.data())
    
        })
        
    ])

    console.log(userData)
    
    return userData
}

module.exports = {returnUserData};