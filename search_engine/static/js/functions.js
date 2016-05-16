// function toggleVisibility(div_id){
//     var div = document.getElementById(div_id);
//     div.style.display = div.style.display == "block" ? "none" : "block";
// }

function goBack() {
    window.history.back();
}

function loadCharts(){
    google.charts.load('current', {'packages':['corechart']});
}

function drawPieChart(title, total_words, total_ents, name, div_id){
    
    
    
    google.charts.setOnLoadCallback(drawChart);
    

    function drawChart() {
    
        var data = google.visualization.arrayToDataTable([
            ['Words', 'Count'],
            [name,     total_ents],
            ['Other Words',      (total_words - total_ents)]
        ]);
        
        var options = {
            title: title
        };
        
        var chart = new google.visualization.PieChart(document.getElementById(div_id));
        
        chart.draw(data, options);
    }
}
