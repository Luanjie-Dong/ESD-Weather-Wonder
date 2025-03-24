import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import Navbar from "@/components/navbar"
import AuthCheck from "../../components/auth-check"

export default function SettingsPage() {
  return (
    <AuthCheck>
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1 pb-16 pt-6 md:pb-6">
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold md:text-3xl">Notification Settings</h1>
            <Button className="bg-highlight">Save Changes</Button>
          </div>

          <Tabs defaultValue="notifications">
            <TabsList className="mb-4">
              <TabsTrigger value="notifications">Notifications</TabsTrigger>
              <TabsTrigger value="preferences">Preferences</TabsTrigger>
              <TabsTrigger value="account">Account</TabsTrigger>
            </TabsList>

            <TabsContent value="notifications" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Daily Weather Notifications</CardTitle>
                  <CardDescription>Receive daily weather forecasts for your saved locations</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="daily-forecast" className="flex flex-col space-y-1">
                      <span>Enable Daily Forecast</span>
                      <span className="text-xs text-muted-foreground">
                        Receive a daily summary of the weather forecast
                      </span>
                    </Label>
                    <Switch id="daily-forecast" defaultChecked />
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="forecast-time" className="flex flex-col space-y-1">
                      <span>Forecast Time</span>
                      <span className="text-xs text-muted-foreground">When to receive your daily forecast</span>
                    </Label>
                    <Select defaultValue="8">
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select time" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="6">6:00 AM</SelectItem>
                        <SelectItem value="7">7:00 AM</SelectItem>
                        <SelectItem value="8">8:00 AM</SelectItem>
                        <SelectItem value="9">9:00 AM</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="weekend-forecast" className="flex flex-col space-y-1">
                      <span>Weekend Forecast</span>
                      <span className="text-xs text-muted-foreground">Receive a special forecast for the weekend</span>
                    </Label>
                    <Switch id="weekend-forecast" defaultChecked />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Emergency Weather Alerts</CardTitle>
                  <CardDescription>Configure emergency weather alert preferences</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="emergency-alerts" className="flex flex-col space-y-1">
                      <span>Emergency Alerts</span>
                      <span className="text-xs text-muted-foreground">
                        Receive alerts for severe weather conditions
                      </span>
                    </Label>
                    <Switch id="emergency-alerts" defaultChecked />
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="severity-threshold">Severity Threshold</Label>
                      <span className="text-sm font-medium">Moderate</span>
                    </div>
                    <Slider
                      id="severity-threshold"
                      defaultValue={[2]}
                      max={3}
                      step={1}
                      className="[&>span:first-child]:bg-accent"
                    />
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Minor</span>
                      <span>Moderate</span>
                      <span>Severe</span>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label>Alert Types</Label>
                    <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
                      {[
                        "Thunderstorms",
                        "Floods",
                        "Hurricanes",
                        "Tornadoes",
                        "Winter Storms",
                        "Extreme Heat",
                        "Air Quality",
                        "Fire Weather",
                      ].map((type) => (
                        <div key={type} className="flex items-center space-x-2">
                          <Switch id={`alert-${type}`} defaultChecked />
                          <Label htmlFor={`alert-${type}`}>{type}</Label>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">
                    Test Emergency Alert
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="preferences" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Display Preferences</CardTitle>
                  <CardDescription>Customize how weather information is displayed</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="units" className="flex flex-col space-y-1">
                      <span>Temperature Units</span>
                    </Label>
                    <Select defaultValue="fahrenheit">
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select units" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="fahrenheit">Fahrenheit (°F)</SelectItem>
                        <SelectItem value="celsius">Celsius (°C)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="wind-units" className="flex flex-col space-y-1">
                      <span>Wind Speed Units</span>
                    </Label>
                    <Select defaultValue="mph">
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select units" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="mph">Miles per hour (mph)</SelectItem>
                        <SelectItem value="kph">Kilometers per hour (km/h)</SelectItem>
                        <SelectItem value="knots">Knots (kn)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="time-format" className="flex flex-col space-y-1">
                      <span>Time Format</span>
                    </Label>
                    <Select defaultValue="12h">
                      <SelectTrigger className="w-[180px]">
                        <SelectValue placeholder="Select format" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="12h">12-hour (AM/PM)</SelectItem>
                        <SelectItem value="24h">24-hour</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="account" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>Account Information</CardTitle>
                  <CardDescription>Manage your account settings</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Name</Label>
                    <div className="rounded-md border border-input bg-muted px-3 py-2">Alex Johnson</div>
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="email">Email</Label>
                    <div className="rounded-md border border-input bg-muted px-3 py-2">alex@example.com</div>
                  </div>

                  <div className="flex items-center justify-between space-x-2">
                    <Label htmlFor="notifications-email" className="flex flex-col space-y-1">
                      <span>Email Notifications</span>
                      <span className="text-xs text-muted-foreground">Receive notifications via email</span>
                    </Label>
                    <Switch id="notifications-email" defaultChecked />
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button variant="outline">Change Password</Button>
                  <Button variant="destructive">Delete Account</Button>
                </CardFooter>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
    </AuthCheck>
  )
}

