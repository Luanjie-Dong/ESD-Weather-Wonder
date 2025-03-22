import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { MapPin, Cloud, AlertTriangle } from "lucide-react"
import Link from "next/link"
import Navbar from "@/components/navbar"
import type { WeatherData } from "@/lib/types"
import { getCurrentWeather } from "@/lib/weather-service"
import WeatherForecastTabs from "@/components/weather-forecast-tabs"

// Mark this as a Server Component by not using "use client"
export default async function HomePage() {
  // Server-side data fetching
  const weather: WeatherData = await getCurrentWeather("San Francisco, CA")

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1 pb-16 pt-6 md:pb-6">
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold md:text-3xl">Welcome back, Alex</h1>
            <Button variant="outline" size="sm" asChild>
              <Link href="/profile">View Profile</Link>
            </Button>
          </div>

          {/* Current Weather Widget */}
          <Card className="overflow-hidden bg-gradient-to-br from-primary to-secondary">
            <CardContent className="p-6">
              <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
                <div className="text-center md:text-left">
                  <h2 className="text-xl font-bold">{weather.location}</h2>
                  <p className="text-4xl font-bold">{weather.temperature}°F</p>
                  <p className="text-sm">{weather.condition}</p>
                </div>
                <div className="flex flex-col items-center">
                  <Cloud className="h-20 w-20 text-brand" />
                  <div className="mt-2 grid grid-cols-3 gap-4 text-center">
                    <div>
                      <p className="text-xs">Humidity</p>
                      <p className="font-bold">{weather.humidity}%</p>
                    </div>
                    <div>
                      <p className="text-xs">Wind</p>
                      <p className="font-bold">{weather.wind} mph</p>
                    </div>
                    <div>
                      <p className="text-xs">UV Index</p>
                      <p className="font-bold">{weather.uvIndex}</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Saved Locations */}
          <div>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-bold">Saved Locations</h2>
              <Button variant="outline" size="sm" asChild>
                <Link href="/locations">Manage</Link>
              </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {weather.savedLocations.map((location) => (
                <Card key={location.name} className="transition-all hover:shadow-md">
                  <CardHeader className="pb-2">
                    <CardTitle className="flex items-center text-lg">
                      <MapPin className="mr-2 h-4 w-4" />
                      {location.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex items-center justify-between pb-4">
                    <p className="text-2xl font-bold">{location.temp}</p>
                    <Cloud className="h-8 w-8 text-brand" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>

          {/* Emergency Alerts */}
          <div>
            <h2 className="mb-4 text-xl font-bold">Emergency Alerts</h2>

            {weather.alerts.length > 0 ? (
              weather.alerts.map((alert) => (
                <Card key={alert.id} className="border-l-4 border-l-destructive bg-destructive/10">
                  <CardHeader className="pb-2">
                    <div className="flex items-center">
                      <AlertTriangle className="mr-2 h-5 w-5 text-destructive" />
                      <CardTitle className="text-lg text-destructive">{alert.title}</CardTitle>
                    </div>
                    <CardDescription>
                      {alert.location} - {alert.expires}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm">{alert.description}</p>
                    <Button variant="destructive" size="sm" className="mt-2">
                      View Details
                    </Button>
                  </CardContent>
                </Card>
              ))
            ) : (
              <Card>
                <CardContent className="p-6 text-center text-muted-foreground">
                  No active alerts for your locations
                </CardContent>
              </Card>
            )}
          </div>

          {/* Weather Forecast */}
          <WeatherForecastTabs forecast={weather.forecast} />
        </div>
      </main>
    </div>
  )
}

