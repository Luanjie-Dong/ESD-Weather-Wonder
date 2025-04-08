"use client"
import { Button } from "@/components/ui/button"
import { logout } from "@/app/lib/auth"
import { useRouter } from "next/navigation"
import Navbar from "@/components/navbar"
import AuthCheck from "@/components/auth-check"
import { useState , useEffect} from "react";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Cloud, CloudRain, Edit, MapPin, MoreHorizontal, Plus, Trash2, Thermometer, ArrowUp, ArrowDown, Wind, Umbrella , Calendar} from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import axios from "axios";
import WeatherDashboard from "@/components/detail-weather"
import Swal from 'sweetalert2';
import LocationCard from "@/components/location-card"

interface AstroForecast {
  moon_phase: string;
  moonrise: string;
  moonset: string;
  sunrise: string;
  sunset: string;
}

interface DailyForecast {
  avghumidity: number;
  avgtemp_c: number;
  condition_code: number;
  condition_icon: string | null;
  condition_text: string | null;
}

interface HourlyForecastItem {
time: string;
temp_c: number;
wind_kph: number;
cloud: number;
chance_of_rain: number;
}


interface UserLocation {
  UserId: string;
  LocationId: string;
  Label: string;
  Address: string;
}

interface LocationInfo {
  UserId?: string;
  Label?: string;
  Address?: string;
}

interface locationWeather {
  LocationId: string;
  Label: string;
  Address: string;
  day: string;
  temp: number;       
  max_temp: number;   
  min_temp: number;   
  wind: number;       
  rain: number;
  astro: AstroForecast;
  daily: DailyForecast;
  hourly:HourlyForecastItem[];       
}

interface HourlyForecast {
  time: string; 
  chance_of_rain?: number; 
}

export default function DashboardPage() {
  const router = useRouter()
  const [userProfile, setUserProfile] = useState<any>({ username: 'User' });
  const [locationInfo, setLocationInfo] = useState<LocationInfo | null>(null);
  const [userLocations,setUserLocations] = useState<UserLocation[]>([])
  const [loading,setLoading] = useState(true)
  const [locationLoading,setLocationLoading] = useState(false)
  const [deleteLoading,setDeleteLoading] = useState(false)
  const [locationWeather,setLocationWeather] = useState<locationWeather[]>([])

  const api_name = process.env.NEXT_PUBLIC_API_KEY_NAME
  const api_key = process.env.NEXT_PUBLIC_API_KEY_VALUE
  const add_location_endpoint = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/add-user-location-api/v1/add_location`
  if (!api_name || !api_key) {
    throw new Error("API key or name is missing");
  }
  const headers = {"Content-Type": "application/json", [api_name]: api_key}
  const user_id = userProfile?.['user_id'];
  const user_locations_endpoint = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/user-location-api/v1/GetUserLocations/user/${user_id}`
  const delete_location_endpoint = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/user-location-api/v1/DeleteUserLocation`
  const all_weather_endpoint = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/location-weather-api/v1/get_user_weather/`
  const update_location_endpoint = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/user-location-api/v1/UpdateUserLocation`
  const update_location_weather = `${process.env.NEXT_PUBLIC_API_GATEWAY_URL}/weather-location-api/v1/poll-location/`

  
  const get_location_weather = async (user_data : UserLocation[]) => {

    if (user_data.length == 0){
      setLocationWeather([])
      setLoading(false)
      return
    }

    const locationIds = user_data.map((x) => x.LocationId);
    const validLocationIds = locationIds.filter((id) => id);
    const locationIdsString = validLocationIds.join(',');
    const url = `${all_weather_endpoint}${locationIdsString}`;
    try {
      console.log('Fetching weather now!')
      const response_forecast = await axios.get(url, { headers });
      const forecast_data = response_forecast.data;
      const formatted_weather_data:locationWeather[] = []; 

      for (let i = 0; i < forecast_data.length; i++) {
          const day = forecast_data[i].hourlyForecast?.filter((hour: HourlyForecast) => new Date(hour.time) >= new Date()).slice(0, 1)[0]?.time.replace('T'," ");
          const temp = forecast_data[i]?.dailyForecast?.avgtemp_c;
          const locationid = forecast_data[i]?.location_id;

          const locationInfo = user_data.find((x) => x.LocationId == locationid);
          if (!locationInfo) {
            console.warn(`No matching location found for LocationId: ${locationid}`);
            continue; 
          }

          const label = locationInfo.Label;
          const address = locationInfo.Address;

          const max_temp = forecast_data[i]?.dailyForecast?.maxtemp_c;
          const min_temp = forecast_data[i]?.dailyForecast?.mintemp_c;
          const wind = forecast_data[i]?.dailyForecast?.maxwind_kph;
          const rain = forecast_data[i]?.hourlyForecast?.filter((hour: HourlyForecast) => new Date(hour.time) >= new Date()).slice(0, 1)[0]?.chance_of_rain;

          const weather_data = {
            LocationId: locationid,
            Label: label || "-",
            Address: address,
            day: day || new Date().toISOString().split('T')[0],
            temp: temp || "-",
            max_temp: max_temp || "-",
            min_temp: min_temp || "-",
            wind: wind || "-",
            rain: rain ,
            astro: forecast_data[i]?.astroForecast,
            daily: forecast_data[i]?.dailyForecast,
            hourly: forecast_data[i]?.hourlyForecast,
          };
          const isDuplicate = formatted_weather_data.some(item => item.LocationId === weather_data.LocationId);
          if (!isDuplicate) {
            formatted_weather_data.push(weather_data);
          }
        }
    setLocationWeather(formatted_weather_data);
    } catch (error) {
      console.error("Error fetching weather data:", error);
    }finally {
      console.log('Extracted Weather',locationWeather)
      setLoading(false);
      setDeleteLoading(false);
    }
  }

  const get_user_location = async () => {
    setLoading(true); 
  
    try {
      const response = await axios.get(user_locations_endpoint, { headers });
        if (response.status !== 200) {
        console.warn(`Unexpected response status: ${response.status}`);
        setUserLocations([]);
        get_location_weather([]);
        return;
      }
      const { data } = response;
      if (!data || !data.Result || !data.Result.Success) {
        console.warn("Result.Success is false or missing. Setting empty array.");
        setUserLocations([]);
        get_location_weather([]);
        return;
      }
  
      const user_data = data.UserLocations;
      if (!Array.isArray(user_data)) {
        console.warn("UserLocations is not an array. Setting empty array.");
        setUserLocations([]);
        get_location_weather([]);
        return;
      }
      const clean_user_data = filterUserData(user_data);
      console.log('Getting weather')
      setUserLocations(clean_user_data);
      get_location_weather(clean_user_data);
  
    } catch (error) {
      console.error("Error fetching user locations:", error);
      setUserLocations([]);
      get_location_weather([]);
    } finally {
      setLoading(false); 
    }
  };

  const addLocation = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); 
    setLocationLoading(true);
    try {

      const payload = {"address":locationInfo?.['Address'],"label":locationInfo?.['Label'],'user_id':user_id}
      const response = await axios.post(add_location_endpoint,payload,{ headers });

      if (response.status == 201) {
        Swal.fire({
          icon: 'success', 
          title: 'Location Added Successfully!',
          text: 'The location has been added successfully.',
          confirmButtonText: 'Go to Dashboard',
          customClass: {
            confirmButton: 'btn btn-primary' 
          }
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = "/dashboard"; 
          }
        });
      }

      if (response.status == 500){
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Failed to add location. Please try again.',
        });
      }
    }
    catch (error) {
      console.error("Error:", error);
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Failed to add location (API call). Please try again.',
      });
    }
    finally {
      setLocationLoading(false); 
    }
  }

  const handleAddLocation = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setLocationInfo((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const deleteLocation = async (locationId: string) => {
    setDeleteLoading(true)
    try {
      const location_info = userLocations.filter((x) => x.LocationId == locationId);
      const response = await axios.delete(delete_location_endpoint, {
        data: location_info[0], 
        headers: headers,    
      });
  
      if (response.status == 200) {
        get_user_location();
      } else {
        console.warn(`Unexpected response status: ${response.status}`);
      }
    } catch (error) {
      console.error(`Error deleting location: ${locationId}`, error);
    }
  };

  const handleUpdate = async (id: string, updatedData: { Label: string; Address: string }) => {
    try {
      const payload = {
        UserId: user_id,
        LocationId: id,
        Label: updatedData.Label,
        Address: updatedData.Address,
      };
  
      const response = await axios.patch(update_location_endpoint, payload, {
        headers: headers,
      });
  
      if (response.status === 200 || response.status === 204) {
        get_user_location(); 
      } else {
        console.warn(`Unexpected response status: ${response.status}`);
      }
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error(`Error updating location: ${id}`, error.response?.data || error.message);
      } else {
        console.error(`Error updating location: ${id}`, error);
      }
    }
  };

  const updateWeather = async (locationId: string) => {
    try {
      const response = await axios.post(
        update_location_weather + locationId,
        { location_id: locationId }, 
        { headers: headers }         
      );;
  
      if (response.status == 200) {
        get_user_location();
      } else {
        console.warn(`Unexpected response status: ${response.status}`);
      }
    } catch (error) {
      console.error(`Error updating location: ${locationId}`, error);
    }
  };

  const filterUserData = (user_data: UserLocation[]): UserLocation[] => {
    const seenLocationIds = new Set<string>(); 
    const filteredData = user_data.filter(item => {
      if (seenLocationIds.has(item.LocationId)) {
        return false; 
      }
      seenLocationIds.add(item.LocationId); 
      return true; 
    });
    return filteredData; 
  };


  useEffect(() => {
      const userProfileString = localStorage.getItem('user_profile');
      if (userProfileString) {
        setUserProfile(JSON.parse(userProfileString));
        }
      }, []);

  

  useEffect(() => {
    if (user_id){
      console.log("Getting locations")
      get_user_location();
    }
    
  }, [user_id]);


  const handleLogout = () => {
    logout()
    router.push("/")
  }
  
  return (
    <AuthCheck>
      <div className={`relative ${locationLoading ? "blur-lg pointer-events-none" : ""} flex min-h-screen flex-col`}>
      <Navbar />
      <main className="flex-1 pb-16 pt-6 md:pb-6">
        {/* Header Section */}
        <div className="container space-y-6">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-800 md:text-4xl capitalize">
              Welcome {userProfile.username}!
            </h1>
            <Button
              variant="outline"
              size="sm"
              className="rounded-md border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              onClick={handleLogout}
            >
              Log Out
            </Button>
          </div>
          {/* Locations Section */}
          <div className="container space-y-6 pl-0">
          <div className="flex items-center justify-between">
          {loading ? (
                <div className="flex items-center justify-center space-x-4 col-span-full">
                  <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-blue-500 border-opacity-50"></div>
                  <p className="text-lg font-medium text-gray-700 dark:text-gray-300">Loading locations...</p>
                </div>
              ) : (
                <h2 className="text-2xl font-semibold text-gray-800 md:text-3xl">
                  {locationWeather.length} Location(s)
                </h2>
              )
          }
        
          </div>

          <Tabs defaultValue="saved">
            <TabsList className="mb-4 gap-4">
              <TabsTrigger value="saved" className="border border-indigo-600 hover:bg-indigo-600 hover:text-white">Saved Locations</TabsTrigger>
              <TabsTrigger value="add" className="border border-red-600 hover:bg-red-600 hover:text-white">Add Location</TabsTrigger>
            </TabsList>

            <TabsContent value="saved" className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {locationWeather.length > 0 && locationWeather.map((location) => (
                  <LocationCard
                  key={location.LocationId}
                  location={location}
                  onDelete={deleteLocation}
                  onUpdate={handleUpdate}
                  onRefresh={updateWeather}
                  />
                ))}
                {!loading && userLocations.length == 0 ? (
                  <div className="flex flex-col items-center justify-center text-center py-12 space-y-6 col-span-full">
                    <div className="text-gray-400 dark:text-gray-500">
                      <MapPin size={64} strokeWidth={1.5} />
                    </div>
                    <p className="text-2xl font-semibold text-gray-600 dark:text-gray-300">
                      No location saved yet 😔
                    </p>
                  </div>
                ) : deleteLoading?(
                <div>
                  <div className="absolute inset-0 flex justify-center bg-black bg-opacity-50 z-50">
                    <p className="text-white text-lg font-semibold pt-48">Deleting location...</p>
                  </div>
                </div>):(<div></div>)}
              </div>
            </TabsContent>

            <TabsContent value="add">
              
              <Card className={`relative ${locationLoading ? "blur-lg pointer-events-none" : ""}`}>
                <CardHeader>
                  <CardTitle>Add New Location</CardTitle>
                  <CardDescription>Enter a city name or address to add a new location</CardDescription>
                </CardHeader>
                <form onSubmit={addLocation}>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="location-name">Location Address</Label>
                      <Input id="location-name" name="Address" value={locationInfo?.Address || ""} onChange={handleAddLocation} placeholder="City, State or Address" />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="location-label">Label</Label>
                      <Input id="location-label" name="Label" value={locationInfo?.Label || ""} onChange={handleAddLocation} placeholder="Home, Work, etc." />
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <div></div>
                    <Button className="bg-highlight hover:bg-purple-700" type="submit">Add Location</Button>
                  </CardFooter>
                </form>
              </Card>
              {locationLoading && (
                  <div className="absolute inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
                    <p className="text-white text-lg font-semibold">Adding location...</p>
                  </div>
                )}
            </TabsContent>
          </Tabs>
        </div>
          
        </div>
      </main>

    </div>
  </AuthCheck>
  )
}