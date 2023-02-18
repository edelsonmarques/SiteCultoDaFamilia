const http = require('http');
const express = require('express');
const session = require('express-session');
const path = require('path');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const bcrypt = require('bcrypt');
const nunjucks = require('nunjucks');

const port = 3000;
const app = express();

nunjucks.configure('cultoparacasais/views', {
    autoescape: true,
    express: app,
    watch: true,
});


app.use(express.json());
app.use(express.static('express'));
app.use(session({ secret: '123456'}));

// URL padrão do site
app.use(bodyParser.urlencoded({extended: true}));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use('/cultoparacasais', express.static(path.join(__dirname, 'cultoparacasais')));
app.use('/register', express.static(path.join(__dirname, 'cultoparacasais/register.html')));
// app.use('/', (req, res) => {
//     res.sendFile(path.join(__dirname+'/cultoparacasais/index.html'));
// });
app.set('views', path.join(__dirname, '/cultoparacasais/views'));
// app.set('css', path.join(__dirname, '/cultoparacasais/src/css'));
// app.set('js', path.join(__dirname, '/cultoparacasais/src/js'));
// app.set('db', path.join(__dirname, '/cultoparacasais/src/db'));

app.post('/', (req, res) => {
    if(req.body.register_page){
        var reporter = {};
        reporter["Username"] = req.body.username;
        return res.render('register', {Reporter: reporter});
        
    } else

    if(req.body.recover_page){
        var reporter = {};
        reporter["Username"] = req.body.username;
        return res.render('recover', {Reporter: reporter});
        
    } else

    if(req.body.register){
        db = getDb();
        try{
            db.all(`SELECT * FROM user WHERE username = ?`, [req.body.username], (err, results) => {
                if (err) {
                    console.log('Erro dentro do exec: ' + err.message);
                }
                if (results.length > 0) {
                    console.log('Usuário já cadastrado!');
                    var reporter = {};
                    reporter["Username"] = req.body.username;
                    reporter["Registed"] = "Usuário já cadastrado!";
                    return res.render('register', {Reporter: reporter});
                } else {
                    bcrypt.hash(req.body.password, 10, (errBcrypt, hash) =>{
                        if (errBcrypt){ return console.log('Erro dentro do hash: ' + errBcrypt.message); }
                        // console.log('Executando o hash: ');
                        // console.log('password: ' + hash);
                        
                        db.run(`INSERT INTO user (username, password) VALUES (?, ?)`, [req.body.username, hash], function(err){
                            if (err) {
                                return console.log('Erro dentro do run: ' + err.message);
                            } 
                            console.log(`A row has been inserted with rowid ${this.lastID}`);
                        });
        
                        db.all(`SELECT * FROM user`, [], (err, rows) => {
                            if (err) {
                                return console.log('Erro dentro do each: ' + err.message);
                            }
                            rows.forEach((row) => {
                                console.log(row.id + "\t" + row.username + "\t" + row.password);
                              });
                        });
                    });
                }
                return res.render('index');        
            });
        } catch (e) {
            console.log('Erro dentro do try: ' + e.message);
        }
    } else
    
    if(req.body.recover){
        db = getDb();
        try{
            db.all(`SELECT * FROM user WHERE username = ?`, [req.body.username], (err, results) => {
                if (err) {
                    console.log('Erro dentro do exec: ' + err.message);
                }
                if (results.length > 0) {
                    bcrypt.hash(req.body.password, 10, (errBcrypt, hash) =>{
                        if (errBcrypt){ return console.log('Erro dentro do hash: ' + errBcrypt.message); }
                        // console.log('Executando o hash: ');
                        // console.log('password: ' + hash);
                        
                        db.run(`UPDATE user set password = ? WHERE username = ?`, [hash, req.body.username], function(err){
                            if (err) {
                                return console.log('Erro dentro do run: ' + err.message);
                            } 
                            console.log(`Row(s) updated: ${this.changes}`);
                        });
        
                        db.all(`SELECT * FROM user`, [], (err, rows) => {
                            if (err) {
                                return console.log('Erro dentro do each: ' + err.message);
                            }
                            rows.forEach((row) => {
                                console.log(row.id + "\t" + row.username + "\t" + row.password);
                              });
                        });
                    });
                } else {
                    console.log('Usuário não encontrado!');
                    var reporter = {};
                    reporter["Username"] = req.body.username;
                    reporter["Recover"] = "Usuário não encontrado!";
                    return res.render('recover', {Reporter: reporter});
                }
                return res.render('index');        
            });
        } catch (e) {
            console.log('Erro dentro do try: ' + e.message);
        }
    } else
    
    if (req.body.login) {
        if (true){
            db = getDb();
            try{
                db.all(`SELECT * FROM user WHERE username = ?`, [req.body.username], (err, results) => {
                    if (err) {
                        console.log('Erro dentro do exec: ' + err.message);
                        return res.render('index');  
                    }
                    var reporter = {};
                    reporter["Username"] = req.body.username;
                    if (results.length > 0) {
                        bcrypt.compare(req.body.password, results[0].password, (errBcrypt, result) =>{
                            if (errBcrypt){ return console.log('Erro dentro do compare: ' + errBcrypt.message); }
                            if (result){
                                req.session.numId = results[0].id;
                                req.session.login = req.body.username;
                                return res.render('home', {Reporter: reporter});
                            }
                            reporter["Registed"] = "Username/password não conferem!";
                            return res.render('index', {Reporter: reporter});
                            
                        });
                    } else {
                        reporter["Registed"] = "Username não encontrado!";
                        return res.render('index', {Reporter: reporter});      
                    }
                          
                });
            } catch (e) {
                console.log('Erro dentro do try: ' + e.message);
            }
            
        } else{
            var error = '';
            return res.render('index', {error: error});
        }
    } else

    if (req.body.logout) {
        delete req.session.login;
        return res.render('index');
    } else 
    
    if (req.body.reset) {
        db = getDb();
        try{
            db.all(`SELECT p.id, author_id, bolasDoBingoJson, rankingJson, username 
                    FROM bolasDoBingo p JOIN user u ON 
                    p.author_id = ? AND u.id = ?`, [req.session.numId, req.session.numId], (err, results) => {
                if (err) {
                    console.log('Erro dentro do exec: ' + err.message);
                }
                if (results.length > 0) {
                    
                    var bolasDoBingo = JSON.parse(results[0].bolasDoBingoJson.replaceAll("'",'"'));
                    var confAPI = [''];
                    if (bolasDoBingo.ConfAPI){
                        confAPI = bolasDoBingo.ConfAPI;
                    }
                    var jsonMontado = { ConfAPI: confAPI,
                        ListaGeral: [],
                        ListaVisitante: [],
                        ListaMenor: [],
                        ListaDinamica: [],
                        ListaNiverCasamento: [],
                        ListaEnsaio: [],
                        MesSorteio: [],
                        ListaMesSorteio: [],
                        NomeSorteadoAnterior: [],
                        NomeSorteado: [],
                        Opcao: [],
                        Proximo: [],
                        Ensaio: [],
                        HabilitarEnsaio: []
                    }
                    jsonMontado = JSON.stringify(jsonMontado);
                    db.run(`UPDATE bolasDoBingo SET bolasDoBingoJson = ?, author_id = ? 
                            WHERE id = ?`, [jsonMontado, req.session.numId, req.session.numId], function(err){
                                if (err) {
                                    return console.log('Erro dentro do run: ' + err.message);
                                } 
                                console.log(`Row(s) updated: ${this.changes}`);
                            });
                    
                } else {
                    console.log('Não conseguimos localizar o id do usuário!!!');
                }
                var reporter = {};
                reporter["Username"] = req.session.login;
                return res.render('home', {Reporter: reporter});        
            });
        } catch (e) {
            console.log('Erro dentro do try: ' + e.message);
        }


    
    } else 
    
    if (req.body.config) {
        db = getDb();
        try{
            db.all(`SELECT p.id, author_id, bolasDoBingoJson, rankingJson, username 
                    FROM bolasDoBingo p JOIN user u ON 
                    p.author_id = ? AND u.id = ?`, [req.session.numId, req.session.numId], (err, results) => {
                if (err) {
                    console.log('Erro dentro do exec: ' + err.message);
                }
                if (results.length > 0) {
                    
                    var bolasDoBingo = JSON.parse(results[0].bolasDoBingoJson.replaceAll("'",'"'));
                    results[0].bolasDoBingoJson = bolasDoBingo;
                    if (bolasDoBingo.ConfAPI != []){
                        confAPI = bolasDoBingo.ConfAPI;
                    }
                    
                } else {
                    console.log('Não conseguimos localizar o id do usuário!!!');
                }
                var reporter = {};
                reporter["Username"] = req.session.login;
                reporter['bolas'] = results[0];
                return res.render('config', {Reporter: reporter});        
            });
        } catch (e) {
            console.log('Erro dentro do try: ' + e.message);
        }
    } 
    
    else {
        res.render('index');
    }
});

app.get('/', (req, res) => {
    if (req.session.login){
        res.render('home', {login: req.session.login});
    }else{
        res.render('index');
        }
});

app.get('/register.html', (req, res) => {
    res.render('register');
});

app.post('/register.html', (req, res) => {
    console.log(req.body);
    if(req.body.register){
        db = db.getDb();
        console.log(db);
        db.serialize(() => {
            db.each(`SELECT * FROM user`, (err, row) => {
                if (err) {
                console.error(err.message);
                }
                console.log(row.id + "\t" + row.username);
            });
        });
    }
    res.render('index'); 
});


// setTimeout(() => {  console.log(db); }, 50);

function getDb(){
    let db = new sqlite3.Database('./cultoparacasais/src/db/flaskr.sqlite', (err) => {
        if (err) {
          console.error(err.message);
        }
        // console.log('Connected to the database.');
    });
    return db;
}

const server = http.createServer(app);
server.listen(port);

console.debug('Server inicializado na porta ' + port);