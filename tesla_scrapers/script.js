 
async function fetchCarData() {
  try {
      const response = await fetch('/data/tesla_m3_20240820_214338.json');
      const data = await response.json();
      return data.results;
  } catch (error) {
      console.error('Fehler beim Laden der Daten:', error);
      return [];
  }
}

// Funktion zum Erstellen einer Autokarte
function createCarCard(car) {
  const imageUrl = car.VehiclePhotos && car.VehiclePhotos.length > 0 ? car.VehiclePhotos[0].imageUrl : 'default-image-url.jpg';

     /**
     * Creates an HTML card element representing a car.
     *
     * @param {Object} car - The car data object.
     * @param {string} car.Model - The model name of the car.
     * @param {number} car.Year - The year of the car.
     * @param {number} car.Odometer - The odometer reading of the car.
     * @param {string} car.OdometerTypeShort - The unit of the odometer reading.
     * @param {number} car.Price - The price of the car.
     * @param {string} car.CurrencyCode - The currency code of the price.
     * @param {string} car.City - The city where the car is located.
     * @param {string} car.StateProvince - The state or province where the car is located.
     * @param {string[]} car.VehiclePhotos - An array of URLs for the car's photos.
     * @returns {string} The HTML string representing the car card.
     */
    // Funktion zum Abrufen der Daten aus der JSON-Datei
  const card = `
    <div class="col-md-4 mb-4">
      <div class="card">
        <img src="${imageUrl}" class="card-img-top car-image" alt="${car.Model}">
        <div class="card-body">
          <h5 class="card-title">${car.Year} ${car.OptionCodeData && car.OptionCodeData[10] ? car.OptionCodeData[10].name : ''}</h5>
          <p class="card-text">${car.OptionCodeData && car.OptionCodeData[12] ? car.OptionCodeData[12].description : ''}</p>
          <p class="card-text">Kilometerstand: ${car.Odometer} ${car.OdometerTypeShort}</p>
          <p class="card-text">Preis: ${car.Price} ${car.CurrencyCode}</p>
          <p class="card-text">${car.City}, ${car.StateProvince}</p>
          <p class="card-text">Kostenindikator: ${(car.Price / car.Odometer).toFixed(2)} € per km</p>
        </div>
      </div>
    </div>
  `;
  return card;
}

// Funktion zum Filtern der Autos basierend auf den ausgewählten Optionen
function filterCars(carsArray) {
  const bestandsart = $('#bestandsart').val();
  const lackierung = $('#lackierung').val();
  const antrieb = $('#antrieb').val();
  // Füge hier weitere Filteroptionen hinzu

  const filteredCars = carsArray.filter(car => {
      return (
          (bestandsart === '' || car.TitleStatus.toLowerCase() === bestandsart) &&
          (lackierung === '' || (car.PAINT && car.PAINT.some(paint => paint.toLowerCase().includes(lackierung.toLowerCase())))) &&
          (antrieb === '' || (car.AUTOPILOT && car.AUTOPILOT.some(autopilot => autopilot.toLowerCase().includes(antrieb.toLowerCase()))))
          // Füge hier weitere Filterkriterien hinzu
      );
  });

  return filteredCars;
}

// Funktion zum Rendern der Autokarten
async function renderCarCards() {
  const carsArray = await fetchCarData();
  const filteredCars = filterCars(carsArray);

  // Leere die Autoliste
  $('#car-list').empty();

  // Füge die gefilterten Autos zur Liste hinzu
  filteredCars.forEach(car => {
      const card = createCarCard(car);
      $('#car-list').append(card);
  });
}

// Rufe die Funktion zum Rendern der Autokarten beim Laden der Seite auf
renderCarCards();

// Rufe die Funktion zum Rendern der Autokarten auf, wenn sich eine Filteroption ändert
$('select, input[type="checkbox"]').on('change', renderCarCards);
