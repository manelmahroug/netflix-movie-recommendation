// replace movies array with real list of titles from csv
var movies = ["Reservoir Dogs","Lord of the Rings","The Room","Jurassic Park","Jaws"];
// var movieIndices = [];
const numInputs = 5;

d3.text("../movie_titles.csv",(e,r)=>{
    if (e) console.log(e);
    var data = d3.csvParseRows(r)
    console.log(data[0]);
    movies = data.map(d=>d[2])
    // data.forEach(d=>{movieIndices[d[2]] = +d[0]});

    for (var i=1; i<=numInputs; i++){
        autocomplete(document.getElementById(`movieInput${i}`), movies);
    }
    
})

function formHtml(num){
    return `<div class="autocomplete">
                <input id="movieInput${num}" type="text" name="movie${num}" placeholder="Type a Movie">
            </div>
            Your Rating:
            <select class="custom-select" id="rating${num}">
                <option>1</option>
                <option>2</option>
                <option>3</option>
                <option>4</option>
                <option>5</option>
            </select>                      
            <br>`
}
var $form = d3.select("#movieRatingsForm");
for (var i=1; i<=numInputs; i++){
    $form.append("div").html(formHtml(i));
}
var $responseText = d3.select("#textResponse");

d3.select("#moviesSubmit").on("click",function(event){
    d3.event.preventDefault();

    titles = [];
    ratings = [];
    for (var i=1; i<=numInputs; i++){
        titles.push(d3.select(`#movieInput${i}`).node().value.trim());
        ratings.push(+d3.select(`#rating${i}`).node().value);
    }
    console.log(titles);
    dummyResponse($responseText, titles, ratings);
})

function dummyResponse($div, tList, rList){
    arr = [];
    tList.forEach(d=>{arr.push(...d.split(" "))});
    // console.log(movieIndices[list[0]]);
    arr = arr.sort(d=>(Math.random()-0.5));
    output = "";
    arr.forEach(d=>{output += d + " "})
    // console.log(arr)
    $div.text(`Based on your input, we think you'll like "${output}". Siskel and Ebert gave it ${d3.mean(rList)} thumbs up.`)
}