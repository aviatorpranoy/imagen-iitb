var btn = doc.getElementByID("btn");
var res= doc.getElementByID("result");

//Display Entry Message
function display(){
    htmlString+= "<p>"+"Select upto three elements"+"</p";
    $('#success').html('htmlString');
}


//Ajax call function
btn.addEventListener("click",function() {
    var ourRequest = new XMLHttpRequest();
    ourRequest.open('GET,'data.json')
    ourRequest.onload = function(){
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData[0]);
    };
    ourRequest.send();
});

//Display Output Function (add html to the page)
function renderHTML(data){
    var htmlString="";

    //AJAX call to load data from python script
 


    //for(i=0;i<data.length;i++){
    htmlString+= "<p>"+"The constants of elasticity of "+data[i].name+", "+data[i+1].name+" and "+data[i+2].name+" is "+"</p>";

    res.insertAdjacentHTML('beforeend',htmlString);
}