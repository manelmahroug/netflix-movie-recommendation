// replace movies array with real list of titles from csv
var movies = ["Reservoir Dogs","Lord of the Rings","The Room","Jurassic Park","Jaws"];
d3.text("../movie_titles.csv",(e,r)=>{
    var data = d3.csvParseRows(r)
    console.log(data[0]);
    movies = data.map(d=>d[2])

    initForm(5);
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

function initForm(n){
    for (var i=1; i<=n; i++){
        $form.append("div").html(formHtml(i))
        autocomplete(document.getElementById(`movieInput${i}`), movies);
    }
}