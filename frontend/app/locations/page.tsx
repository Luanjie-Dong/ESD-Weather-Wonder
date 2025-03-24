import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Cloud, CloudRain, Edit, MapPin, MoreHorizontal, Plus, Trash2 } from "lucide-react"
import Navbar from "@/components/navbar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import AuthCheck from "../../components/auth-check"

export default function LocationsPage() {
  return (
    <AuthCheck>
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 pb-16 pt-6 md:pb-6">
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold md:text-3xl">Location Management</h1>
            <Button className="bg-accent">
              <Plus className="mr-2 h-4 w-4" /> Add Location
            </Button>
          </div>

          <Tabs defaultValue="saved">
            <TabsList className="mb-4">
              <TabsTrigger value="saved">Saved Locations</TabsTrigger>
              <TabsTrigger value="add">Add Location</TabsTrigger>
            </TabsList>

            <TabsContent value="saved" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {[
                  { name: "San Francisco, CA", temp: "72°F", icon: Cloud, primary: true },
                  { name: "New York, NY", temp: "65°F", icon: Cloud },
                  { name: "Los Angeles, CA", temp: "82°F", icon: Cloud },
                  { name: "Chicago, IL", temp: "58°F", icon: CloudRain },
                  { name: "Miami, FL", temp: "85°F", icon: Cloud },
                ].map((location) => (
                  <Card key={location.name} className={location.primary ? "border-2 border-brand" : ""}>
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center text-lg">
                          <MapPin className="mr-2 h-4 w-4" />
                          {location.name}
                        </CardTitle>
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="icon">
                              <MoreHorizontal className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" /> Edit
                            </DropdownMenuItem>
                            {!location.primary && (
                              <DropdownMenuItem>
                                <MapPin className="mr-2 h-4 w-4" /> Set as Primary
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuItem className="text-destructive">
                              <Trash2 className="mr-2 h-4 w-4" /> Delete
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                      {location.primary && <CardDescription>Primary Location</CardDescription>}
                    </CardHeader>
                    <CardContent className="flex items-center justify-between pb-4">
                      <p className="text-2xl font-bold">{location.temp}</p>
                      <location.icon className="h-8 w-8 text-brand" />
                    </CardContent>
                    <CardFooter className="pt-0">
                      <Button variant="outline" size="sm" className="w-full">
                        View Forecast
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
              </div>
            </TabsContent>

            <TabsContent value="add">
              <Card>
                <CardHeader>
                  <CardTitle>Add New Location</CardTitle>
                  <CardDescription>Enter a city name or address to add a new location</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="location-name">Location Name</Label>
                    <Input id="location-name" placeholder="City, State or Address" />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="location-label">Label (Optional)</Label>
                    <Input id="location-label" placeholder="Home, Work, etc." />
                  </div>
                </CardContent>
                <CardFooter className="flex justify-between">
                  <Button variant="outline">Cancel</Button>
                  <Button className="bg-highlight">Add Location</Button>
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

