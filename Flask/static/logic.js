// replace movies array with real list of titles from csv
// var movies = ["Reservoir Dogs","Lord of the Rings","The Room","Jurassic Park","Jaws"];
var movies = [];
var movieIndices = {};
const numInputs = 5;

d3.text("static/movie_titles.csv",(e,r)=>{
    if (e) console.log(e);
    var data = d3.csvParseRows(r)
    console.log(data[0]);
    movies = data.map(d=>d[2])
    data.forEach(d=>{movieIndices[d[2]] = +d[0]});

    
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
var $responseList = d3.select("#listResponse");

d3.select("#moviesSubmit").on("click",function(event){
    d3.event.preventDefault();

    titles = [];
    ratings = [];
    for (var i=1; i<=numInputs; i++){
        titles.push(d3.select(`#movieInput${i}`).node().value.trim());
        ratings.push(+d3.select(`#rating${i}`).node().value);
    }
    console.log(titles);
    // dummyResponse($responseText, titles, ratings);
    recommend($responseText, $responseList, titles, ratings);
})

function recommend($div, $uldiv, tList, rList){
    console.log(`'/predict/${getEndPoint(tList,rList)}'`)
    $div.text(`Calculating movies...`);
    // Assuming the Flask endpoint returns a JSON array of titles
    d3.json(`/predict/${getEndPoint(tList,rList)}`,(e,d)=>{
        if (e) console.warn(e);
        console.log(d);
        
        $div.text(`Based on your input, we recommend the movies:`);
        recList($uldiv, d);
    })
}

function recList($div, mList){
    // console.log($div.attr("id"))
    $div.html("").selectAll("ul").data(mList).enter().append("ul").text(d=>movies[d-1]);
}

function getEndPoint(tList, rList){
    var endpoint = ""
    // console.log(tList.map((d,i)=>[movieIndices[d],rList[i]]));
    tList.forEach((d,i)=>{
        var mi = movieIndices[d];
        // Currently this returns -1 for an unknown movie input. 
        if (!mi) {
            mi = -1;
            console.log(`Didn't recognize movie "${d}"`);
        }
        endpoint+=`${mi}:${rList[i]},`;
    })
    return endpoint
}

function dummyResponse($div, tList, rList){
    arr = [];
    tList.forEach(d=>{arr.push(...d.split(" "))});
    // console.log(movieIndices[list[0]]);
    arr = arr.sort(d=>(Math.random()-0.5));
    output = "";
    arr.forEach(d=>{output += d + " "})
    // console.log(arr)
    $div.text(`Based on your input, we think you'll like "${output}". Siskel and Ebert gave it ${d3.mean(rList)} thumbs up.`)
    
    console.log(`I'ma scrape some datums from '/predict/${getEndPoint(tList,rList)}'!`);
}