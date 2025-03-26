import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AlertTriangle, CloudLightning, CloudRain, Info } from "lucide-react"
import Navbar from "@/components/navbar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function AlertsPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />

      <main className="flex-1 pb-16 pt-6 md:pb-6">
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold md:text-3xl">Emergency Alerts</h1>
            <Badge className="bg-destructive">2 Active Alerts</Badge>
          </div>

          <Tabs defaultValue="active">
            <TabsList className="mb-4">
              <TabsTrigger value="active">Active Alerts</TabsTrigger>
              <TabsTrigger value="history">Alert History</TabsTrigger>
            </TabsList>

            <TabsContent value="active" className="space-y-4">
              {/* Severe Alert */}
              <Card className="border-l-4 border-l-destructive">
                <CardHeader className="pb-2">
                  <div className="flex items-center">
                    <AlertTriangle className="mr-2 h-5 w-5 text-destructive" />
                    <CardTitle className="text-lg text-destructive">Severe Thunderstorm Warning</CardTitle>
                  </div>
                  <CardDescription className="flex items-center justify-between">
                    <span>Chicago, IL</span>
                    <Badge variant="outline" className="text-destructive">
                      Expires in 2 hours
                    </Badge>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="mb-4 text-sm">
                    The National Weather Service has issued a Severe Thunderstorm Warning for your area. Strong
                    thunderstorms with potential for flash flooding and wind gusts up to 60mph are expected. Take
                    necessary precautions and stay indoors if possible.
                  </p>
                  <div className="grid grid-cols-2 gap-2 md:grid-cols-4">
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Severity</p>
                      <p className="font-medium text-destructive">Severe</p>
                    </div>
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Wind</p>
                      <p className="font-medium">60 mph</p>
                    </div>
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Hail</p>
                      <p className="font-medium">1.5 in</p>
                    </div>
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Flash Flood</p>
                      <p className="font-medium">Possible</p>
                    </div>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    <Button size="sm" className="bg-highlight">
                      View on Map
                    </Button>
                    <Button size="sm" variant="outline">
                      Safety Tips
                    </Button>
                  </div>
                </CardContent>
              </Card>

              {/* Moderate Alert */}
              <Card className="border-l-4 border-l-accent">
                <CardHeader className="pb-2">
                  <div className="flex items-center">
                    <CloudRain className="mr-2 h-5 w-5 text-accent" />
                    <CardTitle className="text-lg text-accent">Flood Watch</CardTitle>
                  </div>
                  <CardDescription className="flex items-center justify-between">
                    <span>San Francisco, CA</span>
                    <Badge variant="outline" className="text-accent">
                      Expires in 8 hours
                    </Badge>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <p className="mb-4 text-sm">
                    A Flood Watch has been issued for your area due to heavy rainfall expected over the next 8 hours.
                    Low-lying areas may experience flooding. Stay alert and avoid flood-prone areas.
                  </p>
                  <div className="grid grid-cols-2 gap-2 md:grid-cols-3">
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Severity</p>
                      <p className="font-medium text-accent">Moderate</p>
                    </div>
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Rainfall</p>
                      <p className="font-medium">2-3 in</p>
                    </div>
                    <div className="rounded-md bg-muted p-2 text-center">
                      <p className="text-xs text-muted-foreground">Duration</p>
                      <p className="font-medium">8 hours</p>
                    </div>
                  </div>
                  <div className="mt-4 flex flex-wrap gap-2">
                    <Button size="sm" className="bg-highlight">
                      View on Map
                    </Button>
                    <Button size="sm" variant="outline">
                      Safety Tips
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="history" className="space-y-4">
              {/* Past Alerts */}
              {[
                {
                  title: "Severe Thunderstorm Warning",
                  location: "Chicago, IL",
                  date: "Yesterday, 4:30 PM",
                  icon: CloudLightning,
                  severity: "Severe",
                },
                {
                  title: "Flash Flood Warning",
                  location: "San Francisco, CA",
                  date: "March 15, 2:15 PM",
                  icon: CloudRain,
                  severity: "Moderate",
                },
                {
                  title: "Wind Advisory",
                  location: "New York, NY",
                  date: "March 10, 9:00 AM",
                  icon: Info,
                  severity: "Minor",
                },
              ].map((alert) => (
                <Card key={alert.title + alert.date} className="border-l-4 border-l-muted">
                  <CardHeader className="pb-2">
                    <div className="flex items-center">
                      <alert.icon className="mr-2 h-5 w-5 text-muted-foreground" />
                      <CardTitle className="text-lg text-muted-foreground">{alert.title}</CardTitle>
                    </div>
                    <CardDescription className="flex items-center justify-between">
                      <span>{alert.location}</span>
                      <Badge variant="outline">{alert.date}</Badge>
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <Badge variant="outline">{alert.severity}</Badge>
                      <Button size="sm" variant="ghost">
                        View Details
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}

