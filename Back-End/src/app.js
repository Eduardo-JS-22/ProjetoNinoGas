const express = require('express');
//const routes = require('./routes');

const app = express();
//routes(app);
app.get('/teste', (req, res) => {
    res.status(200).send({ mensagem: 'Teste API Nino Gás.' });
});

module.exports = app;