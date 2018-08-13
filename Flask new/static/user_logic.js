var movies = [];
var movieIndices = {};
const numInputs = 5;

d3.text("static/movie_titles.csv",(e,r)=>{
    if (e) console.log(e);
    var data = d3.csvParseRows(r)
    console.log(data[0]);

    movies = data.map(d=>d[2])
    data.forEach(d=>{movieIndices[d[2]] = +d[0]});
})

var $responseText = d3.select("#textResponse");
var $responseList = d3.select("#listResponse");

d3.select("#userSubmit").on("click",function(event){
    d3.event.preventDefault();

    user = d3.select("#userSelect").node().value.trim()
    console.log(user)

    d3.json(`/user/${getUID(user)}`,(e,d)=>{
        if (e) console.warn(e);
        console.log(d);
        
        $responseText.text(`Based on your input, we recommend the movies:`);
        recList($responseList, d);
    })
})

function getUID(text){
    return text.split(" ").pop()
}

function recList($div, mList){
    // console.log($div.attr("id"))
    $div.html("").append("ul").selectAll("li").data(mList).enter().append("li").text(d=>movies[d-1]);
}
