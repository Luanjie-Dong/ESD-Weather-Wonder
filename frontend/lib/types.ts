export interface WeatherData {
  location: string
  temperature: number
  condition: string
  humidity: number
  wind: number
  uvIndex: number
  savedLocations: {
    name: string
    temp: string
  }[]
  alerts: {
    id: string
    title: string
    location: string
    expires: string
    description: string
  }[]
  forecast: ForecastData
}

export interface ForecastData {
  daily: {
    day: string
    temp: number
    condition: string
  }[]
  hourly: {
    time: string
    temp: number
    condition: string
  }[]
}

export interface LocationData {
  id: string
  name: string
  temp: string
  icon: string
  primary?: boolean
}

export interface AlertData {
  id: string
  title: string
  location: string
  date: string
  severity: string
  description: string
  expires?: string
  active: boolean
}

