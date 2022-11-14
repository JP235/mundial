async function get_game_predictions() {
	const rawResponse = await fetch("/API/predictions", {
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
  console.log("here")
  console.log(d)
	var main = d3.select("#PredictionsTable");
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

}).catch(e => {console.log(e)})