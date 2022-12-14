var teams = document.getElementsByClassName("name_team");
var w = [10 + Math.max(teams[0].offsetWidth, teams[1].offsetWidth), "px"].join(
  ""
);
Object.entries(teams).forEach((element) => {
  element[1].style.width = w;
});

async function get_game_predictions() {
  const rawResponse = await fetch(
    ["/API/game_predictions/", window.location.pathname.split("/")[2]].join(""), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  // console.log(rawResponse)
  let data = rawResponse.json();
  return data;
}
const game_predictions_data = get_game_predictions();
game_predictions_data.then((d) => {
  var main = d3.select("#gamePredictionsTable tbody");
  main.attr("class", "scrollcontent");
  var t = main
    .selectAll("tr.row")
    .data(d)
    .enter()
    .append("tr")
    .attr("class", "row");

  t.append("td")
    .html(
      ({
        owner
      }) =>
      `<a href=/predicciones/${owner}>${owner}</a>`
    )
    .attr("class", "jugador");

  t.append("td")
    .attr("class", "prediccion")
    .append("span")
    .text(({
      predicted_score
    }) => predicted_score);
});