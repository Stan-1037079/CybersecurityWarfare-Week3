import React, { useEffect, useState } from 'react';

function getRainChance(forecastItem) {
  return forecastItem.rain ? forecastItem.pop*100 : 0;
}

function getSnowChance(forecastItem) {
  return forecastItem.snow ? forecastItem.pop*100 : 0
}

function WeatherForecast(props) {
  const [forecast, setForecast] = useState([]);

  useEffect(() => {
    fetch(`http://localhost:5000/api/forecast?location=${props.location}`)
      .then(response => response.json())
      .then(data => {
        if (data.message === 'Location not found') return;
        const forecastData = data;

        const next3DaysForecast = filterNext3DaysForecast(forecastData.list);

        setForecast(next3DaysForecast);
      })
      .catch(error => {
        console.error('Error fetching forecast data:', error);
      });
  }, [props.location]);

  const filterNext3DaysForecast = (forecastData) => {

    const next3Days = [];
    const seenDays = new Set(); 

    for (const forecastItem of forecastData) {
      const forecastDate = new Date(forecastItem.dt * 1000);

      if (forecastDate.getHours() === 8 && !seenDays.has(forecastDate.toISOString())) {
        next3Days.push(forecastItem);
        seenDays.add(forecastDate.toISOString());

        if (next3Days.length === 3) {
          break; 
        }
      }
    }

    return next3Days;
  };

  return (
    <div>
      <h2 style={{ fontSize: '20px' }}>Weersvoorspelling voor de komende 3 dagen</h2>
      <ul>
        {forecast.map(forecastItem => ( 
          
          <li key={forecastItem.dt}>
            <p style={{ fontSize: '24px' }}>Datum: {new Date(forecastItem.dt * 1000).toLocaleDateString()}</p>
            <p style={{ fontSize: '18px' }}>Tijd: {new Date(forecastItem.dt * 1000).toLocaleTimeString()}</p>
            <p style={{ fontSize: '18px' }}>Temperatuur: {forecastItem.main.temp.toFixed(0)}°C</p>
            <p style={{ fontSize: '18px' }}>Weer: {forecastItem.weather[0].description}</p>
            <p style={{ fontSize: '18px' }}>Kans op regen: {getRainChance(forecastItem)}</p>
            <p style={{ fontSize: '18px' }}>Kans op sneeuw: {getSnowChance(forecastItem)}</p>
            <p style={{ fontSize: '18px' }}>Max windsnelheid: {forecastItem.wind.speed} km/h</p>
            <p style={{ fontSize: '18px' }}>Fietsweer: 
                {forecastItem.main.temp >=  props.minTemp &&
                 forecastItem.main.temp <= props.maxTemp &&
                  forecastItem.wind.speed <= props.maxWindSpeed &&
                  getRainChance(forecastItem) <= props.maxRainChance &&
                  getSnowChance(forecastItem) <= props.maxSnowChance
                  ? ' Ja 🚲' : ' Nee ☂️'}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default WeatherForecast;



