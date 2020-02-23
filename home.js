var express=require('express');
var router=express.Router();

router.get('/', (req,res)=>{
	console.log("Got a request");
	res.send({name:"Shreyam"});
	// res.send("Hi");
});

module.exports=router;