document.addEventListener("DOMContentLoaded", function () {
	const searchForm = document.getElementById("search-form");
	const searchInput =
		document.getElementById("search-input");
	const searchResultsDropdown = document.getElementById(
		"search-results-dropdown"
	);

	searchForm.addEventListener("input", function (event) {
		event.preventDefault();
		const query = searchInput.value.trim();

		if (query.length === 0) {
			searchResultsDropdown.style.display = "none";
			searchResultsDropdown.innerHTML = "";
			return;
		}

		fetch(`/search?query=${query}`)
			.then((response) => response.json())
			.then((data) => {
				searchResultsDropdown.innerHTML = "";
				let results = [];

				data.people.forEach((person) => {
					results.push(
						`<li class="dropdown-item"><a class="dropdown-list-item" href="/characters/${person.id}">${person.name} (Person)</a></li>`
					);
				});

				data.films.forEach((film) => {
					results.push(
						`<li class="dropdown-item"><a class="dropdown-list-item" href="/films/${film.id}">${film.title} (Film)</a></li>`
					);
				});

				data.starships.forEach((starship) => {
					results.push(
						`<li class="dropdown-item"><a class="dropdown-list-item" href="/starships/${starship.id}">${starship.name} (Starship)</a></li>`
					);
				});

				data.vehicles.forEach((vehicle) => {
					results.push(
						`<li class="dropdown-item"><a class="dropdown-list-item" href="/vehicles/${vehicle.id}">${vehicle.name} (Vehicle)</a></li>`
					);
				});

				data.planets.forEach((planet) => {
					results.push(
						`<li class="dropdown-item"><a class="dropdown-list-item" href="/planets/${planet.id}">${planet.name} (Planet)</a></li>`
					);
				});

				data.species.forEach((species) => {
					results.push(
						`<li class="dropdown-item"><a class="dropdown-list-item" href="/species/${species.id}">${species.name} (Species)</a></li>`
					);
				});

				searchResultsDropdown.innerHTML = results.join("");
				searchResultsDropdown.style.display = results.length
					? "block"
					: "none";
			})
			.catch((error) => {
				console.error("Error:", error);
				searchResultsDropdown.style.display = "none";
			});
	});
	document.addEventListener("click", function (event) {
		if (!searchForm.contains(event.target)) {
			searchResultsDropdown.style.display = "none";
		}
	});

	// Search animation script

	const searchButton =
		document.getElementById("search-button");

	searchButton.addEventListener("click", function () {
		if (searchForm.classList.contains("active")) {
			// Submit the form if it's already active
			searchForm.submit();
		} else {
			// Add the active class to reveal the input
			searchForm.classList.add("active");
			searchInput.focus();

			searchButton.style.display = "none";
		}
	});
});
