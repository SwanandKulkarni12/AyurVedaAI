const express = require("express");
const app = express();
const bodyParse = require("body-parser");
const User = require('./Model/User');
const mongoose = require("mongoose");
const  bcrypt=require('bcrypt')
const session = require("express-session");
mongoose
  .connect("mongodb://127.0.0.1:27017/authentication", {
 
    useNewUrlParser: true,
  })
 

app.use(express.static("public"));
app.use(bodyParse.urlencoded({ extended: true }));

app.get("/", function(request, response) {
    response.sendFile(__dirname + "/Home.html");
});

app.get("/quiz", function(request, response) {
    response.sendFile(__dirname + "/views/Quiz.html");
});
app.get("/chat", function(request, response) {
    response.sendFile(__dirname + "/views/Chatbot.html");
});


app.get("/views/Login.html", function(request, response) {
    response.sendFile(__dirname + "/views/Login.html");
});

app.listen(3000, function(req, res) {
    console.log("Server running on port 3000");
});
app.post('/views/Login.html', async (req, res) => {
  
    // validate input fields
    const { username, email, phone, password,action,Prakriti} = req.body;
    console.log(action)
    if(action=='Login')
    {
      console.log(username,password)
      User.findOne({ /* Your query criteria */ })
  .then( async user => {
    // Handle the result here
    const isMatch = awaitbcrypt.compare(password, user.password);
    if (!isMatch) {
      console.log("Wrong Password");
      res.render(__dirname + '/views/Form',{
        errorMsg:"Wrong Credentials"
      });
    }
   
    else
    {
      req.session.userId=username;
  req.session.username=username;
  req.session.msg='Login Successful'
  res.redirect('/success')
  
  
    }
  })
  .catch(error => {
    // Handle any errors here
  });
      
    }
    else
    {
      console.log(email)
      console.log(password);
      const hashedPassword =  await bcrypt.hash(password, 10);
      if(Prakriti)
        req.session.Prakriti=Prakriti;
      // create new user object
      const user = new User({
        username,
        email,
        phone,
        password: hashedPassword,
        Prakriti:Prakriti
      });
  
      // save user to database
      user.save();
  
      // send success response
      res.redirect('/')
     
    }
});