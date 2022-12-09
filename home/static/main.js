// console.log("loading tables");

async function get_games() {
  const rawResponse = await fetch("/API/games", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  const {
    p_future,
    p_today
  } = await rawResponse.json();
  set_games_future(p_future)
  set_games_today(p_today)
}

async function get_users() {
  const rawResponse = await fetch("/API/users", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  let users = await rawResponse.json();
  // console.log(users);
  set_users_rank(users)
}

get_games()
get_users()


$("#menudropdown").hover(
  () => { //hover
    $(menu_logo_open).removeClass("hide-display");
    $(menu_logo_closed).addClass("hide-display");
  },
  () => { //out
    $(menu_logo_open).addClass("hide-display");
    $(menu_logo_closed).removeClass("hide-display");
  }
)

function set_users_rank(d) {
  let mainUsers = d3.select("#leaderboardTable tbody");
  mainUsers.attr("class", "scrollcontent");
  // console.log(d)
  let t = mainUsers
    .selectAll("tr.row")
    .data(d)
    .enter()
    .append("tr")
    .attr("class", "row");
  t.append("td")
    .text(({
      rank
    }) => rank)
    .attr("class", "position");
  t.append("td")
    .html(({
      username,winner_flag,winner_abbr
    }) => `<div class="flag-mini"
    style="background:url(${winner_flag}) center center / 100% no-repeat"></div>
<a href=/predicciones/${username}>${username}</a>`)
    .attr("class", "jugador");
  t.append("td")
    .attr("class", "P")
    .append("span")
    .text(({
      points
    }) => points);
}

function set_games_today(p_today) {
  let tableToday = d3.select("#partidosHoyTable tbody");
  tableToday.attr("class", "scrollcontent");
  let t = tableToday
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
      }) => `<a href=/partido/${id}>${team_1} - ${team_2}</a>`
    )
    .attr("class", "equipos");
  t.append("td")
    .attr("class", "hora")
    .append("span")
    .text(({
      game_time
    }) => game_time.slice(0, -3));
}

function set_games_future(p_future) {
  let tableFuture = d3.select("#partidosTable tbody");
  tableFuture.attr("class", "scrollcontent");
  let t = tableFuture
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
      }) => `<a href=/partido/${id}>${team_1} - ${team_2}</a>`
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
}