async function get_game_predictions() {
  const rawResponse = await fetch(["/API/predictions", window.location.pathname.split("/")[2]].join("/"), {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  // console.log(rawResponse)
  let data = rawResponse.json();
  return data;
}
// const loc = window.location.pathname
// console.log(loc)
const predictions_data = get_game_predictions()
predictions_data.then((d) => {
  var main = d3.select("#predictionsTable tbody");
  main.attr("class", "scrollcontent");
	var t = main
		.selectAll("tr.row")
		.data(d)
		.enter()
		.append("tr")
		.attr("class", "row");
	t.append("td")
  .html(
    ({ game, team_1, team_2, round }) =>
      `<a href=/partido/${game}>${team_1} - ${team_2}</a>    <i>${round}</i>`
  )
		.attr("class", "Prediccion");
	t.append("td")
		.attr("class", "P")
		.append("span")
		.text(({ predicted_score }) => predicted_score);

  if ( $(predictionsTable).height() < $(predictions_scroll).height()) {
    down_arrow_predictions.removeClass("hide");
  }
}).catch(e => {
  console.log(e)
})

const up_arrow_predictions = $(up_predictions);
const down_arrow_predictions = $(down_predictions);



$(predictionsTable).scroll(function () {
  const scroll_pt = $(predictionsTable).scrollTop();
  if (scroll_pt > 0.2 * $(predictionsTable).height()) {
    up_arrow_predictions.removeClass("hide");
  } else {
    up_arrow_predictions.addClass("hide");
  }
  if (scroll_pt + $(predictionsTable).height() > 0.2*$(predictionsTable).height() + $(predictions_scroll).height()) {
    down_arrow_predictions.addClass("hide");
  } else {
    down_arrow_predictions.removeClass("hide");
  }
});