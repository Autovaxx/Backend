const admin = require("firebase-admin");
const serviceAccount = require("./service_account_keys.json");
const { getAuth } = require("firebase-admin/auth");

// Sample UID
const userID = "G5VVteOsqpaT46mpQvxDOxU1iD93";

// Connecting to Firestore DB
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

// Creating a DB object allowing us to access DB and DB functions
const db = admin.firestore();

// Getting all the data within a single document
const getSingleDocumentData = async (uid) => {
  let userData;

  await db
    .collection("users")
    .doc(uid)
    .get()
    .then((doc) => {
      userData = doc.data();
    });

  return userData;
};

// NOTE: THESE ARE ALL EXTRAS. NOT USED.

// Fetches all the nested collection document data of user document
const returnUserData = async () => {
  // Storing user data here
  const userData = [];

  // Getting all the collection names
  const userCollectionNames = await getUserCollections(userID);

  // Cycling through the collection names, fetching the document data and storing the document data in the userData array
  for (const collectionName of userCollectionNames) {
    const singleDocument = await getSingleDocumentData(collectionName);

    userData.push(singleDocument);
  }

  // Returning the user data
  return userData;
};

// Gets all the collections associated to a specific userID and returns an array containing the collection IDs
const getUserCollections = async (userID) => {
  const userCollectionID = [];

  // Targeting the document associated with a specific userID
  const userDocTest = db.collection("users").doc(userID);

  // Fetching all the user collections associated with the ID
  const userCollections = await userDocTest.listCollections();

  // Storing collection IDs in the array
  userCollections.forEach((collection) => {
    userCollectionID.push(collection.id);
  });

  // Returning the collection name list
  return userCollectionID;
};

const updateDocumentAppointment = async (
  vaccineName,
  dateTimeApt,
  pharmacyApt,
  pharmacyAddr,
  pharmacyPCodeCity,
  UID
) => {
  await db
    .collection("users")
    .doc(UID)
    .update({
      appointment: [
        {
          booked: true,
          vaccine: vaccineName,
          dateTime: dateTimeApt,
          pharmacy: pharmacyApt,
          pharmacy_address: pharmacyAddr,
          pharmacy_address_pcode_city: pharmacyPCodeCity,
        },
      ],
    });
};

module.exports = { getSingleDocumentData, updateDocumentAppointment };
