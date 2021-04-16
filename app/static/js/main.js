let default_reach_data = [{
    name: "sample1",
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16],
}]
let default_reach_layout = {
    xaxis : { title : 'コスト(円) × 1,000,000'},
    yaxis : { title : '$リーチ × 1,000,000'},
    margin: { t: 0 },
}

let default_budget_data = [{
    name: "sample2",
    type: "waterfall",
    orientation: "v",
    measure: [
        "relative",
        "relative",
        "relative",
        "total",
    ],
    x: [
        "Twitter",
        "Youtube",
        "Facebook",
        "TotalBudget",
    ],
    textposition: "outside",
    text: [
        "50",
        "30",
        "20",
        "Total"
    ],
    y: [
        50,
        30,
        20,
        0
    ],
}];

let default_budget_layout = {
    margin: { t: 0 },
    xaxis: {
        title: "媒体名",
        type: "category"
    },
    yaxis: {
        title: "予算(円) × 1,000,000",
        type: "linear"
    },
    autosize: true,
    showlegend: false
};

Plotly.newPlot(
    "reach-simulator",
    default_reach_data,
    default_reach_layout
    );

Plotly.newPlot(
    "budget-optimizer",
    default_budget_data,
    default_budget_layout
)

$("#btn-simulation").click(function (event) {
    event.preventDefault();
    let form = $("#form-simulation")
    let params = form.serializeJSON();
    console.log(params);

    $.post({
        data: JSON.stringify(params),
        url: form.attr("action"),
        contentType: 'application/json',
    }).done(function (data){
        Plotly.newPlot(
            "reach-simulator",
            JSON.parse(data.graph)[0].data,
            JSON.parse(data.graph)[0].layout
        );
        let strObj = document.getElementById("sample")
        strObj.innerHTML =
            "<p class=h2>" + "広告予算" + params.budget + "円を消化すると" +
            Math.round(data.reach) + "人にリーチできると推測されます" + "</p>"
    })
})

$("#media-checkbox").on("change", function (_event){
    const limit = 1
    const button = $('#btn-optimization');
    let checked = $("input[type=checkbox]:checked")
    if (checked.length > limit){
        button.attr("disabled", false)
    } else {
        button.attr("disabled", true)
    }
})

$("#btn-optimization").click(function (event) {
    event.preventDefault();
    let form = $("#form-optimization");
    let params = form.serializeJSON();
    $.post({
        data: JSON.stringify(params),
        url: form.attr("action"),
        contentType: 'application/json',
    }).done(function (data){
        Plotly.newPlot(
            "budget-optimizer",
            JSON.parse(data.graph)[0].data,
            JSON.parse(data.graph)[0].layout
        );
    }).fail(function (jqXHR){
        let error = JSON.parse(jqXHR.responseText)
        $("#error-message").html(error.detail)
    })
})


