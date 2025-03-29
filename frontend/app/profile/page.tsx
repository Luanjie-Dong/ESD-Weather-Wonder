"use client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import Navbar from "@/components/navbar"
import AuthCheck from "@/components/auth-check"
import { useState , useEffect} from "react";
import axios from "axios";
import { Input } from "@/components/ui/input"
import { login } from "../lib/auth"

interface UserProfile {
  city: string;
  country: string;
  created_at: Date; 
  email: string;
  state: string;
  user_id: string;
  username: string | null;
};

export default function SettingsPage() {
  
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [loading,setLoading] = useState(false)
  const api_name = process.env.NEXT_PUBLIC_API_KEY_NAME
  const api_key = process.env.NEXT_PUBLIC_API_KEY_VALUE
  if (!api_name || !api_key) {
    throw new Error("API key or name is missing");
  }

  const headers = {"Content-Type": "application/json", [api_name]: api_key}

  useEffect(() => {
    const userProfileString = localStorage.getItem('user_profile');
    if (userProfileString) {
      setUserProfile(JSON.parse(userProfileString));
      }
    }, []);

  const user_id = userProfile?.['user_id'];
  const update_user_endpoint = `http://localhost:8000/user-api/v1/user/${user_id}`


  const updateProfile = async() => {
    setLoading(true)

    try{
      const response = await axios.put(update_user_endpoint,userProfile, { headers });

      if (response.status == 200){
        console.log(response.data)
        alert("Profile updated!")
        if (!userProfile) {
          throw new Error("User profile not found in response.");
        }
        login(userProfile)
      }
    } 
    finally{
      setLoading(false)
    }
  }






  return (
    <AuthCheck>
    <div className={`relative ${loading ? "blur-lg pointer-events-none" : ""} flex min-h-screen flex-col`}>
      <Navbar />
        {/* Main Content */}
        <main className="container mx-auto p-6">
          <h1 className="text-3xl font-bold text-gray-800 mb-8">Your Profile</h1>

          {/* Profile Card */}
          <Card className="shadow-md">
            <CardHeader>
              <CardTitle>Profile Information</CardTitle>
              <CardDescription>View and update your profile details.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  defaultValue={userProfile?.username || "Not set"}
                  disabled={!userProfile}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  defaultValue={userProfile?.email || "Not set"}
                  disabled={!userProfile}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="location">Location</Label>
                <Input
                  id="location"
                  defaultValue={`${userProfile?.city || ""}, ${userProfile?.country || ""}`}
                  disabled={!userProfile}
                />
              </div>
            </CardContent>
            <CardFooter className="flex justify-end">
              
              <Button onClick={updateProfile}>Save Changes</Button>
            </CardFooter>
          </Card>
          {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
              <p className="text-white text-lg font-semibold">Updating profile...</p>
            </div>
          )}

        </main>

    </div>
    </AuthCheck>
  )
}




