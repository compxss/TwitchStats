const search = document.getElementById("search")

if (search) {
    const streamers = document.querySelectorAll(".streamer")

    search.addEventListener("input", function () {
        
        const text = search.value.toLowerCase()

        streamers.forEach(function (streamer) {
            const name = streamer
                .querySelector("h3")
                .textContent
                .toLowerCase()

            if (name.includes(text)) {
                streamer.style.display = "block"
            } else {
                streamer.style.display = "none"
            }
        })
    })
}


function openStreamer(name) {
    window.location.href = "streamer.html?name=" + encodeURIComponent(name)
}


const params = new URLSearchParams(window.location.search)
const streamerName = params.get("name")

let selectedStreamer = null

if (streamerName) {
    
    fetch(
        "http://localhost:8000/api/streamer?name="
        + encodeURIComponent(streamerName)
    )

        .then(function(response) {

            if (!response.ok) {
                throw new Error("Стример не найден")
            }

            return response.json()
        })

        .then(function(apiData) {

            console.log("Получили данные:", apiData)

            selectedStreamer = apiData

            const nameElement = document.getElementById("streamer-name")
            if (nameElement) {
                nameElement.textContent = apiData.name
            }

            const average_online = document.getElementById("average_online")
            if (average_online) {
                average_online.textContent = apiData.average_online.toLocaleString("ru-RU")
            }

            const followers = document.getElementById("followers")
            if (followers) {
                followers.textContent = apiData.followers.toLocaleString("ru-RU")
            }

            const peak = document.getElementById("peak")
            if (peak) {
                peak.textContent = apiData.peak.toLocaleString("ru-RU")
            }

            const chart = document.getElementById("chart")

            if (chart) {

                chart.innerHTML = ""

                apiData.history.forEach(function (number) {

                    const bar = document.createElement("div")

                    bar.classList.add("bar")

                    bar.style.height = number / 60 + "px"

                    bar.title = number.toLocaleString("ru-RU") + " зрителей"

                    chart.appendChild(bar)
                })
            }
        })

        .catch(function(error) {

            console.error(
                "Ошибка API:",
                error
            )
        })
}

const streamersContainer = document.getElementById("streamers")

if (streamersContainer) {

    fetch("http://localhost:8000/api/streamers")

        .then(function(response) {
            return response.json()
        })

        .then(function(streamers) {

            console.log(
                "Стримеры:",
                streamers
            )

            for (const name in streamers) {

                const data = streamers[name]

                const card = document.createElement("div")

                card.classList.add("streamer")

                card.onclick = function() {
                    openStreamer(name)
                }

                card.innerHTML = `
                    <h3>${name}</h3>

                    <p>
                        ${data.viewers.toLocaleString("ru-RU")}
                        зрителей
                    </p>

                    <p>
                        ${data.online ? "Онлайн" : "Оффлайн"}
                    </p>
                `

                streamersContainer.appendChild(card)
            }
        })

        .catch(function(error) {
            console.error(
                "Ошибка загрузки стримеров:",
                error
            )
        })
}
