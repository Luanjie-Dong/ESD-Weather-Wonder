import { NextResponse } from "next/server"
import { getCurrentWeather } from "@/lib/weather-service"

export async function GET(request: Request) {
  try {
    // Get location from query params
    const { searchParams } = new URL(request.url)
    const location = searchParams.get("location") || "San Francisco, CA"

    // Fetch weather data
    const weatherData = await getCurrentWeather(location)

    return NextResponse.json(weatherData)
  } catch (error) {
    console.error("Error fetching weather data:", error)
    return NextResponse.json({ error: "Failed to fetch weather data" }, { status: 500 })
  }
}

