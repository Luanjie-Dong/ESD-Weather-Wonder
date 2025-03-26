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
    useEffect(() => {
      const userProfileString = localStorage.getItem('user_profile');
      if (userProfileString) {
        setUserProfile(JSON.parse(userProfileString));
        }
      }, []);
  return (
    <AuthCheck>
    <div className="flex min-h-screen flex-col">
      <Navbar />
        {/* Main Content */}
        <main className="container mx-auto p-6 space-y-8">
          <h1 className="text-3xl font-bold text-gray-800">Your Profile</h1>

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
              <Button variant="outline" className="mr-2">
                Cancel
              </Button>
              <Button>Save Changes</Button>
            </CardFooter>
          </Card>

          
          
        </main>

    </div>
    </AuthCheck>
  )
}




