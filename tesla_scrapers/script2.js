
    // Dummy car data
    const cars = [
      {
        model: '2020 Model 3',
        price: '22.800 €',
        image: 'https://via.placeholder.com/400x300',
        details: 'Standard Plus Hinterradantrieb, Kilometerstand 64.548 km, Parkard, Stand der Auslieferung verfügbar'
      },
      {
        model: '2019 Model 3',
        price: '23.400 €',
        image: 'https://via.placeholder.com/400x300',
        details: 'Standard Plus Hinterradantrieb, Kilometerstand 73.124 km, Staatblicken, In weiter Zukunft'
      },
      {
        model: '2019 Model 3',
        price: '23.700 €',
        image: 'https://via.placeholder.com/400x300',
        details: 'Standard Plus Hinterradantrieb, Kilometerstand 70.501 km, Oberbayung, Stand der Auslieferung verfügbar'
      },
      // Add more car objects as needed
    ];

    // Function to create a car card
    function createCarCard(car) {
      const card = `
        <div class="col-md-4 mb-4">
          <div class="card">
            <img src="${car.image}" class="card-img-top car-image" alt="${car.model}">
            <div class="card-body">
              <h5 class="card-title">${car.model}</h5>
              <p class="card-text">${car.details}</p>
              <p class="card-text font-weight-bold">${car.price}</p>
            </div>
          </div>
        </div>
      `;
      return card;
    }

    // Function to filter cars based on selected options
    function filterCars() {
      const bestandsart = $('#bestandsart').val();
      const lackierung = $('#lackierung').val();
      const antrieb = $('#antrieb').val();
      const performanceAbstandsritic = $('#performanceAbstandsritic').is(':checked');
      const maximaleReichweiteAkku = $('#maximaleReichweiteAkku').is(':checked');
      const maximaleReichweiteHybrid = $('#maximaleReichweiteHybrid').is(':checked');
      const model3Hinterradantrieb = $('#model3Hinterradantrieb').is(':checked');
      const zuatzausstattungPerformance = $('#zuatzausstattungPerformance').is(':checked');
      const anhängerkupplung = $('#anhängerkupplung').is(':checked');
      const accelerationBoost = $('#accelerationBoost').is(':checked');
      const beizerseRücksitze = $('#beizerseRücksitze').is(':checked');
      const baujahr2024 = $('#baujahr2024').is(':checked');
      const baujahr2023 = $('#baujahr2023').is(':checked');
      const felgen18zoll = $('#18zollFelgen').is(':checked');
      const felgen19zoll = $('#19zollFelgen').is(':checked');
      const felgen20zoll = $('#20zollFelgen').is(':checked');

      const filteredCars = cars.filter(car => {
        // Apply filters based on selected options
        // ...
        return true; // Replace with your filtering logic
      });

      // Clear the car list
      $('#car-list').empty();

      // Add filtered cars to the list
      filteredCars.forEach(car => {
        const card = createCarCard(car);
        $('#car-list').append(card);
      });
    }

    // Call the filterCars function when the page loads
    filterCars();

    // Call the filterCars function when any filter option is changed
    $('select, input[type="checkbox"]').on('change', filterCars);
