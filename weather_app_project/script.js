async function getWeather() {
    const city = document.getElementById('cityInput').value;
    const apiKey = "a48d5cba290a44132a69566f94c32fb8"; // Replace with your actual OpenWeatherMap API key
  
    if (!city) {
      alert("Please enter a city name");
      return;
    }
  
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
  
    try {
      const response = await fetch(apiUrl);
      if (!response.ok) throw new Error("City not found");
  
      const data = await response.json();
  
      const weatherInfo = `
        <h2>${data.name}, ${data.sys.country}</h2>
        <p><strong>Temperature:</strong> ${data.main.temp} °C</p>
        <p><strong>Condition:</strong> ${data.weather[0].description}</p>
        <p><strong>Humidity:</strong> ${data.main.humidity}%</p>
        <p><strong>Wind Speed:</strong> ${data.wind.speed} m/s</p>
      `;
  
      document.getElementById("weatherResult").innerHTML = weatherInfo;
  
    } catch (error) {
      document.getElementById("weatherResult").innerHTML = `<p style="color:red;">${error.message}</p>`;
    }
  }
  