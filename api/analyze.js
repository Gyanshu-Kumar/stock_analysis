const express = require('express');
const { exec } = require('child_process');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const pythonPath = '"C:\\Users\\GYANSHU KUMAR\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"';

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/api/analyze', (req, res) => {
    const { year } = req.body;

    const command = `${pythonPath} ../python/analyze_stocks.py ${year}`;
    exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).send(`Error: ${error.message}`);
        }
        if (stderr) {
            console.error(`stderr: ${stderr}`);
            return res.status(500).send(`Stderr: ${stderr}`);
        }
        console.log(`stdout: ${stdout}`);
        res.send(`<pre>${stdout}</pre>`);
    });
});

module.exports = app;
