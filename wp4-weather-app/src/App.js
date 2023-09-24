import React, { useState } from 'react';
import axios from 'axios';
import WeatherForecast from './WeatherForecast';
import Cookies from 'js-cookie';

function App() {
  const [data, setData] = useState({});
  const [location, setLocation] = useState(Cookies.get('locationCookie') || '');
  const [rainChance, setRainChance] = useState('');
  const [rainChanceinput, setRainChanceinput] = useState(Cookies.get('rainChanceinputCookie') || '');
  const [maxTemp, setMaxTemp] = useState(Cookies.get('maxTempCookie') || '');
  const [minTemp, setMinTemp] = useState(Cookies.get('minTempCookie') || '');
  const [snowChanceinput, setSnowChanceinput] = useState(Cookies.get('snowChanceinputCookie') || '');
  const [maxWindSpeed, setMaxWindSpeed] = useState(Cookies.get('maxWindSpeedCookie') || '');
  
  //const url = `https://api.openweathermap.org/data/2.5/weather?q=${location}&units=metric&appid=11b4c7f160b27a5f817bbfa076f221b4`;

  Cookies.set('rainChanceinputCookie', rainChanceinput);
  Cookies.set('snowChanceinputCookie', snowChanceinput);
  Cookies.set('maxTempCookie', maxTemp);
  Cookies.set('minTempCookie', minTemp);
  Cookies.set('maxWindSpeedCookie', maxWindSpeed);
  
  const searchLocation = () => {
    const weatherUrl = `http://localhost:5000/api/weather?location=${location}`;
    
    axios.get(weatherUrl).then((response) => {
      if (response.data.cod !== 200) return;
        setData(response.data);

        const forecastUrl = `http://localhost:5000/api/forecast?location=${location}`;

        axios.get(forecastUrl).then((forecastResponse) => {
          if (forecastResponse.data.list && forecastResponse.data.list.length > 0) {
            const rainChance = forecastResponse.data.list[0].pop;
            console.log(forecastResponse.data.list)
            setRainChance(rainChance * 100);
            Cookies.set('locationCookie', location);
            
            axios.post('http://localhost:5000/api/saveinput', {
              location: location,
              rainChanceinput: rainChanceinput,
              maxTemp: maxTemp,
              minTemp: minTemp,
              snowChanceinput: snowChanceinput,
              maxWindSpeed: maxWindSpeed
            }).then((saveResponse) => {
              console.log(saveResponse.data);
            }).catch((error) => {
              console.error(error);
            });
          }
        });
      });
    };
  return (
    <div className="App">
      <div className="Zoeken">
      <label htmlFor="Zoeken">📍</label>
        <input
          value={location}
          onChange={(event) => setLocation(event.target.value)}
          onKeyDown={searchLocation}
          placeholder="Locatie"
          type="text"
          />
          <div className="temperature-inputs">
  <div className="temperature-input">
    <label htmlFor="minTemp">🧊</label>
    <input
      type="number"
      id="minTemp"
      value={minTemp}
      placeholder="Min temperatuur"
      onChange={(event) => setMinTemp(event.target.value)}
    />
  </div>
  <div className="temperature-input">
    <label htmlFor="maxTemp">☀️</label>
    <input
      type="number"
      id="maxTemp"
      value={maxTemp}
      placeholder="Max temperatuur"
      onChange={(event) => setMaxTemp(event.target.value)}
    />
  </div>
  <div className="rain">
  <label htmlFor="rainChance">☔</label>
  <input
    type="number"
    id="rainChance"
    value={rainChanceinput}
    placeholder="Kans op regen"
    onChange={(event) => setRainChanceinput(event.target.value)}
  />
</div>
  </div>
  <div className="Snow-inputs">
          <div className="Snowy-input">
            <label htmlFor="snowChance">❄️</label>
            <input
              type="number"
              id="snowChance"
              value={snowChanceinput}
              placeholder="Kans op sneeuw"
              onChange={(event) => setSnowChanceinput(event.target.value)}
            />
          </div>
          <div className="wind-input">
            <label htmlFor="maxWindSpeed">🍃</label>
            <input
              type="number"
              id="maxWindSpeed"
              value={maxWindSpeed}
              placeholder="Max windsnelheid"
              onChange={(event) => setMaxWindSpeed(event.target.value)}
            />
            </div>
      </div>
      </div>
      <div className="container">
        <div className="top">
          <div className="locatie">
            <p>{data.name}</p>
          </div>
          <div className="temp">
            {data.main ? <h1>{data.main.temp.toFixed(0)}°C</h1> : null}
          </div>
          <div className="beschrijving">
            {data.weather ? <p>{data.weather[0].main}</p> : null}
          </div>
          {location && 
          <WeatherForecast location={location} 
          minTemp={minTemp} 
          maxTemp={maxTemp} 
          maxWindSpeed={maxWindSpeed}
          maxRainChance={rainChanceinput} 
          maxSnowChance={snowChanceinput} />}
        </div>
        <div className="bottom">
          <div className="gevoelstemperatuur">
          <h1 style={{ fontSize: '14px' }}>Gevoelstemperatuur</h1>
            {data.main ? <p>{data.main.feels_like.toFixed(0)}°C</p>  : null}
          </div>
          <div className="luchtvochtigheid">
          <h1 style={{ fontSize: '14px' }}>Luchtvochtigheid</h1>
            {data.main ? <p>{data.main.humidity}%</p>  : null}
          </div>
          <div className="wind">
          <h1 style={{ fontSize: '14px' }}>Windsnelheid km/h</h1>
            {data.wind ? <p>{data.wind.speed}</p>  : null }
          </div>
          <div className="rain">
          <h1 style={{ fontSize: '14px' }}>Kans op neerslag</h1>
          {rainChance && <p>{rainChance}%</p>}
        </div>
        </div>
      </div>
    </div>
  );
}

export default App;