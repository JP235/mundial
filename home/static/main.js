// console.log("loaded tables");

// based on: D3 Table - F1 Leaderboard by: Jonathan
// https://codepen.io/jonakirke94/pen/NWzreGM

$(menudropdown).hover(
  () => { //hover
    $(menu_logo_open).removeClass("hide-display");
    $(menu_logo_closed).addClass("hide-display");
  },
  () => { //out
    $(menu_logo_open).addClass("hide-display");
    $(menu_logo_closed).removeClass("hide-display");
  }
)

async function get_games() {
  const rawResponse = await fetch("/API/games", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  // console.log(rawResponse)
  let data = rawResponse.json();
  return data;
}


async function get_users() {
  const rawResponse = await fetch("/API/users", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  // console.log(rawResponse)
  let data = rawResponse.json();
  return data;
}

const games_data = get_games();

games_data.then((d) => {
  let p_future = d.p_future
  let p_today = d.p_today

  var main_future = d3.select("#partidosTable tbody");
  main_future.attr("class", "scrollcontent");
  var t = main_future
    .selectAll("tr.row")
    .data(p_future)
    .enter()
    .append("tr")
    .attr("class", "row");

  t.append("td")
    .html(
      ({
        id,
        team_1,
        team_2
      }) =>
      `<a href=/partido/${id}>${team_1} - ${team_2}</a>`
    )
    .attr("class", "equipos");

  t.append("td")
    .attr("class", "fecha")
    .append("span")
    .text(({
      game_date
    }) => {
      [y, m, d] = game_date.split("-");
      return [d, m, y.slice(2)].join("/");
    });

  t.append("td")
    .attr("class", "hora")
    .append("span")
    .text(({
      game_time
    }) => game_time.slice(0, -3));

  var main_today = d3.select("#partidosHoyTable tbody");
  main_today.attr("class", "scrollcontent");
  var t = main_today
    .selectAll("tr.row")
    .data(p_today)
    .enter()
    .append("tr")
    .attr("class", "row");

  t.append("td")
    .html(
      ({
        id,
        team_1,
        team_2
      }) =>
      `<a href=/partido/${id}>${team_1} - ${team_2}</a>`
    )
    .attr("class", "equipos");
  t.append("td")
    .attr("class", "hora")
    .append("span")
    .text(({
      game_time
    }) => game_time.slice(0, -3));
  // t.append("td")
  //   .attr("class", "prediccion")
  //   .append("span")
  //   .text(({
  //     prediction
  //   }) => prediction);
});

const users_data = get_users();
users_data.then((d) => {
  var main = d3.select("#leaderboardTable tbody");
  main.attr("class", "scrollcontent");

  var t = main
    .selectAll("tr.row")
    .data(d)
    .enter()
    .append("tr")
    .attr("class", "row");
  t.append("td")
    .text((d, i) => i + 1)
    .attr("class", "position");
  t.append("td")
    .html(({
      username
    }) => `<a href=/predicciones/${username}>${username}</a>`)
    .attr("class", "jugador");
  t.append("td")
    .attr("class", "P")
    .append("span")
    .text(({
      points
    }) => points);
});