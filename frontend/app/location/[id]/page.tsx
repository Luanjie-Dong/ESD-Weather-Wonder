import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Cloud, CloudDrizzle, CloudLightning, CloudRain, Droplets, Thermometer, Wind } from "lucide-react"
import Link from "next/link"
import Navbar from "@/components/navbar"
import { getLocationWeather } from "@/lib/weather-service"
import { notFound } from "next/navigation"
import AuthCheck from "@/components/auth-check"

// This is a Server Component
export default async function LocationDetailPage({ params }: { params: { id: string } }) {
  try {
    // Server-side data fetching
    const weather = await getLocationWeather(params.id)

    return (
      <AuthCheck>
      <div className="flex min-h-screen flex-col">
        <Navbar />

        <main className="flex-1 pb-16 pt-6 md:pb-6">
          <div className="container space-y-6">
            <div className="flex items-center gap-2">
              <Button variant="ghost" size="icon" asChild>
                <Link href="/locations">
                  <ArrowLeft className="h-5 w-5" />
                </Link>
              </Button>
              <h1 className="text-2xl font-bold md:text-3xl">{weather.location}</h1>
            </div>

            {/* Current Weather */}
            <Card className="overflow-hidden bg-gradient-to-br from-primary to-secondary">
              <CardContent className="p-6">
                <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
                  <div className="text-center md:text-left">
                    <p className="text-sm">Current Weather</p>
                    <p className="text-5xl font-bold">{weather.temperature}°F</p>
                    <p className="text-lg">{weather.condition}</p>
                    <p className="text-sm">Feels like 74°F</p>
                  </div>
                  <div className="flex flex-col items-center">
                    <Cloud className="h-24 w-24 text-brand" />
                  </div>
                  <div className="grid grid-cols-2 gap-4 text-center md:grid-cols-1">
                    <div className="flex items-center gap-2">
                      <Thermometer className="h-5 w-5" />
                      <div className="text-left">
                        <p className="text-xs">High/Low</p>
                        <p className="font-bold">78°/65°</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Wind className="h-5 w-5" />
                      <div className="text-left">
                        <p className="text-xs">Wind</p>
                        <p className="font-bold">{weather.wind} mph</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Droplets className="h-5 w-5" />
                      <div className="text-left">
                        <p className="text-xs">Humidity</p>
                        <p className="font-bold">{weather.humidity}%</p>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Weather Forecast */}
            <div>
              <h2 className="mb-4 text-xl font-bold">5-Day Forecast</h2>

              <div className="grid grid-cols-5 gap-2 overflow-x-auto">
                {[
                  { day: "Today", temp: "72°F", icon: Cloud },
                  { day: "Tue", temp: "75°F", icon: Cloud },
                  { day: "Wed", temp: "68°F", icon: CloudRain },
                  { day: "Thu", temp: "65°F", icon: CloudLightning },
                  { day: "Fri", temp: "70°F", icon: CloudDrizzle },
                ].map((day) => (
                  <Card key={day.day} className="border-none bg-muted text-center">
                    <CardHeader className="p-2 pb-0">
                      <CardTitle className="text-sm">{day.day}</CardTitle>
                    </CardHeader>
                    <CardContent className="p-2">
                      <day.icon className="mx-auto h-8 w-8 text-brand" />
                      <p className="mt-1 text-sm font-bold">{day.temp}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Hourly Forecast */}
            <div>
              <h2 className="mb-4 text-xl font-bold">Hourly Forecast</h2>

              <div className="flex gap-2 overflow-x-auto pb-2">
                {Array.from({ length: 12 }).map((_, i) => {
                  const hour = new Date()
                  hour.setHours(hour.getHours() + i)
                  const hourLabel = hour.getHours() % 12 || 12
                  const ampm = hour.getHours() >= 12 ? "PM" : "AM"

                  return (
                    <Card key={i} className="min-w-[80px] border-none bg-muted text-center">
                      <CardHeader className="p-2 pb-0">
                        <CardTitle className="text-xs">{`${hourLabel}${ampm}`}</CardTitle>
                      </CardHeader>
                      <CardContent className="p-2">
                        <Cloud className="mx-auto h-6 w-6 text-brand" />
                        <p className="mt-1 text-sm font-bold">{`${Math.round(72 - Math.sin(i) * 5)}°`}</p>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>
            </div>

            {/* Weather Details */}
            <Card>
              <CardHeader>
                <CardTitle>Weather Details</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Sunrise</p>
                    <p className="font-medium">6:42 AM</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Sunset</p>
                    <p className="font-medium">7:38 PM</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Chance of Rain</p>
                    <p className="font-medium">10%</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Pressure</p>
                    <p className="font-medium">1012 hPa</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Visibility</p>
                    <p className="font-medium">10 mi</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">UV Index</p>
                    <p className="font-medium">3 (Moderate)</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Wind Direction</p>
                    <p className="font-medium">NW</p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-xs text-muted-foreground">Air Quality</p>
                    <p className="font-medium">Good</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
      </AuthCheck>
    )
  } catch (error) {
    notFound()
  }
}

