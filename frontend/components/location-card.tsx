
import { RefreshCw, Check , MapPin, Trash2, Calendar, Thermometer, ArrowUp, ArrowDown, Wind, Umbrella, Pencil } from "lucide-react"; // Adjust icon imports as needed
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import WeatherDashboard from "./detail-weather";
import React, { useState } from "react";

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

  export interface Location {
    LocationId: string;
    Label: string;
    Address: string;
    day: string;
    temp: number;
    max_temp: number;
    min_temp: number;
    wind: number;
    rain: number;
    astro: AstroForecast;
    daily: DailyForecast;
    hourly: HourlyForecastItem[];
  }

  interface LocationCardProps {
    location: Location;
    onDelete: (id: string) => void;
    onUpdate: (id: string, updatedData: { Label: string; Address: string }) => void;
    onRefresh: (id: string) => void;
  }

  const LocationCard: React.FC<LocationCardProps> = ({ location, onDelete, onUpdate , onRefresh}) => {
    const [isEditing, setIsEditing] = useState(false);
    const [editedLabel, setEditedLabel] = useState(location.Label);
    const [isExpanded, setIsExpanded] = useState(false); 

  
    const handleSave = () => {
      onUpdate(location.LocationId, { Label: editedLabel, Address: location.Address });
      setIsEditing(false); // Exit edit mode after saving
    };
  
    return (
      <Card key={location.LocationId} className="border-2 border-brand">
        <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          
            <CardTitle className="flex items-center text-lg capitalize">
                <MapPin className="mr-2 h-4 w-4" />
                {location.Address}
            </CardTitle>
          
          <div className="flex space-x-2">
            <button onClick={() => onRefresh(location.LocationId)}>
              <RefreshCw></RefreshCw>
            </button>
            {isEditing ? (
              <button
                onClick={handleSave}
                className="text-green-500 hover:text-green-700"
              >
                <Check className="h-5 w-5" /> {/* Save icon */}
              </button>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="text-blue-500 hover:text-blue-700"
              >
                <Pencil className="h-5 w-5" /> {/* Edit icon */}
              </button>
            )}
            {/* Delete Button */}
            <button
              onClick={() => onDelete(location.LocationId)}
              className="text-red-500 hover:text-red-700"
            >
              <Trash2 className="h-5 w-5" />
            </button>
          </div>
        </div>
      </CardHeader>
        <CardContent className="flex items-center justify-between pb-4">
          {isEditing ? (
            <div className="text-2xl font-bold capitalize">
                <div className="flex flex-col space-y-2 w-full">
                    <input
                    type="text"
                    value={editedLabel}
                    onChange={(e) => setEditedLabel(e.target.value)}
                    placeholder="Enter label"
                    className="p-2 border rounded-md"
                    />
                </div>
            </div>
          ) : (
            <p className="text-2xl font-bold capitalize">{location.Label}</p>
          )}
        </CardContent>
        <CardContent className="flex flex-col space-y-2 pb-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-5 w-5 text-gray-500" />
            <p className="text-lg font-medium">{location.day}</p>
          </div>
          <div className="flex items-center space-x-2">
            <Thermometer className="h-5 w-5 text-gray-500" />
            <p className="text-lg font-medium">Temperature: {location.temp}°C</p>
          </div>
  
          <div className="flex items-center space-x-2">
            <ArrowUp className="h-5 w-5 text-red-500" />
            <p className="text-base text-red-500">Max: {location.max_temp}°C</p>
            <ArrowDown className="h-5 w-5 text-blue-500" />
            <p className="text-base text-blue-500">Min: {location.min_temp}°C</p>
          </div>
  
          <div className="flex items-center space-x-2">
            <Wind className="h-5 w-5 text-gray-500" />
            <p className="text-base">Wind: {location.wind} kph</p>
          </div>
  
          <div className="flex items-center space-x-2">
            <Umbrella className="h-5 w-5 text-gray-500" />
            <p className="text-base">Rain: {location.rain}%</p>
          </div>
        </CardContent>
        <CardFooter className="pt-0">
          <WeatherDashboard
            astroForecast={location.astro}
            dailyForecast={location.daily}
            hourlyForecast={location.hourly}
            locationName={location.Address}
          />
        </CardFooter>
      </Card>
    );
  };
  
  export default LocationCard;