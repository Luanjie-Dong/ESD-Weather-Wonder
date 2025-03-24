"use client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Cloud, CloudRain, Edit, MapPin, MoreHorizontal, Plus, Trash2 } from "lucide-react"
import Navbar from "@/components/navbar"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import AuthCheck from "@/components/auth-check"
import { useState , useEffect} from "react";
import axios from "axios";
import { useRouter } from 'next/router';

interface UserProfile {
  city: string;
  country: string;
  created_at: Date; 
  email: string;
  state: string;
  user_id: string;
  username: string | null;
};

interface UserLocation {
  UserId?: string;
  LocationId?: string;
  Label?: string;
  Address?: string;
}

interface LocationInfo {
  UserId?: string;
  Label?: string;
  Address?: string;
}

export default function LocationsPage() {
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [locationInfo, setLocationInfo] = useState<LocationInfo | null>(null);
  const [loadLocation,setLoadLocation] = useState(true)

  const api_name = process.env.NEXT_PUBLIC_API_KEY_NAME
  const api_key = process.env.NEXT_PUBLIC_API_KEY_VALUE
  if (!api_name || !api_key) {
    throw new Error("API key or name is missing");
  }
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const userProfileString = localStorage.getItem('user_profile');
      if (userProfileString) {
        setUserProfile(JSON.parse(userProfileString));
        
          const formattedAddress = `${userProfile?.country}, ${userProfile?.state}, ${userProfile?.city}`;

          // Set the location info
          setLocationInfo({UserId: userProfile?.user_id,Address: formattedAddress,Label: "Home",});
      
        }
      }}, []);

  const [userLocations,setUserLocations] = useState<UserLocation[]>([])
  const headers = {
    "Content-Type": "application/json", 
    [api_name]: api_key,               
  }

  const user_id = userProfile?.['user_id'];
  console.log(user_id)
  const user_locations_endpoint = `http://localhost:8000//user-location-api/v1/GetUserLocations/user/${user_id}`
  console.log(user_locations_endpoint)
  const get_user_location = async () =>{
    
    try{
      const response = await axios.get(user_locations_endpoint,{ headers });
      if (response.status == 200){
        console.log(response.data)
        const user_data = response.data?.UserLocations
        if (user_data){
          setUserLocations(user_data)
          setLoadLocation(false)
        }

      }

    } catch (error){
      console.error("Error:", error);
    }
  }

  useEffect(() => {
    if (user_id){
      console.log("Getting locations")
      get_user_location();
    }
    
  }, [user_id]);

  
  return (
    <AuthCheck>
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 pb-16 pt-6 md:pb-6">
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold md:text-3xl">Location Management</h1>
            {/* <Button className="bg-accent">
              <Plus className="mr-2 h-4 w-4" /> Add Location
            </Button> */}
          </div>

          <Tabs defaultValue="saved">
            <TabsList className="mb-4 gap-4">
              <TabsTrigger value="saved" className="border border-indigo-600">Saved Locations</TabsTrigger>
              <TabsTrigger value="add" className="border border-red-600">Add Location</TabsTrigger>
            </TabsList>

            <TabsContent value="saved" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {userLocations.length > 0 && userLocations.map((location) => (
                  <Card key={location.Address} className="border-2 border-brand">
                    <CardHeader className="pb-2">
                      <div className="flex items-center justify-between">
                        <CardTitle className="flex items-center text-lg">
                          <MapPin className="mr-2 h-4 w-4" />
                          {location.Address}
                        </CardTitle>
                        {/* <DropdownMenu>
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
                        </DropdownMenu> */}
                      </div>
                      {/* {location.primary && <CardDescription>Primary Location</CardDescription>} */}
                    </CardHeader>
                    <CardContent className="flex items-center justify-between pb-4">
                      <p className="text-2xl font-bold">{location.Label}</p>
                      {/* <location.icon className="h-8 w-8 text-brand" /> */}
                    </CardContent>
                    <CardFooter className="pt-0">
                      <Button variant="outline" size="sm" className="w-full">
                        View Forecast
                      </Button>
                    </CardFooter>
                  </Card>
                ))}
                {loadLocation ? (
                  <div className="flex flex-col space-y-4">
                    <div className="animate-spin rounded-full h-10 w-10 border-t-4 border-blue-500 border-opacity-50"></div>
                    <p className="text-lg text-gray-700">Loading locations...</p>
                  </div>
                ) : userLocations.length === 0 ? (
                  <div className="text-xl text-center text-gray-500">
                    No location saved :/
                  </div>
                ) : (<div></div>)}
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

