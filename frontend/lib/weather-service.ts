import type { WeatherData } from "./types"

// Mock data service - in a real app, this would call an API
export async function getCurrentWeather(location: string): Promise<WeatherData> {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 100))

  return {
    location: "San Francisco, CA",
    temperature: 72,
    condition: "Partly Cloudy",
    humidity: 65,
    wind: 8,
    uvIndex: 3,
    savedLocations: [
      { name: "New York, NY", temp: "65°F" },
      { name: "Los Angeles, CA", temp: "82°F" },
      { name: "Chicago, IL", temp: "58°F" },
    ],
    alerts: [
      {
        id: "1",
        title: "Severe Thunderstorm Warning",
        location: "Chicago, IL",
        expires: "Expires in 2 hours",
        description: "Strong thunderstorms with potential for flash flooding and wind gusts up to 60mph.",
      },
    ],
    forecast: {
      daily: [
        { day: "Mon", temp: 70, condition: "cloudy" },
        { day: "Tue", temp: 71, condition: "cloudy" },
        { day: "Wed", temp: 72, condition: "stormy" },
        { day: "Thu", temp: 73, condition: "cloudy" },
        { day: "Fri", temp: 74, condition: "cloudy" },
      ],
      hourly: [
        { time: "Now", temp: 72, condition: "cloudy" },
        { time: "1PM", temp: 71, condition: "cloudy" },
        { time: "2PM", temp: 70, condition: "cloudy" },
        { time: "3PM", temp: 69, condition: "cloudy" },
        { time: "4PM", temp: 68, condition: "cloudy" },
        { time: "5PM", temp: 67, condition: "cloudy" },
      ],
    },
  }
}

export async function getLocationWeather(locationId: string): Promise<WeatherData> {
  // In a real app, this would fetch data for a specific location
  return getCurrentWeather(locationId)
}

export async function getAlerts(): Promise<WeatherData["alerts"]> {
  const weather = await getCurrentWeather("")
  return weather.alerts
}

