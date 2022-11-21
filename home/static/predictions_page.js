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
  // console.log(d)
  main.attr("class", "scrollcontent");
  var t = main
    .selectAll("tr.row")
    .data(d)
    .enter()
    .append("tr")
    .attr("class", "row");
  if (d) {
    t.append("td")
      .html(
        ({
          game,
          team_1,
          team_2,
          round
        }) =>
        `<a href=/partido/${game}>${team_1} - ${team_2}</a>    <i>${round}</i>`
      )
      .attr("class", "partido");
    t.append("td")
      .attr("class", "resultado")
      .append("span")
      .text(({
        score
      }) => score);
    t.append("td")
      .attr("class", "prediccion")
      .append("span")
      .text(({
        predicted_score
      }) => predicted_score);
    t.append("td")
      .attr("class", "points")
      .append("span")
      .text(({
        correct
      }) => correct != null ? correct * 2 : "-");
  }
}).catch(e => {
  console.log(e)
})
