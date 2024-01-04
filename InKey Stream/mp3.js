const express = require('express');
const trackRoute = express.Router();
var filename = "if_i_cant.mp3"

/**
 * NodeJS Module dependencies.
 */
const { Readable } = require('stream');

const app = express();

trackRoute.get('/', (req, res) => {

    res.set('content-type', 'audio/mp3');
    res.set('accept-ranges', 'bytes');

    let downloadStream = bucket.openDownloadStream(filename);
  
    downloadStream.on('data', (chunk) => {
        res.write(chunk);
    });
  
    downloadStream.on('error', () => {
        res.sendStatus(404);
    });
  
    downloadStream.on('end', () => {
        res.end();
    });
});

app.listen(3005, () => {
    console.log("App listening on port 3005!");
});