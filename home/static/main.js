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
  // console.log(d);
  var main = d3.select("#partidosTable tbody");
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

  if ($(partidosTable).height() < $(partidos_scroll).height()) {
    down_arrow_partidos.removeClass("hide");
  }

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

  if ($(leaderboardTable).height()< $(leaderboard_scroll).height() ) {
    down_arrow_leaderboard.removeClass("hide");
  }
});

const up_arrow_partidos = $(up_partidos);
const down_arrow_partidos = $(down_partidos);

$(partidosTable).scroll(function () {
  const scroll = $(partidosTable).scrollTop();

  if (scroll > 0.2 * $(partidosTable).height()) {
    up_arrow_partidos.removeClass("hide");
  } else {
    up_arrow_partidos.addClass("hide");
  }
  if (scroll + $(partidosTable).height() > 0.2 * $(partidosTable).height() + $(partidos_scroll).height()) {
    down_arrow_partidos.addClass("hide");
  } else {
    down_arrow_partidos.removeClass("hide");
  }
});

const up_arrow_leaderboard = $(up_leaderboard);
const down_arrow_leaderboard = $(down_leaderboard);

$(leaderboardTable).scroll(function () {
  const scroll = $(leaderboardTable).scrollTop();
  if (scroll > 0.2 * $(leaderboardTable).height()) {
    up_arrow_leaderboard.removeClass("hide");
  } else {
    up_arrow_leaderboard.addClass("hide");
  }
  if (
    scroll + $(leaderboardTable).height() >
    1.2 * $(leaderboard_scroll).height()
  ) {
    down_arrow_leaderboard.addClass("hide");
  } else {
    down_arrow_leaderboard.removeClass("hide");
  }
});

