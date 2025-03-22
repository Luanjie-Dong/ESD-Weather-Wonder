"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Cloud, CloudLightning } from "lucide-react"
import type { ForecastData } from "@/lib/types"

export default function WeatherForecastTabs({ forecast }: { forecast: ForecastData }) {
  return (
    <div>
      <h2 className="mb-4 text-xl font-bold">Forecast</h2>

      <Tabs defaultValue="daily">
        <TabsList className="mb-4">
          <TabsTrigger value="daily">Daily</TabsTrigger>
          <TabsTrigger value="hourly">Hourly</TabsTrigger>
        </TabsList>

        <TabsContent value="daily" className="space-y-0">
          <div className="grid grid-cols-5 gap-2 overflow-x-auto">
            {forecast.daily.map((day) => (
              <Card key={day.day} className="border-none bg-muted text-center">
                <CardHeader className="p-2 pb-0">
                  <CardTitle className="text-sm">{day.day}</CardTitle>
                </CardHeader>
                <CardContent className="p-2">
                  {day.condition === "stormy" ? (
                    <CloudLightning className="mx-auto h-8 w-8 text-brand" />
                  ) : (
                    <Cloud className="mx-auto h-8 w-8 text-brand" />
                  )}
                  <p className="mt-1 text-sm font-bold">{day.temp}°F</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="hourly">
          <div className="grid grid-cols-6 gap-2 overflow-x-auto">
            {forecast.hourly.map((hour) => (
              <Card key={hour.time} className="border-none bg-muted text-center">
                <CardHeader className="p-2 pb-0">
                  <CardTitle className="text-sm">{hour.time}</CardTitle>
                </CardHeader>
                <CardContent className="p-2">
                  <Cloud className="mx-auto h-6 w-6 text-brand" />
                  <p className="mt-1 text-sm font-bold">{hour.temp}°F</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}

