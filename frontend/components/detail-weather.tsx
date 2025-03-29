import { useState } from 'react';
import {
  Moon,
  Sunrise,
  Sunset,
  Thermometer,
  Droplets,
  Wind,
  Cloud,
  Umbrella,
  Clock
} from 'lucide-react';
import { Button } from "@/components/ui/button"


interface AstroForecast {
    moon_phase: string;
    moonrise: string;
    moonset: string;
    sunrise: string;
    sunset: string;
}
  
interface DailyForecast {
    avghumidity: number;
    avgtemp_c: number;
    condition_code: number;
    condition_icon: string | null;
    condition_text: string | null;
}
  
interface HourlyForecastItem {
time: string;
temp_c: number;
wind_kph: number;
cloud: number;
chance_of_rain: number;
}


  
type HourlyForecast = HourlyForecastItem[];
  
interface WeatherDashboardProps {
    astroForecast: AstroForecast;
    dailyForecast: DailyForecast;
    hourlyForecast: HourlyForecast;
    locationName: string;
}

const WeatherDashboard: React.FC<WeatherDashboardProps> = ({
  astroForecast,
  dailyForecast,
  hourlyForecast,
  locationName
}) => {
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const openPopup = () => {
        setIsPopupOpen(true);
    };

    const closePopup = () => {
        setIsPopupOpen(false);
    };
  return (
    <div className="w-full">
    <Button variant="outline" size="sm" className="w-full hover:bg-gray-300" onClick={openPopup}>
        View Detailed Forecast
    </Button>

    {/* Popup Modal */}
    {isPopupOpen && (
      <div className="fixed inset-0 flex items-center justify-center z-50 mx-4">
        {/* Background Overlay */}
        <div
          className="fixed inset-0 bg-black bg-opacity-50"
          onClick={closePopup} 
        ></div>

        {/* Popup Content */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 max-w-md w-full relative z-10">
          {/* Close Button */}
          <button
            className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
            onClick={closePopup}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="w-6 h-6"
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>

          {/* Title */}
          <h2 className="text-xl text-center font-semibold text-gray-800 dark:text-gray-200 mb-4">
            <span className="capitalize">{locationName}'s</span> Detailed Forecast
          </h2>

          {/* Astro Forecast */}
          <div className="space-y-4 mb-6">
                <h3 className="text-lg font-medium dark:text-gray-300 text-brand">Astro Forecast</h3>
                <p className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                <Moon size={18} />
                <span>Moon Phase: {astroForecast.moon_phase}</span>
                </p>
                <p className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                <Sunrise size={18} />
                <span>Sunrise: {astroForecast.sunrise}</span>
                </p>
                <p className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
                <Sunset size={18} />
                <span>Sunset: {astroForecast.sunset}</span>
                </p>
            </div>

          {/* Daily Forecast */}
          <div className="space-y-4 mb-6">
            <h3 className="text-lg font-medium text-brand dark:text-gray-300">Daily Forecast</h3>
            <p className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
            <Thermometer size={18} />
            <span>Avg Temp: {dailyForecast.avgtemp_c}°C</span>
            </p>
            <p className="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
            <Droplets size={18} />
            <span>Avg Humidity: {dailyForecast.avghumidity}%</span>
            </p>
        </div>
        <div className="space-y-4">
        <h3 className="text-lg font-medium text-brand dark:text-gray-300">Hourly Forecast</h3>

        <div className="grid grid-cols-3 gap-4">
            {hourlyForecast
            .filter((hour) => new Date(hour.time) > new Date()) 
            .slice(0, 5) 
            .map((hour, index) => (
                <div
                key={index}
                className="bg-gray-100 dark:bg-gray-700 rounded-lg p-4 space-y-2 text-center"
                >
                {/* Time */}
                <p className="text-sm font-medium text-gray-600 dark:text-gray-300">
                    {hour.time.split('T')[1]} 
                </p>

                {/* Weather Details */}
                <div className="space-y-1">
                    <p className="flex items-center justify-center space-x-1 text-gray-500 dark:text-gray-400">
                    <Wind size={16} />
                    <span className="text-xs">{`${hour.wind_kph ?? 'N/A'} kph`}</span>
                    </p>
                    <p className="flex items-center justify-center space-x-1 text-gray-500 dark:text-gray-400">
                    <Cloud size={16} />
                    <span className="text-xs">{`${hour.cloud ?? 'N/A'}%`}</span>
                    </p>
                    <p className="flex items-center justify-center space-x-1 text-gray-500 dark:text-gray-400">
                    <Umbrella size={16} />
                    <span className="text-xs">{`${hour.chance_of_rain ?? 'N/A'}%`}</span>
                    </p>
                </div>
                </div>
            ))}
        </div>
        </div>
        
        </div>
      </div>
    )}
  </div>
);
};


export default WeatherDashboard;